from abc import ABC, abstractmethod
from typing import Any, Dict

VERSION_LATEST = "latest"


class ConfigStorage(ABC):
    @abstractmethod
    def get(self, version: str = VERSION_LATEST) -> Dict[str, Any]:
        """returns configuration of the version"""
