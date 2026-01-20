from asyncio import sleep
import os
import time
import discord
from typing import List
from Client import Client

# Starting/Stopping.
async def on_connect() -> None:
    print("Connected to Discord API.")

async def on_disconnect() -> None:
    print("Disconnected from Discord API.")

async def on_ready(client: discord.Client) -> None:
    print("Started bot:")
    if client.user:
        print(f"  ID:      {client.user.id}")
        print(f"  Name:    {client.user.name}")
        print(f"  Mention: {client.user.mention}")

# Messages.
async def on_message(message: discord.Message) -> None:
    print("Message sent:")
    print(f"  Author:  {message.author}")
    print(f"  Channel: {message.channel}")
    print(f"  Content: {message.content}")

async def on_message_edit(before: discord.Message, after: discord.Message) -> None:
    print("Message edited:")
    print(f"  Author: {after.author}")
    print(f"  Before: {before.content}")
    print(f"  After:  {after.content}")

async def on_message_delete(message: discord.Message) -> None:
    print("Message deleted:")
    print(f"  Author:  {message.author}")
    print(f"  Channel: {message.channel}")
    print(f"  Content: {message.content}")

async def on_bulk_message_delete(messages: List[discord.Message]) -> None:
    print(f"Bulk message delete: {len(messages)} messages")
    for msg in messages:
        await on_message(msg)

# Members.
async def on_member_join(member: discord.Member) -> None:
    print("Member joined:")
    print(f"  ID:      {member.id}")
    print(f"  Name:    {member.name}")
    print(f"  Mention: {member.mention}")

async def on_member_remove(member: discord.Member) -> None:
    print("Member left:")
    print(f"  ID:      {member.id}")
    print(f"  Name:    {member.name}")
    print(f"  Mention: {member.mention}")

    user_dir: str = os.path.join("data/users/", str(member.id))
    if os.path.exists(user_dir):
        os.remove(user_dir)

async def on_member_update(before: discord.Member, after: discord.Member) -> None:
    print("Member updated:")
    print(f"  User: {after}")
    if before.nick != after.nick:
        print(f"  Nick: {before.nick} -> {after.nick}")
    if before.roles != after.roles:
        print("  Roles changed")

# Voice.
async def on_voice_state_update(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    print("Voice state changed:")
    print(f"  User:   {member.name}")
    print(f"  ID:     {member.id}")
    print(f"  Before: {before.channel}")
    print(f"  After:  {after.channel}")

# Reactions.
async def on_reaction_add(
    reaction: discord.Reaction,
    user: discord.User,
) -> None:
    print("Reaction added:")
    print(f"  User:    {user}")
    print(f"  Emoji:   {reaction.emoji}")
    print(f"  Message: {reaction.message.id}")

async def on_reaction_remove(
    reaction: discord.Reaction,
    user: discord.User,
) -> None:
    print("Reaction removed:")
    print(f"  User:  {user}")
    print(f"  Emoji: {reaction.emoji}")

# Channels.
async def on_guild_channel_create(channel: discord.abc.GuildChannel) -> None:
    print("Channel created:")
    print(f"  Name: {channel.name}")
    print(f"  ID:   {channel.id}")

async def on_guild_channel_delete(channel: discord.abc.GuildChannel) -> None:
    print("Channel deleted:")
    print(f"  Name: {channel.name}")
    print(f"  ID:   {channel.id}")

async def on_guild_channel_update(
    before: discord.abc.GuildChannel,
    after: discord.abc.GuildChannel,
) -> None:
    print("Channel updated:")
    print(f"  Before: {before.name}")
    print(f"  After:  {after.name}")

# Roles.
async def on_guild_role_create(role: discord.Role) -> None:
    print("Role created:")
    print(f"  Name: {role.name}")
    print(f"  ID:   {role.id}")

async def on_guild_role_delete(role: discord.Role) -> None:
    print("Role deleted:")
    print(f"  Name: {role.name}")
    print(f"  ID:   {role.id}")

async def on_guild_role_update(before: discord.Role, after: discord.Role) -> None:
    print("Role updated:")
    print(f"  Before: {before.name}")
    print(f"  After:  {after.name}")

# Guilds.
async def on_guild_join(guild: discord.Guild) -> None:
    print("Joined guild:")
    print(f"  Name: {guild.name}")
    print(f"  ID:   {guild.id}")

async def on_guild_remove(guild: discord.Guild) -> None:
    print("Left guild:")
    print(f"  Name: {guild.name}")
    print(f"  ID:   {guild.id}")

async def on_guild_update(before: discord.Guild, after: discord.Guild) -> None:
    print("Guild updated:")
    print(f"  Before: {before.name}")
    print(f"  After:  {after.name}")

# Moderation.
async def on_member_ban(
    guild: discord.Guild,
    user: discord.User,
) -> None:
    print("Member banned:")
    print(f"  Guild: {guild.name}")
    print(f"  User:  {user}")

async def on_member_unban(
    guild: discord.Guild,
    user: discord.User,
) -> None:
    print("Member unbanned:")
    print(f"  Guild: {guild.name}")
    print(f"  User:  {user}")

async def BackgroundProcess(
) -> None:
    print("Started!")
    _i: int = 0
    while(True):
        print(f"{time.time()}")
        _i += 1
        await sleep(1)


Client(
    on_connect_fn             = on_connect,
    on_disconnect_fn          = on_disconnect,
    on_ready_fn               = on_ready,

    on_message_fn             = on_message,
    on_message_edit_fn        = on_message_edit,
    on_message_delete_fn      = on_message_delete,
    on_bulk_message_delete_fn = on_bulk_message_delete,

    on_member_join_fn         = on_member_join,
    on_member_remove_fn       = on_member_remove,
    on_member_update_fn       = on_member_update,

    on_voice_state_update_fn  = on_voice_state_update,

    on_reaction_add_fn        = on_reaction_add,
    on_reaction_remove_fn     = on_reaction_remove,

    on_channel_create_fn      = on_guild_channel_create,
    on_channel_delete_fn      = on_guild_channel_delete,
    on_channel_update_fn      = on_guild_channel_update,

    on_role_create_fn         = on_guild_role_create,
    on_role_delete_fn         = on_guild_role_delete,
    on_role_update_fn         = on_guild_role_update,

    on_guild_join_fn          = on_guild_join,
    on_guild_remove_fn        = on_guild_remove,
    on_guild_update_fn        = on_guild_update,

    on_member_ban_fn          = on_member_ban,
    on_member_unban_fn        = on_member_unban,

    background_process        = BackgroundProcess,
)