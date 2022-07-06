"""
MIT License

Copyright (c) 2022 DLCHAMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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

# Configure bot's gateway intents and instantiate the Interaction bot object
# add guild IDs into test_guilds to prevent global registration and instantly have commands
# working with guilds whose IDs are in this list (ex: test_guilds=[1234456789,54433635533,342234234344])
intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.InteractionBot(intents=intents, test_guilds=[])


# Begin bot event listeners
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
