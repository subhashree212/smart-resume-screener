import redis
from rq import Worker, Queue, Connection
from config import Config

conn = redis.from_url(Config.REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(Queue('default'))
        worker.work()
