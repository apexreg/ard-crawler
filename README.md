# ARD Crawler — Agentic Resource Discovery crawler for ApexRegistry

Automatically discovers AI agents by fetching `ai-catalog.json` manifests from domains and GitHub,
validates them against the ARD spec, embeds their capabilities, and upserts into the ApexRegistry pgvector database.

## What it does
- Fetches `https://domain/.well-known/ai-catalog.json` and GitHub raw ARD manifests
- Validates entries against the ARD schema
- Computes embeddings for capabilities_text (all‑MiniLM‑L6‑v2, 384‑dim)
- Upserts agent profiles into the `agent_registry` table (pgvector)

## Target environment
- Database: Supabase (Postgres + pgvector) or any Postgres with pgvector
- Embedding model: all‑MiniLM‑L6‑v2 (384‑dim) via sentence-transformers
- Runtime: Python 3.9+ async worker (can run in Docker)

## Quick start
1) Set environment variables:
   - DATABASE_URL=your_supabase_postgres_url
2) (Optional) Configure seeds:
   - config/seed_domains.txt
   - config/seed_github_repos.txt
3) Run locally:
   - `python -m crawler.main`
4) Or run in Docker:
   - `docker build -t apexreg/ard-crawler .`
   - `docker run --env DATABASE_URL=... apexreg/ard-crawler`

## Architecture
- fetcher.py: HTTP fetch with retries and rate limiting
- validator.py: JSON Schema validation for ARD manifests
- embedder.py: text → 384‑dim embeddings
- upsert.py: write to agent_registry (Supabase/pgvector)
- main.py: async entrypoint orchestrating the pipeline

## License
Apache‑2.0
