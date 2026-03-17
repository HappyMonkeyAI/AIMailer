# Codebase Insight: Django Web Control Panel

## Overview
A web-based administrative layer to transition the project from rigid CLI/Cron management to a dynamic UI.

## Architecture
- **Framework**: Django 4.2 + Django REST Framework.
- **Authentication**: Custom `email`-based auth using `CustomUser` and `CustomUserManager`.
- **Admin Extensions**: Custom CSS and JS in `web/static/` to enhance the Newsletter management experience (e.g., interactive keyword chips).

## Key Components
- **`accounts/`**: Handles user lifecycle, staff flags, and superuser resets.
- **`newsletters/`**: Manages the CRUD logic for newsletter streams, subscribers, and source mappings.
- **Management Commands**:
    - `reset_admin`: Essential for recovering access in Dockerized environments without interactive shell access.

## Hidden Knowledge
- **Static File Recovery**: Some static assets were historically lost in PR merges; current versions in `web/static/` are the source of truth recreated from `master`.
- **Docker Sync**: The web app runs in `aimailer-web-1`. Changes to local `web/` are synced via volumes but may require `collectstatic` if CSS/JS changes significantly.
