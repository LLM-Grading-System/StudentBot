import json
import aiohttp
from abc import ABC, abstractmethod


class GitHubService(ABC):
    @abstractmethod
    async def is_verified(self, github_username: str, telegram_username: str) -> tuple[bool, str]:
        raise NotImplementedError


class HTTPGitHubService(GitHubService):
    async def is_verified(self, github_username: str, telegram_username: str) -> tuple[bool, str]:
        github_profile_social_accounts_link = f"https://api.github.com/users/{github_username}/social_accounts"
        telegram_profile_link = f"https://t.me/{telegram_username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(github_profile_social_accounts_link) as res:
                content = await res.text(encoding="utf-8")
                data = json.loads(content)
                for account in data:
                    actual_link = account["url"]
                    if telegram_profile_link == actual_link:
                        return True
        return False
