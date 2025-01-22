import json
import aiohttp
from abc import ABC, abstractmethod


class GitHubService(ABC):
    @abstractmethod
    async def is_verified(self, github_username: str, telegram_username: str) -> bool:
        raise NotImplementedError


class HTTPGitHubService(GitHubService):
    async def is_verified(self, github_username: str, telegram_username: str) -> bool:
        github_profile_link = f"https://api.github.com/users/{github_username}"
        telegram_profile_link = f"https://t.me/{telegram_username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(github_profile_link) as res:
                content = await res.text(encoding="utf-8")
                data = json.loads(content)
                if "blog" not in data:
                    return False
                actual_link = data["blog"]

        return actual_link == telegram_profile_link
