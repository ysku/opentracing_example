import json
import os
import time

import redis
import requests


LOOP_INTERVAL = int(os.environ.get('LOOP_INTERVAL') or 5)
API_HOST = os.environ.get('API_HOST') or 'localhost'
API_PORT = os.environ.get('API_PORT') or '50002'


class APIClient:
    def __init__(self):
        self.base_url = f'http://{API_HOST}:{API_PORT}'

    def save(self, body=None):
        if body is None:
            body = {}
        res = requests.post(f'{self.base_url}/save', json=body)
        res.raise_for_status()
        return res.json()


class Subscriber:
    def __init__(self, r: redis.StrictRedis, client: APIClient):
        self.redis = r
        self.client = client

    def subscribe(self):
        while True:
            try:
                for key in self.__get_keys():
                    data = self.__get(key)
                    self.client.save({'id': key, **data})
            except Exception as e:
                print(e)
            finally:
                time.sleep(LOOP_INTERVAL)

    def __get(self, key):
        data = json.loads(self.redis.get(key).decode('utf-8'))
        self.redis.delete(key)
        return data

    def __get_keys(self):
        return [key.decode('utf-8') for key in self.redis.scan_iter()]

    @classmethod
    def create(cls):
        pool = redis.ConnectionPool(
            host=os.environ.get('REDIS_HOST') or 'localhost',
            port=int(os.environ.get('REDIS_PORT') or '6379'),
            db=0)
        api_client = APIClient()
        return cls(redis.StrictRedis(connection_pool=pool), api_client)


if __name__ == '__main__':
    print(' === start subscriber === ')
    subscriber = Subscriber.create()
    subscriber.subscribe()
