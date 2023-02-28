import modules.hubbleTg as hubTg
import asyncio
from config import TOKEN
import multiprocessing

bot = hubTg.HubbleTg(TOKEN)

def processing_message(message: dict, bot) -> None:
    print(asyncio.run(bot.send_message(message['text'], message['chat']['id'], ['Кнопка 1', 'Кнопка 2'], False)))

def main_loop():
    while True:
        messages = asyncio.run(bot.get_messages())
        if messages['ok']:
            for message in messages['messages']:
                multiprocessing.Process(target=processing_message, args=(message, bot), name=f'''message: {message['message_id']}''').start()
                


if __name__ == '__main__':
    main_loop()