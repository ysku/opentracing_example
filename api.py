import os

from opentracing import Format
from opentracing.ext import tags as ext_tags
from flask import Flask, request, jsonify

from app.config import ENV
from app.tracer import tracer
from app.queue import Queue
from app.db import DB
from app.uploader import Uploader
from app.publisher import Publisher

api = Flask(__name__)
uploader = Uploader()
publisher = Publisher(Queue.create())
db = DB()


@api.route('/upload/<identifier>', methods=['POST'])
def upload(identifier: str):
    with tracer.start_active_span('upload') as scope:
        scope.span.set_tag('env', ENV)
        scope.span.set_tag(ext_tags.SAMPLING_PRIORITY, 1)

        uploader.upload()

        value = {}
        tracer.inject(scope.span, Format.TEXT_MAP, value)
        message = Publisher.Message(key=identifier, value=value)
        publisher.publish(message)

        return jsonify({'message': 'ok'})


@api.route('/save/<identifier>', methods=['POST'])
def save(identifier: str):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    with tracer.start_active_span('api save', child_of=span_ctx) as scope:
        scope.span.set_tag('env', ENV)
        scope.span.set_tag(ext_tags.SAMPLING_PRIORITY, 1)

        data = request.get_json()
        db.save(DB.Record(key=identifier, value=data))
        return jsonify({'message': 'ok'})


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=os.environ.get('API_PORT', '50001'))
