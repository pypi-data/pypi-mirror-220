import os
import sys
import time
import uuid
import sanic
import pickle
import hashlib
import sqlite3
import asyncio
import aiohttp
from logging import critical as log

APP = sanic.Sanic('kvlog')
APP.config.KEEP_ALIVE_TIMEOUT = 300


class Database():
    def __init__(self, db):
        d = hashlib.sha256(db.encode()).hexdigest()
        self.path = os.path.join('db', d[0:3], d[3:6], d + '.sqlite3')

        if not os.path.isfile(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

            tmp = os.path.join('db', str(uuid.uuid4()))

            db = sqlite3.connect(tmp)
            db.execute('''create table log(
                          log_seq      unsigned int not null primary key,
                          promised_seq unsigned int,
                          accepted_seq unsigned int,
                          key          text,
                          version      unsigned int,
                          value        blob)''')
            db.execute('create index i0 on log(key,version,log_seq)')
            db.execute('insert into log(log_seq) values(0)')
            db.commit()

            os.replace(tmp, self.path)

    def row_read(self, seq):
        rows = self.sql('select * from log where log_seq=?', [seq])
        return rows[0] if rows else None

    def max_log_seq(self):
        return self.db.execute('select max(log_seq) from log').fetchone()[0]

    def sql(self, query, args=[]):
        return self.db.execute(query, args).fetchall()

    def commit(self):
        self.db.execute('commit')

    def __enter__(self):
        self.db = sqlite3.connect(self.path, timeout=30)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.db.close()


@APP.post('/<phase:str>/<db:str>/<log_seq:int>/<proposal_seq:int>')
async def paxos_server(request, phase, db, log_seq, proposal_seq):
    with Database(db) as db:
        db.sql('update log set key=null where log_seq=0')

        db.sql('insert or ignore into log values(?,0,0,null,null,null)',
               [log_seq])
        _, promised_seq, accepted_seq, key, ver, value = db.row_read(log_seq)

        if promised_seq is None and accepted_seq is None:
            if 'promise' == phase:
                return response([999999999999999, key, ver, value])

            if 'accept' == phase or 'learn' == phase:
                return response('OK')

        if 'promise' == phase and proposal_seq > promised_seq:
            db.sql('update log set promised_seq=? where log_seq=?',
                   [proposal_seq, log_seq])
            db.commit()

            return response([accepted_seq, key, ver, value])

        if 'accept' == phase and proposal_seq == promised_seq:
            key, version, value = pickle.loads(request.body)

            db.sql('''update log
                      set accepted_seq=?, key=?, version=?, value=?
                      where log_seq=?
                   ''', [proposal_seq, key, version, value, log_seq])
            db.commit()

            return response('OK')

        if 'learn' == phase and promised_seq == accepted_seq == proposal_seq:
            db.sql('''update log
                      set promised_seq=null, accepted_seq=null
                      where log_seq=?
                   ''', [log_seq])
            db.commit()

            return response('OK')

    raise sanic.exceptions.BadRequest('INVALID_SEQ_OR_UNKNOWN')


async def paxos_client(db, log_seq, key, version, value):
    quorum = int((len(sys.argv)-1)/2) + 1
    url = '{{}}/{}/{}/{}'.format(db, log_seq, time.strftime('%Y%m%d%H%M%S'))

    res = await rpc(url.format('promise'))
    if quorum > len(res):
        raise sanic.exceptions.BadRequest('NO_PROMISE_QUORUM')

    proposal = (0, key, version, value)
    for accepted_seq, k, ver, val in res.values():
        if accepted_seq > proposal[0]:
            proposal = (accepted_seq, k, ver, val)

    res = await rpc(url.format('accept'), proposal[1:])
    if quorum > len(res):
        raise sanic.exceptions.BadRequest('NO_ACCEPT_QUORUM')

    await rpc(url.format('learn'))

    return 'OK'


async def put_helper(db, key, version, value):
    server_list = sorted(sys.argv[1:])
    server_count = len(server_list)
    my_server_index = server_list.index(sys.argv[1])

    with Database(db) as DB:
        DB.sql('update log set key=null where log_seq=0')
        max_log_seq = DB.max_log_seq()

        tmp = int((max_log_seq + server_count) / server_count) * server_count
        log_seq = tmp + my_server_index

        DB.sql('insert into log values(?,0,0,null,null,null)', [log_seq])
        DB.commit()

    if 'OK' == await paxos_client(db, log_seq, key, version, value):
        return log_seq


@APP.put('/<db:str>/<key:str>/<version:int>')
async def put_key_version(request, db, key, version):
    log_seq = await put_helper(db, key, version, request.body)

    if log_seq is None:
        raise sanic.exceptions.BadRequest('FAILED')

    return sanic.response.json(dict(writer=sys.argv[1], log_seq=log_seq))


@APP.put('/<db:str>/<key:str>')
async def put_key(request, db, key):
    return await put_key_version(request, db, key, None)


@APP.put('/<db:str>')
async def append(request, db):
    if not hasattr(append, 'lock'):
        append.lock = asyncio.Lock()
        append.batch = dict(queue=list())

    my_batch = append.batch
    my_batch['queue'].append(request.body)

    async with append.lock:
        if append.batch == my_batch:
            value = b''.join(append.batch.pop('queue'))
            append.batch = dict(queue=list())

            my_batch['result'] = await put_helper(db, None, None, value)

        if my_batch.get('result', None) is not None:
            return sanic.response.json(
                dict(writer=sys.argv[1], log_seq=my_batch['result']))

    raise sanic.exceptions.BadRequest('FAILED')


@APP.post('/key_log_seq/<db:str>/<key:str>')
async def key_log_seq(request, db, key):
    with Database(db) as db:
        rows1 = db.sql('''select version, min(log_seq) from log
                          where key=? and version is not null
                          group by version
                          order by version desc
                          limit 1
                       ''', [key])

        rows2 = db.sql('''select max(log_seq) from log
                          where key=? and version is null
                       ''', [key])

        log_seq = max(rows1[0][1] if rows1 else 0,
                      rows2[0][0] if rows2 else 0)

        return response(log_seq)


async def sync(db, log_seq):
    for i in range(2):
        with Database(db) as DB:
            rows = DB.sql('select * from log where log_seq=?', [log_seq])

        if rows and rows[0][1] is None and rows[0][2] is None:
            return rows[0]

        await paxos_client(db, log_seq, None, None, None)


@APP.get('/<db:str>/<key:str>')
async def get_value(request, db, key):
    res = await rpc('key_log_seq/{}/{}'.format(db, key))
    log_seq = max(res.values())

    if log_seq < 1:
        raise sanic.exceptions.NotFound('KEY_NOT_FOUND')

    row = await sync(db, log_seq)
    if row and row[3] == key:
        return sanic.response.raw(row[5], headers={
            'x-seq': log_seq,
            'x-key': row[3],
            'x-version': row[4]})

    raise sanic.exceptions.BadRequest('SYNC_FAILED')


@APP.post('/max_log_seq/<db:str>')
async def max_log_seq(request, db):
    with Database(db) as db:
        return response(db.max_log_seq())


@APP.get('/<db:str>/<log_seq:int>')
async def get_log(request, db, log_seq):
    with Database(db) as DB:
        max_log_seq = DB.max_log_seq()

    if log_seq > max_log_seq:
        res = await rpc('max_log_seq/{}'.format(db))
        max_log_seq = max(res.values())

    if log_seq > max_log_seq:
        raise sanic.exceptions.NotFound('LOG_SEQ_OUT_OF_RANGE')

    row = await sync(db, log_seq)
    if row:
        return sanic.response.raw(row[5], headers={
            'x-seq': row[0],
            'x-key': row[3]})

    raise sanic.exceptions.NotFound('ROW_NOT_FOUND')


def response(obj):
    return sanic.response.raw(pickle.dumps(obj))


async def rpc(url, obj=None):
    servers = sys.argv[1:]

    if not hasattr(rpc, 'session'):
        rpc.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
                limit=1000, limit_per_host=1000, ssl=False))

    responses = await asyncio.gather(
        *[asyncio.ensure_future(rpc.session.post(
            'https://{}/{}'.format(s, url), data=pickle.dumps(obj)))
          for s in servers],
        return_exceptions=True)

    result = dict()
    for s, r in zip(servers, responses):
        if type(r) is aiohttp.client_reqrep.ClientResponse:
            if 200 == r.status:
                result[s] = pickle.loads(await r.read())

    return result


if '__main__' == __name__:
    for i, srv in enumerate(sys.argv[1:]):
        log('nodes({}) : {}'.format(i+1, srv))

    HOST, PORT = sys.argv[1].split(':')
    APP.run(HOST, int(PORT), single_process=True, access_log=True,
            ssl=dict(cert='cert.pem', key='key.pem', names=["*"]))
