import requests


class APIClient:
    def __init__(self, protocol='http', host=None, port=None):
        if host is None:
            raise ValueError()
        if port is None:
            raise ValueError()
        self.base_url = f'{protocol}://{host}:{port}'

    def save(self, identifier: str, headers=None, payload=None):
        if headers is None:
            headers = {}
        if payload is None:
            payload = {}

        res = requests.post(f'{self.base_url}/save/{identifier}', headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
