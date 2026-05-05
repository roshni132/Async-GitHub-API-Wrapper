import time
import asyncio
from functools import wraps

def limits(calls: int, period: float):
    """
    A decorator that enforces API rate limits.
    It inspects the client's current rate limit state and pauses 
    execution if the available tokens have been exhausted.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Check if the API client has tracked rate limit properties
            if hasattr(self, 'rate_limit_remaining') and hasattr(self, 'rate_limit_reset'):
                
                # If we have 0 requests left, calculate how long to wait
                if self.rate_limit_remaining <= 0:
                    current_time = time.time()
                    wait_time = self.rate_limit_reset - current_time
                    
                    if wait_time > 0:
                        print(f"\n[Warning] API Rate Limit Exceeded.")
                        print(f"Automatically sleeping for {wait_time:.2f} seconds...")
                        await asyncio.sleep(wait_time)
                        print("[Info] Resuming operations...")

            # Proceed with the actual API request
            return await func(self, *args, **kwargs)
            
        return wrapper
    return decorator