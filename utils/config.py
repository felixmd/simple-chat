# utils/config.py
import os
from typing import Dict, Any
from dotenv import load_dotenv
from services import ChatAPIClient, ChatAPIConfig

def load_api_keys() -> Dict[str, str]:
    """Load API keys from environment variables"""
    load_dotenv()
    return {
        "ChatGPT": os.getenv("OPENAI_API_KEY"),
        "ChatGPT-O1": os.getenv("OPENAI_API_KEY"),
        "DeepSeek": os.getenv("DEEPSEEK_API_KEY")
    }

def create_model_config() -> Dict[str, Dict[str, Any]]:
    """Create configuration for different models"""
    return {
        "ChatGPT": {
            "base_url": "https://api.openai.com/v1",
            "model": "chatgpt-4o-latest" 
        },
        "ChatGPT-O1": {
            "base_url": "https://api.openai.com/v1",
            "model": "o1-preview"
        },
        "DeepSeek": {
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat"
        }
    }


def create_api_client(model_name: str) -> ChatAPIClient:
    """Create API client with appropriate configuration"""
    model_config = create_model_config()[model_name]
    api_keys = load_api_keys()
    
    config = ChatAPIConfig(
        api_key=api_keys[model_name],
        base_url=model_config["base_url"],
        models=[model_config["model"]]  # This configures available models
    )
    
    return ChatAPIClient(config)
