import asyncio
import datetime
import random

from telethon import TelegramClient
from telethon import errors
from telethon import functions, types
import questionary

from report_text import generate_text

api_id = int(questionary.password("Api ID:").ask())
api_hash = questionary.password("Api hash:").ask()

client = TelegramClient("session_new", api_id, api_hash)
client.start()

print('Bot started')


async def main():
    number_of_channels_rep = 150

    telegram_list = open("telegram_db", "r").readlines()
    random.shuffle(telegram_list)

    for (i, telegram_channel) in enumerate(telegram_list[:number_of_channels_rep]):
        if "https://" in telegram_channel:
            telegram_channel = telegram_channel.split('/')[-1]
        elif '@' in telegram_channel:
            telegram_channel = telegram_channel[1:]
        print(f"{i + 1}. Reporting {telegram_channel.strip()}")
        try:
            result = await client(functions.account.ReportPeerRequest(
                peer=telegram_channel,
                reason=types.InputReportReasonSpam(),
                message=generate_text())
            )
            print(f"{telegram_channel.strip()} reported successfully" if result else f"{telegram_channel.strip()} failed to report")
        except ValueError:
            print("Channel not found")
        except errors.UsernameInvalidError:
            print("Nobody is using this username, or the username is unacceptable")
        except errors.FloodWaitError as e:
            seconds_left = e.seconds
            while seconds_left > 0:
                print("Flood wait error. Waiting for ", str(datetime.timedelta(seconds=seconds_left)))
                seconds_left -= 60
                await asyncio.sleep(60)

        await asyncio.sleep(10 + 2 * random.random())


with client:
    client.loop.run_until_complete(main())
