import json
import requests

class HubbleTg:
    """Взаимодействие с API телеграм бота"""
    
    def __init__(self, token: str) -> None:
        """Инициализирует создание объекта телеграм бота"""
        
        self.token = token
        self.update_id = 0
        
    def get_messages(self) -> dict:
        """Получает непрочитанные сообщения"""
        
        answer = {
            'ok': False,
            'messages': [],
            'error': None
        }
        
        try:
            response = json.loads(requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates',
                headers={"Content-Type": "application/json"},
                data=json.dumps({'offset': self.update_id})
            ).text)
            
            if 'ok' in response:
                answer['ok'] = response['ok']
                
            if 'ok' in response and response['ok'] and 'result' in response:
                for result in response['result']:
                    if 'update_id' in result and int(result['update_id']) >= self.update_id:
                        self.update_id = int(result['update_id']) + 1
                        
                    if 'message' in result:
                        answer['messages'].append(result['message'])
                        
        except Exception as error:
            answer['error'] = str(error)
            
        return answer