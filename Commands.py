from datetime  import datetime, timedelta, timezone
from discord   import Interaction, Member, app_commands, utils
from Formatter import format_message, format_time
from Client    import Client
from Data      import Data
from Reminders import Reminder, Reminders

async def send_message(interaction: Interaction, private: bool, title: str, description: str):
    await interaction.response.send_message(format_message(title, description), ephemeral=private)

class Commands():
    reminders: Reminders

    def __init__(self, client: Client, reminders: Reminders):
        self.reminders = reminders

        @client.tree.command(name="settings-color", description="Removes the previous color-role(s) and gives a new one.")
        @app_commands.describe(color="The role-color to be given.")
        @app_commands.choices(
            color=[
                app_commands.Choice(name="Red"   , value="red"   ),
                app_commands.Choice(name="Orange", value="orange"),
                app_commands.Choice(name="Yellow", value="yellow"),
                app_commands.Choice(name="Green" , value="green" ),
                app_commands.Choice(name="Blue"  , value="blue"  ),
                app_commands.Choice(name="Purple", value="purple"),
            ])
        async def settings_color(interaction: Interaction, color: str):
            # This bot does not work-in/use DMs, therefore the user left the server or the server was deleted, and no message should be sent.
            if interaction.guild is None or not isinstance(interaction.user, Member):
                return

            new_role = utils.get(interaction.guild.roles, name=color)
            if new_role is None:
                await send_message(
                    interaction,
                    True,
                    "Error:",
                    "Failed to find the role associated with that color. Please contact an admin to fix this."
                )
                return

            await interaction.user.remove_roles(
                *[role for role in interaction.user.roles if role.name in ["red","orange","yellow","green","blue","purple"]],
                reason="Previous color role(s) removed."
            )
            await interaction.user.add_roles(
                new_role,
                reason="New color role added."
            )

            await send_message(
                interaction,
                True,
                "Success:",
               f"{color} role color was applied."
            )

        @client.tree.command(name="settings-role", description="Gives a role that specifies what you do or what channels you want to see.")
        @app_commands.describe(role="The role to be given.")
        @app_commands.choices(
            role=[
                app_commands.Choice(name="Developer", value="dev"),
                app_commands.Choice(name="Artist"   , value="art"),
                app_commands.Choice(name="Musician" , value="sfx"),
            ])
        async def settings_role(interaction: Interaction, role: str):
            if interaction.guild is None or not isinstance(interaction.user, Member):
                return

            new_role = utils.get(interaction.guild.roles, name=role)
            if new_role is None:
                await send_message(
                    interaction,
                    True,
                    "Error:",
                    "Failed to find the role associated with that name. Please contact an admin to fix this."
                )
                return

            if new_role in interaction.user.roles:
                await interaction.user.remove_roles(
                    new_role,
                    reason="settings-role <role>: Role removed."
                )
                await send_message(
                    interaction,
                    True,
                    "Success:",
                   f"{role} role was removed."
                )
            else:
                await interaction.user.add_roles(
                    new_role,
                    reason="settings-role <role>: Role added."
                )
                await send_message(
                    interaction,
                    True,
                    "Success:",
                   f"{role} role was added."
                )


        @client.tree.command(name="reminder-offset", description="Offsets all new reminders based on your timezone.")
        @app_commands.describe(utc_offset="Your timezone relative to UTC in hours. Examples: -4, -1, 0, 7")
        async def reminder_offset(interaction: Interaction, utc_offset: int):
            Data(interaction.user.id, "offset").overwrite({ "offset": utc_offset })

            await send_message(
                interaction,
                True,
                "Success:",
               f"Offset was set to {utc_offset}hr from UTC."
            )

        @client.tree.command(name="reminder-add", description="Adds a new reminder relative to your timezone offset.")
        @app_commands.describe(
            description  = "A short or long description of what the reminder is for.",
            hour         = "The reminder's hour.",
            minute       = "The reminder's minute.",
            day          = "The reminder's day.",
            month        = "The reminder's month.",
            year         = "The reminder's year.",
            repeat_delay = "Whether or not the reminder will repeat, and how often, in days.")
        @app_commands.choices(
            repeat_delay = [
                app_commands.Choice(name="Never", value=0 ),
                app_commands.Choice(name="01"   , value=1 ),
                app_commands.Choice(name="02"   , value=2 ),
                app_commands.Choice(name="03"   , value=3 ),
                app_commands.Choice(name="04"   , value=4 ),
                app_commands.Choice(name="05"   , value=5 ),
                app_commands.Choice(name="06"   , value=6 ),
                app_commands.Choice(name="07"   , value=7 ),
                app_commands.Choice(name="08"   , value=8 ),
                app_commands.Choice(name="09"   , value=9 ),
                app_commands.Choice(name="10"   , value=10),
                app_commands.Choice(name="11"   , value=11),
                app_commands.Choice(name="12"   , value=12),
                app_commands.Choice(name="13"   , value=13),
                app_commands.Choice(name="14"   , value=14),
                app_commands.Choice(name="21"   , value=21),
                app_commands.Choice(name="28"   , value=28),
            ])
        async def reminder_add(
            interaction : Interaction,
            description : str,
            hour        : int,
            minute      : int,
            day         : int,
            month       : int,
            year        : int,
            repeat_delay: int):
            new_time = datetime(
                hour   = hour,
                minute = minute,
                day    = day   ,
                month  = month ,
                year   = year  ,
                tzinfo = timezone.utc
            ) - timedelta(hours=Data(interaction.user.id, "offset").read()["offset"])
            if new_time < datetime.now(timezone.utc):
                await send_message(
                    interaction,
                    True,
                    "Error:",
                    "The reminder must be past the current time."
                )
                return

            Data(interaction.user.id, "reminders").append( { str(new_time) : (repeat_delay, description) } )
            self.reminders.Add(Reminder(new_time, repeat_delay, description, interaction.user.id))

            if repeat_delay == 0:
                await send_message(
                    interaction,
                    True,
                    "Success:",
                   f"A reminder was created for {format_time(interaction.user.id, new_time)}."
                )
            else:
                await send_message(
                    interaction,
                    True,
                    "Success:",
                   f"A reminder was created for {format_time(interaction.user.id, new_time)}, which repeats every {repeat_delay} day(s)."
                )

        @client.event
        async def on_ready():
            # await client.tree.sync()
            print("ready")