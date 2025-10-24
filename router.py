from typing import List, Optional

from handlers import *

class SocialRouter:
    def __init__(self, handlers: Optional[List[SocialHandler]] = None):
        if handlers is None:
            handlers = [TikTokHandler(), InstagramHandler(), YouTubeHandler()]
        self.handlers = handlers

    def handle(self, url: str) -> Optional[str]:
        for handler in self.handlers:
            if handler.is_url_valid(url):
                return handler.handle_url(url)
        return None
