import os
from dataclasses import dataclass
from datetime import datetime

import discord
from discord import Embed
from mcstatus import JavaServer
from mcstatus import motd
from mcstatus.motd.components import ParsedMotdComponent

SERVER_ADDRESS = os.environ["SERVER_ADDRESS"]


@dataclass
class ServerInfo:
    total_queries = 0
    successful_queries = 0

    address: str = SERVER_ADDRESS
    is_online: bool = False
    players: list[str] = None
    players_online: int = None
    max_players: int = None
    version: str = None
    motd: str = None

    def get_uptime(self) -> float:
        return self.successful_queries / self.total_queries if self.total_queries else 0

    def to_embed(self) -> Embed:
        if self.is_online:
            embed = Embed(color=discord.Color.green())
        else:
            embed = Embed(color=discord.Color.red())

        embed.title = "Server status"
        embed.add_field(name="Address", value=f"```{self.address}```", inline=False)
        embed.set_footer(text=f"{self.get_uptime():.2%} uptime")
        embed.timestamp = datetime.now()

        if not self.is_online:
            embed.add_field(name="Status", value="Server is unreachable", inline=False)
            return embed

        embed.add_field(name="Version", value=self.version, inline=True)
        embed.add_field(name="Status", value="Online", inline=True)
        embed.add_field(
            name="Players",
            value=f"{self.players_online}/{self.max_players}",
            inline=True,
        )
        embed.add_field(name="Message of the day", value=self.motd, inline=False)
        if self.players:
            embed.add_field(
                name="Player list", value="\n".join(self.players), inline=False
            )

        return embed


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
    ServerInfo.total_queries += 1

    try:
        query = server.query()
        status = server.status()
        ServerInfo.successful_queries += 1

        return ServerInfo(
            is_online=True,
            players=query.players.names,
            players_online=query.players.online,
            max_players=query.players.max,
            version=status.version.name,
            motd=to_markdown(status.motd.parsed),
        )
    except Exception:
        return ServerInfo(is_online=False)


if __name__ == "__main__":
    query_server()
