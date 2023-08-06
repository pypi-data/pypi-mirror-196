import random
from typing import Awaitable, List

from asyncio_connection_pool import ConnectionStrategy

from ecmind_blue_client_asyncio.blue_client import BlueClient
from ecmind_blue_client_asyncio.blue_server_config import BlueServerConfig


class BlueConnectionStrategy(ConnectionStrategy[BlueClient]):
    def __init__(self, connection_string: str, appname: str, username: str, password: str, file_cache_byte_limit: int = 33554432):
        self.appname = appname
        self.username = username
        self.password = password
        self.file_cache_byte_limit = file_cache_byte_limit
        self.server_configs: List[BlueServerConfig] = []
        self.server_weights: List[int] = []

        server_strings = connection_string.split("#")
        for server_string in server_strings:
            server_config = BlueServerConfig(server_string)
            self.server_configs.append(server_config)
            self.server_weights.append(server_config.weight)

    async def make_connection(self) -> Awaitable[BlueClient]:
        server_config = random.choices(self.server_configs, self.server_weights, k=1)[0]
        return BlueClient(
            server_config.hostname, server_config.port, self.appname, self.username, self.password, self.file_cache_byte_limit
        )

    def connection_is_closed(self, conn: BlueClient) -> bool:
        if conn is None:
            return True
        else:
            return False

    async def close_connection(self, conn: BlueClient) -> None:
        conn.close()
