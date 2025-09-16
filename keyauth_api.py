import os
from dataclasses import dataclass
import httpx
from dotenv import load_dotenv

load_dotenv()

@dataclass
class KeyAuthConfig:
    url: str
    seller_key: str
    default_expiry_days: int
    default_level: int

    @classmethod
    def from_env(cls) -> "KeyAuthConfig":
        return cls(
            url=os.getenv("KEYAUTH_SELLER_URL", "https://keyauth.win/api/seller/").strip(),
            seller_key=os.getenv("KEYAUTH_SELLER_KEY", "").strip(),
            default_expiry_days=int(os.getenv("KEYAUTH_DEFAULT_EXPIRY_DAYS", "30")),
            default_level=int(os.getenv("KEYAUTH_DEFAULT_LEVEL", "1")),
        )

class KeyAuthAPI:
    def __init__(self, cfg: KeyAuthConfig | None = None):
        self.cfg = cfg or KeyAuthConfig.from_env()
        if not self.cfg.seller_key:
            raise RuntimeError("KEYAUTH_SELLER_KEY não definido")

    async def request(self, params: dict) -> dict:
        form = {"sellerkey": self.cfg.seller_key, **params}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(self.cfg.url, data=form)
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return {"raw": r.text, "status_code": r.status_code}

    async def key_info(self, key: str) -> dict:
        return await self.request({"type": "keyinfo", "key": key, "format": "json"})

    async def create_keys(self, amount: int, expiry_days: int | None = None, level: int | None = None) -> dict:
        expiry = expiry_days if expiry_days is not None else self.cfg.default_expiry_days
        lvl = level if level is not None else self.cfg.default_level
        return await self.request({
            "type": "add",
            "expiry": expiry,
            "level": lvl,
            "amount": amount,
            "format": "json"
        })

    async def ban_key(self, key: str) -> dict:
        return await self.request({"type": "ban", "key": key, "format": "json"})

    async def unban_key(self, key: str) -> dict:
        return await self.request({"type": "unban", "key": key, "format": "json"})

    async def reset_key(self, key: str) -> dict:
        return await self.request({"type": "reset", "key": key, "format": "json"})

    async def delete_key(self, key: str) -> dict:
        return await self.request({"type": "del", "key": key, "format": "json"})