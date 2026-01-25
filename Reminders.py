import os
from datetime import datetime, timedelta, timezone
from discord import Forbidden, User
from Client  import Client
from Data    import Data
from Formatter import format_message, format_time

class Reminder:
    def __init__(self, date: datetime, repeatDelay: int, description: str, id: int):
        self.date        = date
        self.repeatDelay = repeatDelay
        self.description = description
        self.id          = id

class Reminders:
    reminders: list[Reminder] = []

    def Add(self, reminder: Reminder):
        i = 0
        for i in range(len(self.reminders)):
            if self.reminders[i].date > reminder.date:
                break
        self.reminders.insert(i, reminder)

    def __init__(self):
        if not os.path.exists("data/users/"):
            return

        for entry in os.scandir("data/users/"):
            if entry.is_dir:
                if not os.path.exists(f"{entry.path}/reminders"):
                    continue


                id: int = int(entry.name)
                for key, value in Data(id, "reminders").read().items():
                    self.Add(Reminder(datetime.fromisoformat(key), value[0], value[1], id))

    async def Update(self, client: Client):
        if len(self.reminders) == 0:
            return

        if self.reminders[0].date < datetime.now(timezone.utc):
            reminder: Reminder = self.reminders.pop(0)
            user: User = await client.fetch_user(reminder.id)

            try:
                await user.send(format_message(f"Reminder -\n {format_time(reminder.id, reminder.date)}:", reminder.description))
            except Forbidden:
                return

            file: Data = Data(reminder.id, "reminders")
            data = file.read()
            data.pop(str(reminder.date), None)

            if reminder.repeatDelay != 0:
                reminder.date += timedelta(days=reminder.repeatDelay)
                self.reminders.append(reminder)
                data[str(reminder.date)] = (reminder.repeatDelay, reminder.description)

            file.overwrite(data)