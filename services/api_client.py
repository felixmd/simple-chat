# services/api_client.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Generator, Optional, Callable
from openai import OpenAI
from .rate_limiter import RateLimiter
from models import Message

@dataclass
class ChatAPIConfig:
    api_key: str
    base_url: str
    models: list[str]
    tokens_per_minute: int = 60
    max_tokens: int = 60
    default_params: Dict = field(default_factory=lambda: {
    })

class ChatAPIClient:
    def __init__(self, config: ChatAPIConfig):
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        self.config = config
        self.rate_limiter = RateLimiter(
            tokens_per_minute=config.tokens_per_minute,
            max_tokens=config.max_tokens
        )

    def generate_stream_response(
        self,
        messages: List[Message],
        model: str,  # This is the display name
        progress_callback: Optional[Callable[[float, float], None]] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        # Get the actual model name from config
        actual_model = self.config.models[0]  # Use the configured model name
        
        if not self.rate_limiter.wait_for_token(progress_callback):
            yield "Rate limit exceeded. Please try again later."
            return

        try:
            formatted_messages = [msg.to_dict() for msg in messages]
            params = {**self.config.default_params, **kwargs}
            
            stream = self.client.chat.completions.create(
                model=actual_model,  # Use the actual model name here
                messages=formatted_messages,
                stream=True,
                **params
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"API Error for model {actual_model}: {error_msg}")  # For debugging
            yield error_msg

