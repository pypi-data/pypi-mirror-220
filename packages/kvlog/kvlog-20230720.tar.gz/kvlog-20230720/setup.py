import time
import glob
from distutils.core import setup

setup(
  name = 'kvlog',
  packages = ['kvlog'],
  version = time.strftime('%Y%m%d'),
  description = 'A simple Queue and DB - with get/put operations over HTTPS.',
  long_description = 'Uses Paxos for replication and SQLite for storage. Leaderless and highly available.',
  author = 'Bhupendra Singh',
  author_email = 'bhsingh@gmail.com',
  url = 'https://github.com/magicray/kvlog',
  keywords = ['queue', 'paxos', 'pubsub', 'pub', 'sub', 'kv', 'key', 'value']
)
