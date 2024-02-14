# main.py

# dpy?
import discord
from discord.ext import commands
from lib import Database as Database
import os

DBC = Database.DatabaseConnector()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = "!",intents=intents)


@client.event
async def on_ready():
    print(f"logged in as {client.user.name}")
    for f in os.listdir("./cogs"):
	    if f.endswith(".py"):
		    await client.load_extension("cogs." + f[:-3])




Token = DBC.execute_query('SELECT Token FROM Auth LIMIT 1;')[0][0]
client.run(Token)
