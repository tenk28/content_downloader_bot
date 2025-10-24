import re
from .base import *

class YouTubeHandler(SocialHandler):
    _pattern = re.compile(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/")

    def is_url_valid(self, url: str) -> bool:
        return bool(self._pattern.search(url))

    def handle_url(self, url: str) -> List[str]:
        return f"YouTube handled: {url}" if self.is_url_valid(url) else None
