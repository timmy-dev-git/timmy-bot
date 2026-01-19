import os
import discord
from typing import Awaitable, Callable, List

OnConnectFn             = Callable[[], Awaitable[None]]
OnDisconnectFn          = Callable[[], Awaitable[None]]
OnReadyFn               = Callable[[discord.Client], Awaitable[None]]

OnMessageFn             = Callable[[discord.Message], Awaitable[None]]
OnMessageEditFn         = Callable[[discord.Message, discord.Message], Awaitable[None]]
OnMessageDeleteFn       = Callable[[discord.Message], Awaitable[None]]
OnBulkMessageDeleteFn   = Callable[[List[discord.Message]], Awaitable[None]]

OnMemberJoinFn          = Callable[[discord.Member], Awaitable[None]]
OnMemberRemoveFn        = Callable[[discord.Member], Awaitable[None]]
OnMemberUpdateFn        = Callable[[discord.Member, discord.Member], Awaitable[None]]

OnVoiceStateUpdateFn    = Callable[[discord.Member, discord.VoiceState, discord.VoiceState], Awaitable[None]]

OnReactionFn            = Callable[[discord.Reaction, discord.User], Awaitable[None]]

OnChannelFn             = Callable[[discord.abc.GuildChannel], Awaitable[None]]
OnChannelUpdateFn       = Callable[[discord.abc.GuildChannel, discord.abc.GuildChannel], Awaitable[None]]

OnRoleFn                = Callable[[discord.Role], Awaitable[None]]
OnRoleUpdateFn          = Callable[[discord.Role, discord.Role], Awaitable[None]]

OnGuildFn               = Callable[[discord.Guild], Awaitable[None]]
OnGuildUpdateFn         = Callable[[discord.Guild, discord.Guild], Awaitable[None]]

OnBanFn                 = Callable[[discord.Guild, discord.User], Awaitable[None]]

class Event:
    def __init__(
        self,

        on_connect_fn            : OnConnectFn,
        on_disconnect_fn         : OnDisconnectFn,
        on_ready_fn              : OnReadyFn,

        on_message_fn            : OnMessageFn,
        on_message_edit_fn       : OnMessageEditFn,
        on_message_delete_fn     : OnMessageDeleteFn,
        on_bulk_message_delete_fn: OnBulkMessageDeleteFn,

        on_member_join_fn        : OnMemberJoinFn,
        on_member_remove_fn      : OnMemberRemoveFn,
        on_member_update_fn      : OnMemberUpdateFn,

        on_voice_state_update_fn : OnVoiceStateUpdateFn,

        on_reaction_add_fn       : OnReactionFn,
        on_reaction_remove_fn    : OnReactionFn,

        on_channel_create_fn     : OnChannelFn,
        on_channel_delete_fn     : OnChannelFn,
        on_channel_update_fn     : OnChannelUpdateFn,

        on_role_create_fn        : OnRoleFn,
        on_role_delete_fn        : OnRoleFn,
        on_role_update_fn        : OnRoleUpdateFn,

        on_guild_join_fn         : OnGuildFn,
        on_guild_remove_fn       : OnGuildFn,
        on_guild_update_fn       : OnGuildUpdateFn,

        on_member_ban_fn         : OnBanFn,
        on_member_unban_fn       : OnBanFn,
    ) -> None:

        intents = discord.Intents.default()
        intents.guilds           = True
        intents.members          = True
        intents.messages         = True
        intents.message_content  = True
        intents.voice_states     = True
        intents.reactions        = True
        intents.bans             = True

        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_connect():
            await on_connect_fn()

        @self.client.event
        async def on_disconnect():
            await on_disconnect_fn()

        @self.client.event
        async def on_ready():
            await on_ready_fn(self.client)

        @self.client.event
        async def on_message(message):
            await on_message_fn(message)

        @self.client.event
        async def on_message_edit(before, after):
            await on_message_edit_fn(before, after)

        @self.client.event
        async def on_message_delete(message):
            await on_message_delete_fn(message)

        @self.client.event
        async def on_bulk_message_delete(messages):
            await on_bulk_message_delete_fn(messages)

        @self.client.event
        async def on_member_join(member):
            await on_member_join_fn(member)

        @self.client.event
        async def on_member_remove(member):
            await on_member_remove_fn(member)

        @self.client.event
        async def on_member_update(before, after):
            await on_member_update_fn(before, after)

        @self.client.event
        async def on_voice_state_update(member, before, after):
            await on_voice_state_update_fn(member, before, after)

        @self.client.event
        async def on_reaction_add(reaction, user):
            await on_reaction_add_fn(reaction, user)

        @self.client.event
        async def on_reaction_remove(reaction, user):
            await on_reaction_remove_fn(reaction, user)

        @self.client.event
        async def on_guild_channel_create(channel):
            await on_channel_create_fn(channel)

        @self.client.event
        async def on_guild_channel_delete(channel):
            await on_channel_delete_fn(channel)

        @self.client.event
        async def on_guild_channel_update(before, after):
            await on_channel_update_fn(before, after)

        @self.client.event
        async def on_guild_role_create(role):
            await on_role_create_fn(role)

        @self.client.event
        async def on_guild_role_delete(role):
            await on_role_delete_fn(role)

        @self.client.event
        async def on_guild_role_update(before, after):
            await on_role_update_fn(before, after)

        @self.client.event
        async def on_guild_join(guild):
            await on_guild_join_fn(guild)

        @self.client.event
        async def on_guild_remove(guild):
            await on_guild_remove_fn(guild)

        @self.client.event
        async def on_guild_update(before, after):
            await on_guild_update_fn(before, after)

        @self.client.event
        async def on_member_ban(guild, user):
            await on_member_ban_fn(guild, user)

        @self.client.event
        async def on_member_unban(guild, user):
            await on_member_unban_fn(guild, user)

        self.client.run(os.environ["TOKEN"])