# models/conversation.py
from dataclasses import dataclass, field
from typing import List, Optional
import uuid
from .message import Message
from services.api_client import ChatAPIClient

@dataclass
class Conversation:
    selected_model: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = field(default_factory=list)
    api_client: Optional[ChatAPIClient] = None

    def __post_init__(self):
        if not self.api_client:
            from utils.config import create_api_client
            self.api_client = create_api_client(self.selected_model)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation"""
        self.messages.append(message)

    def clear_messages(self) -> None:
        """Clear all messages from the conversation"""
        self.messages.clear()

    def get_message_count(self) -> int:
        """Get the number of messages in the conversation"""
        return len(self.messages)
