import asyncio
import os
from dotenv import load_dotenv
from async_github.client import GitHubAPI
from async_github.exceptions import APIError

# Load environment variables from the .env file into memory
load_dotenv() 

async def main():
    # Retrieve the token securely from environment variables
    token = os.getenv("GITHUB_TOKEN")
    
    # Validate that the token was successfully loaded
    if not token:
        print("Error: GITHUB_TOKEN not found. Please ensure your .env file is configured correctly.")
        return

    try:
        # Using the async context manager to handle the session lifecycle
        async with GitHubAPI(token) as api:
            
            print("--- Fetching User Data ---")
            user_data = await api.get_user("torvalds")
            print(f"Name: {user_data.get('name')}")
            print(f"Followers: {user_data.get('followers')}\n")

            print("--- Fetching User Repositories (Paginated) ---")
            repo_count = 0
            
            # Asynchronously iterate over the paginated repository results
            async for repo in api.get_repos("torvalds"):
                print(f"- {repo['name']} (Stars: {repo['stargazers_count']})")
                repo_count += 1
                
                # Limit the output to 5 repositories for testing purposes
                if repo_count >= 5:
                    break

    except APIError as e:
        print(f"An API Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())