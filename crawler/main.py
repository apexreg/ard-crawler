from __future__ import annotations
import asyncio
import os
from pathlib import Path
from .fetcher import fetch_json
from .validator import validate_catalog
from .embedder import embed_text
from .upsert import upsert_agent

ROOT = Path(__file__).resolve().parent.parent
SEED_DOMAINS_FILE = ROOT / "config" / "seed_domains.txt"
SEED_GITHUB_FILE = ROOT / "config" / "seed_github_repos.txt"

def load_seeds(file_path: Path) -> list[str]:
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

async def crawl_domain(domain: str) -> None:
    url = f"https://{domain}/.well-known/ai-catalog.json"
    catalog = await fetch_json(url)
    if not catalog:
        print(f"[SKIP] No catalog at {url}")
        return
    ok, errors = validate_catalog(catalog)
    if not ok:
        print(f"[WARN] Invalid catalog for {domain}: {errors[:3]}")
    entries = catalog.get("entries", [])
    for entry in entries:
        name = entry.get("name", "")
        description = entry.get("description", "")
        if not name or not description:
            continue
        ans_address = f"agent://{domain}/{name.replace(' ', '-').lower()}"
        capabilities_text = f"{name}: {description}"
        embedding = embed_text(capabilities_text)
        public_key = f"pk_{domain}_{name.replace(' ', '_').lower()}"
        try:
            upsert_agent(
                ans_address=ans_address,
                domain=domain,
                capabilities_text=capabilities_text,
                embedding=embedding,
                public_key=public_key,
            )
            print(f"[OK] Upserted {ans_address}")
        except Exception as e:
            print(f"[ERR] Failed to upsert {ans_address}: {e}")

async def main() -> None:
    domains = load_seeds(SEED_DOMAINS_FILE)
    if not domains:
        print("No seed domains found in config/seed_domains.txt")
        return
    for domain in domains:
        print(f"[CRAWL] Processing {domain}")
        await crawl_domain(domain)

if __name__ == "__main__":
    asyncio.run(main())
