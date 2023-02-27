import aiohttp
import random
import requests
import json

class HubbleTg:
    """Взаимодействие с API телеграм бота"""
    
    def __init__(self, token: str) -> None:
        """Инициализирует создание объекта телеграм бота"""
        
        self.token = token
        self.update_id = 0
        self.session_id = self.get_session_id()
        
        response = json.loads(requests.get(f'https://api.telegram.org/bot{token}/getMe').text)
        self.bot_id = response['result']['id']
        self.first_name = response['result']['first_name']
        self.username = response['result']['username']
        
    def get_session_id(self) -> str:
        """Генерирует session id"""
        
        symbols = ['A', 'E', 'I', 'O', 'U', 'Y', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        session_id = ''
        for i in range(0, 10):
            session_id += symbols[random.randint(0, len(symbols) - 1)]
        return session_id
        
    async def get_messages(self) -> dict:
        """Получает непрочитанные сообщения"""
        
        answer = {
            'ok': False,
            'messages': [],
            'description': None
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.telegram.org/bot{self.token}/getUpdates',
                                       params={'offset': self.update_id}) as resp:
                    response = await resp.json()

            if 'ok' in response:
                answer['ok'] = response['ok']
                
            if 'ok' in response and response['ok'] and 'result' in response:
                for result in response['result']:
                    if 'update_id' in result and int(result['update_id']) >= self.update_id:
                        self.update_id = int(result['update_id']) + 1
                        
                    if 'message' in result:
                        answer['messages'].append(result['message'])
                        
        except Exception as error:
            answer['description'] = str(error)
        return answer
    
    async def send_message(self, text: str, chat_id: int, buttons: list = [], drop_buttons: bool=True) -> dict:
        """Отправляет сообщение"""
        
        answer = {
            'status_code': None,
            'description': None
        }
        try:
            if text in [None, '']:
                answer['status_code'] = 204
                answer['description'] = 'Пустое сообщение'
                
            elif chat_id in [None, 0]:
                answer['status_code'] = 204
                answer['description'] = 'Пустой chat_id'
                
            else:
                payload = {
                    "chat_id": chat_id,
                    "text": text[:4095]
                }
                
                if buttons and len(buttons) != 0:
                    payload["reply_markup"] = {
                        "keyboard": [[{"text": text}] for text in buttons],
                        "remove_keyboard": True,
                        "resize_keyboard": True,
                        "one_time_keyboard": False
                    }
                elif drop_buttons:
                    payload["reply_markup"] = {
                        "remove_keyboard": True
                    }
                else:
                    payload["reply_markup"] = {
                        "remove_keyboard": False
                    }
                    
                async with aiohttp.ClientSession() as session:
                    async with session.post(f'https://api.telegram.org/bot{self.token}/sendMessage', json=payload) as resp:
                        answer['status_code'] = resp.status
        except Exception as error:
            answer['status_code'] = -1
            answer['description'] = str(error)
        return answer