from typing import Any


class DB:
    class Record:
        def __init__(self, key: str, value: Any):
            self.key = key
            self.value = value

    def __init__(self):
        self.store = {}

    def save(self, record: Record):
        self.store[record.key] = record.value
