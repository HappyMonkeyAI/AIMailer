# Patterns & Lessons

## Success Patterns (Low Gravity)
- **[Success] Modular RSS Pipeline**: Decoupling fetching, extraction, and summarization allows each stage to be optimized independently.
- **[Success] `reset_admin` Command**: Providing an unambiguous management command for superuser management in Dockerized environments significantly reduces administrative "Drag".
- **[Success] Round-Robin Diversity**: Implementing a simple yet effective source diversity algorithm avoids content echo chambers.

## Failure Lessons (High Gravity)
- **[Failure] Undocumented Local Work**: Failing to sync local `db.sqlite3` with Dockerized Postgres led to out-of-sync configurations.
- **[Failure] Missing Static Assets**: Historical PR merges that deleted static files caused recurring UI breakage; moved to a policy of explicit static verification after every rebase.
- **[Failure] LLM Thinking Output**: Models outputting `<think>` blocks into emails caused "noisy" user experiences.
- **[Lesson Learned] Surgical Refactoring**: Large-scale changes to `AGENTS.md` should always be preceded by a handof/backup of existing context.
