import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Storage(BaseStorage):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_path: str = "storage/user_data.json"):
        self.file_path = Path(file_path)
        self.data: Dict[str, Any] = {}
        self.refresh_data()

    def refresh_data(self) -> None:
        """Принудительно обновляет данные из файла"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.file_path.exists():
                with open(self.file_path, "w") as f:
                    json.dump({}, f)
                self.data = {}
                return

            if os.path.getsize(self.file_path) == 0:
                self.data = {}
                return

            with open(self.file_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f"Error loading storage: {e}")
            backup_path = self.file_path.with_suffix(".bak.json")
            self.file_path.rename(backup_path)
            logger.warning(f"Created backup of invalid storage: {backup_path}")
            self.data = {}
        except Exception as e:
            logger.error(f"Unexpected error loading storage: {e}")
            self.data = {}

    def _save_data(self) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving storage: {e}")

    # FSM методы
    async def set_state(self, key: StorageKey, state: Optional[str] = None) -> None:
        self.refresh_data()
        user_id = str(key.user_id)
        if user_id not in self.data:
            self.data[user_id] = {}

        state_str = state.state if state and hasattr(state, 'state') else state
        self.data[user_id]["state"] = state_str
        self._save_data()

    async def get_state(self, key: StorageKey) -> Optional[str]:
        self.refresh_data()
        user_id = str(key.user_id)
        return self.data.get(user_id, {}).get("state")

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        self.refresh_data()
        user_id = str(key.user_id)
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id]["data"] = data
        self._save_data()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        self.refresh_data()
        user_id = str(key.user_id)
        return self.data.get(user_id, {}).get("data", {})

    async def close(self) -> None:
        pass

    async def wait_closed(self) -> bool:
        return True

    def ban_user(self, user_id: int) -> None:
        self.refresh_data()
        user_id_str = str(user_id)
        if user_id_str in self.data:
            self.data[user_id_str]["is_banned"] = True
            self._save_data()

    def get_favorites(self, user_id: int) -> List[str]:
        self.refresh_data()
        user_id_str = str(user_id)
        favorites = self.data.get(user_id_str, {}).get("favorites", [])
        return favorites if isinstance(favorites, list) else []

    def add_favorite(self, user_id: int, crypto_id: str) -> None:
        self.refresh_data()
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {"favorites": []}
        if "favorites" not in self.data[user_id_str]:
            self.data[user_id_str]["favorites"] = []
        if crypto_id not in self.data[user_id_str]["favorites"]:
            self.data[user_id_str]["favorites"].append(crypto_id)
            self._save_data()

    def is_favorite(self, user_id: int, crypto_id: str) -> bool:
        self.refresh_data()
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            return False
        if "favorites" not in self.data[user_id_str]:
            return False
        return crypto_id in self.data[user_id_str]["favorites"]

    def remove_favorite(self, user_id: int, crypto_id: str) -> None:
        self.refresh_data()
        user_id_str = str(user_id)
        if user_id_str in self.data and "favorites" in self.data[user_id_str]:
            if crypto_id in self.data[user_id_str]["favorites"]:
                self.data[user_id_str]["favorites"].remove(crypto_id)
                self._save_data()

    def is_banned(self, user_id: int) -> bool:
        self.refresh_data()
        user_id_str = str(user_id)
        return self.data.get(user_id_str, {}).get("is_banned", False)