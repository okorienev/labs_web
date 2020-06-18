from minio import Minio
from itertools import cycle


class MinioManager:
    def __init__(self, config):
        self._clients = iter(cycle(
            Minio(node, config['access_key'], config['secret_key']) for node in config['nodes']
        ))

    @property
    def client(self) -> Minio:
        return next(self._clients)
