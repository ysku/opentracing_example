from app.queue import Queue


class Publisher:

    class Message:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self, q: Queue):
        self.queue = q

    def publish(self, message: Message):
        self.queue.put(message.key, message.value)
