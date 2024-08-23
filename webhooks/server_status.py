import os
from dataclasses import dataclass

from mcstatus import JavaServer
from mcstatus import motd
from mcstatus.motd.components import ParsedMotdComponent

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


# Supported MOTD-to-Markdown formatters.
markdown_formatters = {
    motd.Formatting.ITALIC: "*",
    motd.Formatting.BOLD: "**",
    motd.Formatting.UNDERLINED: "__",
    motd.Formatting.STRIKETHROUGH: "~~",
}


def to_markdown(parsed: list[ParsedMotdComponent]) -> str:
    """Convert Minecraft MOTD components into Markdown formatted string."""
    md_text = []
    last_formatter = None

    for component in parsed:
        if type(component) is str:
            md_text.append(component)
            continue
        if formatter := markdown_formatters.get(component):
            md_text.append(formatter)
            last_formatter = component
            continue
        if component is motd.Formatting.RESET:
            md_text.append(markdown_formatters.get(last_formatter, ""))
            last_formatter = None
            continue
    if last_formatter:
        md_text.append(markdown_formatters.get(last_formatter, ""))

    return "".join(md_text)


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
