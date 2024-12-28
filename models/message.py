# models/message.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class Message:
    content: str
    role: Role
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Optional[dict] = None  # For any additional message-specific data

    def to_dict(self) -> dict:
        """Convert message to dictionary format for API calls"""
        return {
            "role": self.role.value,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        """Create a Message instance from a dictionary"""
        return cls(
            content=data["content"],
            role=Role(data["role"]),
            metadata=data.get("metadata")
        )
