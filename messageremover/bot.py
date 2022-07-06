from sys import version as py_version
from typing import List, Optional

from disnake import (
    ApplicationCommandInteraction,
    Embed,
    Intents,
    Member,
    Message,
    TextChannel,
)
from disnake import __version__ as disnake_version
from disnake.ext import commands

from messageremover import __version__ as bot_version

bot = commands.InteractionBot(intents=Intents.all(), test_guilds=[947543739671412878])


@bot.listen()
async def on_ready():
    """Invoked when the bot is ready"""
    print(
        "\n------------------------------\n"
        f"{bot.user} has successfully connected to Discord\n"
        f"Python Version: {py_version}\n"
        f"Disnake Version: {disnake_version}\n"
        f"Bot Version: {bot_version}\n"
        "------------------------------"
    )


@bot.slash_command(name="purge")
@commands.default_member_permissions(manage_messages=True)
async def purge_channel(
    interaction: ApplicationCommandInteraction,
    channel: Optional[TextChannel] = None,
    with_terms: Optional[str] = None,
    without_terms: Optional[str] = None,
    limit: Optional[int] = 1,
    author: Optional[Member] = None,
) -> None:
    """
    Purge messages from an optional target channel with or without options.

    Parameters
    ----------
    channel: (Optional) Target channel to purge messages from
    with_terms: (Optional) Comma separated list of terms purged message should contain
    without_terms: (Optional) Comma separated list of terms purged messages should NOT contain
    limit: (Optional) Total number of messages to purge (default: 1)
    author: (Optional) Target messages by this author (member)
    """
    if with_terms and without_terms:
        return await interaction.response.send_message(
            f"You cannot use `with_terms` and `without_terms` in the same command",
            ephemeral=True,
        )

    if with_terms is None and without_terms is None:
        return await interaction.response.send_message(
            "You must include 'with_terms' or 'without_terms' for this command to work.",
            ephemeral=True,
        )

    channel: TextChannel = channel or interaction.channel
    embed: Embed = Embed(title="Deleted Messages")

    if with_terms:
        with_terms: List[str] = with_terms.lower().split(",")
        embed.add_field(name="With Terms", value=", ".join(with_terms), inline=False)

        def message_check(m: Message) -> bool:
            """custom message check"""
            if author is None:
                return any(word in m.content.lower() for word in with_terms)
            return (
                any(word in m.content.lower() for word in with_terms)
                and m.author == author
            )

    if without_terms:
        without_terms: List[str] = without_terms.lower().split(",")
        embed.add_field(
            name="Without Terms", value=", ".join(without_terms), inline=False
        )

        def message_check(m: Message) -> bool:
            """custom message check"""
            if author is None:
                return not all(word in m.content.lower() for word in without_terms)
            return (
                not all(word in m.content.lower() for word in without_terms)
                and m.author == author
            )

    deleted: List[Message] = await channel.purge(limit=limit, check=message_check)

    embed.add_field(
        name="Target Channel | Target Author",
        value=f"#{channel.name} | {str(author)}",
        inline=False,
    )

    embed.add_field(
        name="\u200b",
        value=f"{len(deleted)} messages matched the selected options",
        inline=False,
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)
