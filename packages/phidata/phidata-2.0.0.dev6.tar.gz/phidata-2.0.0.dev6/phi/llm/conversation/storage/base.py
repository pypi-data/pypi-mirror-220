from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any


class ConversationStorage(ABC):
    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self, user_id: str) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    def upsert(
        self,
        user_id: str,
        user_persona: Optional[str] = None,
        user_data: Optional[Dict[str, Any]] = None,
        user_chat_history: Optional[List[Dict[str, Any]]] = None,
        llm_chat_history: Optional[List[Dict[str, Any]]] = None,
        usage_data: Optional[Dict[str, Any]] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def end(self, user_id: str) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

