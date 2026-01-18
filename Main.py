import os
import discord

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True   # REQUIRED to read message text
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (id={client.user.id})")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    print(
        f"Message | guild={message.guild.name if message.guild else 'DM'} "
        f"channel={message.channel} "
        f"user={message.author} "
        f"content='{message.content}'"
    )

@client.event
async def on_member_join(member):
    print(
        f"Member joined | guild={member.guild.name} "
        f"user={member} id={member.id}"
    )

@client.event
async def on_member_remove(member):
    print(
        f"Member left | guild={member.guild.name} "
        f"user={member} id={member.id}"
    )

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        print(
            f"Voice change | user={member} "
            f"from={before.channel} "
            f"to={after.channel}"
        )

client.run(os.environ["TOKEN"])