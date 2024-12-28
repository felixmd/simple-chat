# services/rate_limiter.py
from dataclasses import dataclass, field
from time import time, sleep
from typing import Optional, Callable

@dataclass
class RateLimiter:
    tokens_per_minute: int
    max_tokens: int
    max_wait_seconds: int = 30
    tokens: float = field(init=False)
    last_update: float = field(init=False)

    def __post_init__(self):
        self.tokens = self.max_tokens
        self.last_update = time()

    def wait_for_token(self, progress_callback: Optional[Callable[[float, float], None]] = None) -> bool:
        start_time = time()
        while True:
            elapsed = time() - start_time
            if elapsed >= self.max_wait_seconds:
                return False

            self._update_tokens()
            if self.tokens >= 1:
                self.tokens -= 1
                return True

            if progress_callback:
                remaining = self.time_until_next_token()
                progress_callback(elapsed, remaining)
            
            sleep(0.1)

    def _update_tokens(self):
        now = time()
        elapsed = now - self.last_update
        new_tokens = elapsed * (self.tokens_per_minute / 60.0)
        self.tokens = min(self.max_tokens, self.tokens + new_tokens)
        self.last_update = now

    def time_until_next_token(self) -> float:
        self._update_tokens()
        if self.tokens >= 1:
            return 0
        return (1 - self.tokens) * (60.0 / self.tokens_per_minute)
