# handlers/tiktok_handler.py

import re
from .base import *

class TikTokHandler(SocialHandler):
    _pattern = re.compile(r"(https?://)?(www\.)?tiktok\.com/")

    def is_url_valid(self, url: str) -> bool:
        return bool(self._pattern.search(url))

    def handle_url(self, url: str) -> List[str]:
        # Your real logic goes here
        return f"TikTok handled: {url}" if self.is_url_valid(url) else None