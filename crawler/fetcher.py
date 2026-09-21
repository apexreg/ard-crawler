from __future__ import annotations
import httpx
from typing import Optional

DEFAULT_TIMEOUT = 10.0
DEFAULT_RETRIES = 2

async def fetch_json(url: str, timeout: float = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> Optional[dict]:
    """
    Fetch JSON from a URL with retries and timeout.
    Returns None if the request fails after retries.
    """
    attempt = 0
    while attempt <= retries:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 404:
                    return None
                else:
                    # Non-200, non-404: retry
                    attempt += 1
                    continue
        except Exception:
            attempt += 1
            continue
    return None
