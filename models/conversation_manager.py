# models/conversation_manager.py
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple
from .conversation import Conversation

@dataclass
class ConversationManager:
    conversations: Dict[str, Conversation] = field(default_factory=dict)
    active_conversation_id: Optional[str] = None

    def create_conversation(self, model_name: str) -> Conversation:
        """Create a new conversation and set it as active"""
        try:
            conversation = Conversation(selected_model=model_name)
            self.conversations[conversation.id] = conversation
            self.active_conversation_id = conversation.id
            return conversation
        except Exception as e:
            raise Exception(f"Failed to create conversation: {str(e)}")

    def get_active_conversation(self) -> Optional[Conversation]:
        """Get the currently active conversation"""
        if self.active_conversation_id is None:
            return None
        return self.conversations.get(self.active_conversation_id)

    def switch_conversation(self, conversation_id: str) -> bool:
        """Switch to a different conversation"""
        if conversation_id not in self.conversations:
            return False
        self.active_conversation_id = conversation_id
        return True

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id not in self.conversations:
            return False
        del self.conversations[conversation_id]
        if self.active_conversation_id == conversation_id:
            self.active_conversation_id = None
        return True

    def list_conversations(self) -> List[Tuple[str, str, int]]:
        """Returns list of (id, model, message_count) for all conversations"""
        return [
            (id, conv.selected_model, conv.get_message_count())
            for id, conv in self.conversations.items()
        ]
