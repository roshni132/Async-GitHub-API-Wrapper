class APIError(Exception):
    """Base class for all GitHub API exceptions."""
    pass

class NotFoundError(APIError):
    """Raised when a resource (like a user or repo) is not found (404)."""
    pass

class RateLimitError(APIError):
    """Raised when the GitHub API rate limit is exceeded (429 or 403)."""
    pass

class ServerError(APIError):
    """Raised when GitHub's servers are down (500, 502, 503)."""
    pass