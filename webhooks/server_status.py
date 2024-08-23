import os
from dataclasses import dataclass

from mcstatus import JavaServer

SERVER_ADDRESS = os.environ["SERVER_ADDRESS"]


@dataclass
class ServerInfo:
    address: str = SERVER_ADDRESS
    is_online: bool = False
    players: list[str] = None
    players_online: int = None
    max_players: int = None
    version: str = None
    motd: str = None



def query_server() -> ServerInfo:
    server = JavaServer.lookup(SERVER_ADDRESS)

    try:
        query = server.query()
        status = server.status()

        return ServerInfo(
            players=query.players.names,
            players_online=query.players.online,
            max_players=query.players.max,
            version=status.version.name,
            motd=status.motd.to_plain(),
        )
    except TimeoutError:
        return ServerInfo(is_online=False)


if __name__ == "__main__":
    query_server()
