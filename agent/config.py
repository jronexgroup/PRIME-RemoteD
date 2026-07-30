import json
import os
from pathlib import Path


class Config:
    def __init__(self):
        self.device_id: str = "home-pc"
        self.device_name: str = "Office PC"
        self.api_key: str = ""
        self.backend_url: str = ""
        self._load()

    def _load(self):
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                data = json.load(f)
                self.device_id = data.get("device_id", self.device_id)
                self.device_name = data.get("device_name", self.device_name)
                self.api_key = data.get("api_key", self.api_key)
                self.backend_url = data.get("backend_url", self.backend_url)

    def save(self):
        config_path = Path(__file__).parent / "config.json"
        data = {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "api_key": self.api_key,
            "backend_url": self.backend_url,
        }
        with open(config_path, "w") as f:
            json.dump(data, f, indent=4)

    def validate(self) -> bool:
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.backend_url:
            raise ValueError("Backend URL is required")
        return True


config = Config()
