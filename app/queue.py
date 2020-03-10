import json
import os

import redis


class Queue:
    def __init__(self, r: redis.StrictRedis):
        self.redis = r

    @classmethod
    def create(cls):
        pool = redis.ConnectionPool(
            host=os.environ.get('REDIS_HOST') or 'localhost',
            port=int(os.environ.get('REDIS_PORT') or '6379'),
            db=0)
        return cls(redis.StrictRedis(connection_pool=pool))

    def put(self, key, value: dict):
        self.redis.set(key, json.dumps(value))

    def get(self, key):
        value = json.loads(self.redis.get(key).decode('utf-8'))
        self.redis.delete(key)
        return value

    def peek_all_keys(self):
        return [key.decode('utf-8') for key in self.redis.scan_iter()]
