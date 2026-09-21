# Contributing to ARD Crawler

Thanks for contributing! This guide explains how to contribute to the ARD Crawler for ApexRegistry.

## How to contribute
1. Fork this repository.
2. Create a branch: `git checkout -b feat/your-feature-name`.
3. Make your changes (fetcher, validator, embedder, upsert, main).
4. Test locally with a Supabase/Postgres + pgvector database.
5. Open a Pull Request (PR) with a clear description of your changes.

## Code style
- Use clear, simple Python 3.9+ async code.
- Keep functions small and focused.
- Add docstrings to public functions.
- Log progress and errors clearly in main.py.

## Testing
- Validate against real ai-catalog.json files when possible.
- Ensure embeddings are 384‑dim and upserts succeed in agent_registry.

## License
By contributing, you agree that your contributions will be licensed under Apache-2.0.
