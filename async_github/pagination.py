from typing import AsyncGenerator, Dict, Any

class Paginator:
    def __init__(self, api_client, endpoint: str, params: Dict[str, Any] = None):
        self.api_client = api_client
        self.endpoint = endpoint
        self.params = params or {}
        self.page = 1
        self.params["per_page"] = 100 # Fetch max items per page

    async def get_all(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Async generator that yields individual items from paginated results."""
        while True:
            self.params["page"] = self.page
            data = await self.api_client._request("GET", self.endpoint, params=self.params)
            
            # If data is empty, we reached the end of the pages
            if not data:
                break
                
            for item in data:
                yield item
                
            self.page += 1