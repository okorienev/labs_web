from minio import Minio
from itertools import repeat


class MinioManager:
    def __init__(self, config):
        self._clients = iter(repeat(
            [Minio(node, config['access_key'], config['secret_key']) for node in config['nodes']]
        ))

    @property
    def client(self):
        return next(self._clients)
