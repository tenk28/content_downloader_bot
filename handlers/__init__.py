# handlers/__init__.py
from .base import SocialHandler
from .tiktok_handler import TikTokHandler
from .instagram_handler import InstagramHandler
from .youtube_handler import YouTubeHandler

__all__ = [
    "SocialHandler",
    "TikTokHandler",
    "InstagramHandler",
    "YouTubeHandler",
]
