# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `requirements.txt` / `requirements-dev.txt` with pinned runtime and dev dependencies.
- `pyproject.toml` (PEP 621) with build config, `aice` console entry point, and
  ruff / mypy / pytest / coverage configuration.
- `app_meta.py` as the single source of truth for app metadata and support links.
- `assets/` directory for bundled binary assets (sponsor QR).
- Generic extractors (`core/extractors/generic/`) so C/C++, "All Languages" and
  unmatched profiles no longer silently run the Python extractors.
- `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` and a GitHub Actions CI workflow.

### Changed
- Removed the runtime PySide6 auto-installer and `os.execv()` self-restart from the
  entry point; the app now performs a clean dependency check with a friendly message.
- Centralised hardcoded contact/sponsor details into `app_meta.py`; removed the
  personal phone number from the UI.
- `OutputRegistry` is now cleared on project load and at the start of every analysis,
  so switching projects can no longer surface stale outputs.
- Rewrote `README.md` to match actual behaviour.

### Fixed
- C/C++ and "All Languages" modes produced misleading Python-derived output.
- Analysis phase routing now maps every supported language to a correct extractor.

## [2.4.0]

### Added
- Multi-language audit suite (Kotlin/Android, JavaScript/TypeScript/Web Portal, Python).
- Deep extraction: data flow tracer, Room DB schema, navigation graph, DI graph,
  call graph, Firestore/backend schema, DOM map, hardware/service integrations,
  architecture digest, risk analysis.
- Git "diff only" scanning, safe-mode secret sanitizer, markdown merge/export,
  multi-theme UI, ZIP/`.md`/`.txt` export.

### Changed
- Production-grade UI/UX redesign with a unified dark/light design system.

## [1.0.0]

- Initial public release: structural context extraction for AI coding assistants.
