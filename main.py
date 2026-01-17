import os
import discord

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(os.environ["TOKEN"])
