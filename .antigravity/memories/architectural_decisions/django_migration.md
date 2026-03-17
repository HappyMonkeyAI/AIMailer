# Architectural Decision: CLI to Django-Managed Web Control Panel

## Status
**Active** (Migration in progress/completed)

## Context
The project initially relied on local CLI scripts and cron jobs for all administrative tasks (e.g., source management, subscriber list maintenance). This created a high bar for entry and lacked a persistent, accessible administrative interface.

## Decision
Migrate administrative logic to a Django-based Web Control Panel. This involves creating a robust set of models to mirror the `config.py` logic and providing a DRF (Django REST Framework) API for future expansion.

## Tradeoffs
- **Pros**: Dynamic source management, simplified subscriber CRUD, centralized logging, and easier future scaling.
- **Cons**: Increased infrastructure complexity (Postgres, Redis, Docker), and the need for database migrations.

## Hidden Knowledge
- **Dual Flow**: The core AI pipeline remains decoupled from the Django app to ensure localized failures don't crash the entire mailing engine.
- **SQLite vs Postgres**: While SQLite is present for local development, the production system is strictly Dockerized Postgres.
