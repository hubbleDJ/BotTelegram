import modules.HubbleTg as hubTg
import asyncio
from config import TOKEN

bot = hubTg.HubbleTg(TOKEN)

while True:
    messages = asyncio.run(bot.get_messages())
    if messages['ok']:
        for message in messages['messages']:
            print(asyncio.run(bot.send_message(message['text'], message['chat']['id'], [])))