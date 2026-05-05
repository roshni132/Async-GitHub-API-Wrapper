# Async GitHub API Wrapper 🚀

A production-ready, highly efficient asynchronous Python wrapper for the GitHub API. Built using `aiohttp` and `asyncio`, this library provides a clean, object-oriented interface to interact with GitHub data safely and concurrently.

## ✨ Features

* **⚡ Asynchronous Design:** Fully non-blocking API calls using `aiohttp` for high-performance data retrieval.
* **🔁 Smart Pagination:** Built-in async generators (`Paginator`) to effortlessly stream large datasets (like user repositories) without exhausting system memory.
* **🛡️ Built-in Rate Limiting:** Implements a custom Token-Bucket decorator that monitors GitHub's `X-RateLimit` headers in real-time, automatically pausing requests to prevent 403/429 API bans.
* **🎯 Custom Exception Handling:** Clean and descriptive custom error classes (`NotFoundError`, `RateLimitError`, `ServerError`) for precise debugging.
* **🔒 Secure Authentication:** Strictly uses environment variables (`.env`) to prevent accidental token leaks.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/roshni132/Async-GitHub-API-Wrapper.git](https://github.com/roshni132/Async-GitHub-API-Wrapper.git)
   cd Async-GitHub-API-Wrapper
Install required dependencies:

Bash
pip install aiohttp python-dotenv
Configure your Environment:
Create a .env file in the root directory and add your GitHub Personal Access Token (PAT):

Code snippet
GITHUB_TOKEN=your_github_personal_access_token_here
💻 Quick Start Guide
Here is a simple example of how to use the library to fetch a user's profile and paginate through their repositories.

Python
import asyncio
import os
from dotenv import load_dotenv
from async_github.client import GitHubAPI

# Load the secret token securely
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

async def main():
    # Use the async context manager to handle the session safely
    async with GitHubAPI(TOKEN) as api:
        
        # 1. Fetch a User
        print("Fetching User Profile...")
        user = await api.get_user("torvalds")
        print(f"Name: {user.get('name')} | Followers: {user.get('followers')}\n")

        # 2. Stream Repositories (Handled Automatically by Paginator)
        print("Fetching Repositories...")
        async for repo in api.get_repos("torvalds"):
            print(f"- {repo['name']} (⭐ {repo['stargazers_count']})")

if __name__ == "__main__":
    asyncio.run(main())
📁 Project Structure
Plaintext
Async-GitHub-API-Wrapper/
├── async_github/
│   ├── __init__.py         # Package initialization
│   ├── client.py           # Core GitHubAPI client class
│   ├── exceptions.py       # Custom API error hierarchy
│   ├── pagination.py       # Async generator for data streaming
│   └── rate_limiter.py     # Token-bucket rate-limiting decorator
├── test_main.py            # Usage examples and testing script
├── .gitignore              # Security and cache exclusions
└── README.md               # Project documentation
