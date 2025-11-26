# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and this project adheres to Semantic Versioning.

## [Unreleased]

- Ongoing work: implement fetchers, summarizer, ranker, composer, sender, and scheduling.

## [0.1.0] - 2025-11-26
### Added
- Initial project scaffold and planning documents:
  - `BRIEF.md` — project brief and sample HTML email content
  - `SOURCES.md` — curated sources and pipeline outline
  - `PLAN.md` — project plan and pipeline overview
  - `TODO.md` — task list with current statuses
  - `project.json` — machine-friendly project manifest (conforms to referenced schema)
  - `CHANGELOG.md` — this file

### Notes
- First commit captures planning and manifest creation. Next steps: confirm LLM provider and email delivery method, create config and skeleton fetchers, and implement extraction + summarization.

---

### How to use
- Add new changes under the `Unreleased` section as work progresses.
- When cutting a release, move `Unreleased` changes into a new version section with the release date.
- Follow Semantic Versioning for release numbering.
