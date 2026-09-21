from __future__ import annotations
import os
import psycopg2
from typing import List, Optional

DATABASE_URL = os.environ.get("DATABASE_URL", "")

def upsert_agent(
    ans_address: str,
    domain: str,
    capabilities_text: str,
    embedding: List[float],
    public_key: str,
    verified_wallet: Optional[str] = None,
) -> None:
    """
    Upsert an agent profile into agent_registry (Supabase/pgvector).
    """
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set")

    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            upsert_sql = """
            INSERT INTO agent_registry (ans_address, domain, capabilities_text, embedding, verified_wallet, public_key)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (ans_address) DO UPDATE SET
                domain = EXCLUDED.domain,
                capabilities_text = EXCLUDED.capabilities_text,
                embedding = EXCLUDED.embedding,
                verified_wallet = EXCLUDED.verified_wallet,
                public_key = EXCLUDED.public_key,
                last_crawled = CURRENT_TIMESTAMP;
            """
            cur.execute(
                upsert_sql,
                (ans_address, domain, capabilities_text, embedding, verified_wallet, public_key),
            )
        conn.commit()
    finally:
        conn.close()
