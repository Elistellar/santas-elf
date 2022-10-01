from json import load as json_load
from typing import Any

from .file_manager import path
from .log import log


class Config:
    
    file = "config.json"
    
    @classmethod
    def load(cls):
        try:
            with open(path(cls.file), "r", encoding="utf-8") as f:
                cls._data = json_load(f)
        except Exception as e:
            log.critical("Failed to load config file: " + str(e))
            exit(-1)
    
    def __class_getitem__(cls, key: str) -> Any:
        return cls._data.get(key)
