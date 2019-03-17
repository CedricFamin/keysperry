from discord.ext import commands as discordcmd
import logging
import os
import commands
import events


logging.basicConfig(level=logging.INFO)

client = discordcmd.Bot(command_prefix=discordcmd.when_mentioned_or('$'))

commands.add_all_commands(client)
events.add_all_events(client)
client.run(os.getenv('KEYSPERRY_DISCORD_BOT_TOKEN'), bot=True)
