import os
import discord
import asyncio
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

BackgroundProcess       = Callable[[]]

async def BackgroundFuncs():
    pass

class Client:
    async def __init__(
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

        background_process       : BackgroundProcess,
    ) -> None:

        intents = discord.Intents.all()
        intents.presences = False
        client = discord.Client(intents=intents)

        await BackgroundFuncs()
        asyncio.create_task(BackgroundFuncs())

        async def main_loop():
            asyncio.create_task(background_process())
            try:
                await client.start(os.environ["TOKEN"])
            finally:
                await client.close()

        asyncio.run(main=main_loop())