import json
import os
from typing import Dict, Optional, Union

from flask import Flask, request, jsonify
import redis


SERVICE_NAME = os.environ.get('SERVICE_NAME')
ENV = os.environ.get('STAGE')


class Message:
    def __init__(
            self,
            trace_id: Optional[str] = None,
            parent_id: Optional[str] = None,
            sampling_priority: Optional[int] = None):
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.sampling_priority = sampling_priority

    def asdict(self) -> Dict[str, Union[str, int, None]]:
        r = {}
        if self.trace_id:
            r['trace_id'] = self.trace_id
        if self.parent_id:
            r['parent_id'] = self.parent_id
        if self.sampling_priority:
            r['sampling_priority'] = self.sampling_priority
        return r


class Uploader:
    def upload(self):
        # TODO: implement
        print('not implemented yet')


class DB:
    def __init__(self):
        self.store = {}

    def save(self, id: str, record: dict):
        self.store[id] = {**record}


class Publisher:
    def __init__(self, r: redis.StrictRedis):
        self.redis = r

    def publish(self, id: str, message: Message):
        value = json.dumps(message.asdict())
        self.redis.set(id, value)

    @classmethod
    def create(cls):
        pool = redis.ConnectionPool(
            host=os.environ.get('REDIS_HOST') or 'localhost',
            port=int(os.environ.get('REDIS_PORT') or '6379'),
            db=0)
        return cls(redis.StrictRedis(connection_pool=pool))


api = Flask(__name__)
uploader = Uploader()
publisher = Publisher.create()
db = DB()


@api.route('/upload/<id>', methods=['POST'])
def upload(id: str):
    print('upload called')

    uploader.upload()

    message = Message()
    publisher.publish(id, message)

    return jsonify({
        'message': 'ok'
    })


@api.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    print(f'save called: {data}')

    id = data.pop('id')
    db.save(id, data)
    return jsonify({
        'message': 'ok'
    })


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=os.environ.get('API_PORT', '50001'))
