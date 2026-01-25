from asyncio.tasks import sleep
from Commands      import Commands
from Client        import Client
from Reminders     import Reminders

def main():
    client   : Client    = Client   ()
    reminders: Reminders = Reminders()
    commands : Commands  = Commands (client, reminders)

    async def background_loop():
        while (True):
            if client.is_ready():
                await reminders.Update(client)

            await sleep(1)

    client.Start(background_loop)

if __name__ == "__main__":
    main()