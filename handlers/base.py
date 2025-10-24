# handlers/base.py

from abc import ABC, abstractmethod
from typing import List

__all__ = [
    'SocialHandler',
    'List'
]

class SocialHandler(ABC):
    @abstractmethod
    def is_url_valid(self, url: str) -> bool:
        pass

    @abstractmethod
    def handle_url(self, url: str) -> List[str]:
        pass
