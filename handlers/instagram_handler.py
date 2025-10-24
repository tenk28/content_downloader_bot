# handlers/instagram_handler.py

import os
import re
import requests
from .base import *

RAPID_API_KEY = os.getenv('RAPID_API_KEY')

class InstagramHandler(SocialHandler):
    _pattern = re.compile(r"(https?://)?(www\.)?instagram\.com/")

    def is_url_valid(self, url: str) -> bool:
        return bool(self._pattern.search(url))

    def handle_url(self, url: str) -> List[str]:
        endpoint = 'https://instagram120.p.rapidapi.com/api/instagram/links'

        payload = { 'url': url }
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': 'instagram120.p.rapidapi.com',
            'Content-Type': 'application/json'
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            print(f"Could retrive url data: {response_json}")
            return None

        result: List[str] = []
        if isinstance(response_json, list) and response_json:
            for data in response_json:
                if isinstance(data, dict) and 'urls' in data:
                    data = data.get('urls')
                    if isinstance(data, list) and data:
                        data = data[0]
                        if isinstance(data, dict) and 'url' in data:
                            result.append(data.get('url'))

        return result
