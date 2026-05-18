import requests
import os
from django.conf import settings
from pathlib import Path

class VKClient:
    def __init__(self):
        self.token = settings.VK_TOKEN
        self.api_version = '5.131'
        self.base_url = 'https://api.vk.com/method'

    def _request(self, method, params=None):
        if params is None:
            params = {}
        params['access_token'] = self.token
        params['v'] = self.api_version
        response = requests.post(f"{self.base_url}/{method}", data=params)
        return response.json()

    def send_message(self, user_id, text, keyboard=None):
        params = {
            'user_id': user_id,
            'message': text,
            'random_id': 0
        }
        if keyboard:
            params['keyboard'] = keyboard
            
        return self._request('messages.send', params)

    def download_file(self, url, filename):
        save_path = settings.MEDIA_ROOT / 'layouts'
        save_path.mkdir(parents=True, exist_ok=True)
        full_path = save_path / filename
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return str(full_path.relative_to(settings.MEDIA_ROOT))
        return None
