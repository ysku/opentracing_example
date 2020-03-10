import os
import time

from opentracing.propagation import Format

from app.api_client import APIClient
from app.config import ENV
from app.tracer import tracer
from app.queue import Queue

LOOP_INTERVAL = int(os.environ.get('LOOP_INTERVAL') or 5)
API_HOST = os.environ.get('API_HOST') or 'localhost'
API_PORT = os.environ.get('API_PORT') or '50002'


class Subscriber:
    def __init__(self, q: Queue, client: APIClient):
        self.queue = q
        self.client = client

    def subscribe(self):
        while True:
            try:
                for key in self.queue.peek_all_keys():
                    value = self.queue.get(key)
                    span_ctx = tracer.extract(Format.TEXT_MAP, value)
                    with tracer.start_active_span('subscribe', child_of=span_ctx) as scope:
                        scope.span.set_tag('env', ENV)
                        print(f'subscriber: value = {value}')
                        tracer.inject(scope.span, Format.HTTP_HEADERS, value)
                        self.client.save(key, value)
            except Exception as e:
                print(e)
            finally:
                time.sleep(LOOP_INTERVAL)


if __name__ == '__main__':
    queue = Queue.create()
    api_client = APIClient(host=API_HOST, port=API_PORT)

    print(' === start subscriber === ')
    subscriber = Subscriber(queue, api_client)
    subscriber.subscribe()
