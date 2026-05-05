import aiohttp
import asyncio
import time
from typing import AsyncGenerator, Dict, Any

from .exceptions import APIError, NotFoundError, RateLimitError, ServerError
from .pagination import Paginator
from .rate_limiter import limits  # Import our new decorator

class GitHubAPI:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.token = token
        self.session = None
        
        # Initial safe assumptions for the token bucket
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = time.time() + 3600

    async def __aenter__(self):
        """Setup the aiohttp session when entering 'async with' block."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the session properly when exiting the block."""
        if self.session:
            await self.session.close()

    # Apply the rate limiter decorator to the main request pipeline
    @limits(calls=5000, period=3600)
    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Internal method to handle HTTP requests and errors."""
        url = f"{self.BASE_URL}/{endpoint}"
        
        async with self.session.request(method, url, **kwargs) as response:
            
            # 1. Update our internal token bucket from live GitHub headers
            if "X-RateLimit-Remaining" in response.headers:
                self.rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
                
            if "X-RateLimit-Reset" in response.headers:
                self.rate_limit_reset = float(response.headers["X-RateLimit-Reset"])

            # 2. Error Management Mapping
            if response.status == 404:
                raise NotFoundError(f"Resource not found: {url}")
            elif response.status in (403, 429):
                raise RateLimitError(f"Rate limit completely exhausted. Resets at {self.rate_limit_reset}")
            elif response.status >= 500:
                raise ServerError(f"GitHub server error: {response.status}")
            
            # 3. Return successfully parsed JSON data
            response.raise_for_status()
            return await response.json()

    # --- Public API Methods ---

    async def get_user(self, username: str) -> Dict[str, Any]:
        """Fetch a specific GitHub user profile."""
        return await self._request("GET", f"users/{username}")

    def get_repos(self, username: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Get all repositories for a user using the Paginator."""
        paginator = Paginator(self, f"users/{username}/repos")
        return paginator.get_all()