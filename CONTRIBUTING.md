# Contributing to AI Context Extractor

Thanks for your interest in improving the project.

## Prerequisites

- Python **3.11+**
- Git

## Setup

```bash
git clone https://github.com/smtechie7-collab/ai_project_extractor.git
cd ai_project_extractor

python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements-dev.txt
```

## Run the app

```bash
python ai_project_extractor.py
# after `pip install -e .`:
aice
```

## Quality gates

Every pull request must pass:

```bash
ruff check .          # lint + import order
ruff format --check . # formatting
mypy core state models
pytest                # unit + golden tests
```

The same checks run in CI (`.github/workflows/ci.yml`).

## Project layout

| Path | Purpose |
|------|---------|
| `core/` | Scanning, classification, intelligence, per-language extractors |
| `core/extractors/<lang>/` | Language-specific extractors, one phase per module |
| `core/extractors/generic/` | Language-neutral extractors (C/C++, "All Languages", fallback) |
| `ui/` | PySide6 widgets, theming, main window |
| `state/` | Output registry and (for now) app state |
| `exporters/` | Output serialisation helpers |
| `tests/` | Unit, golden and UI tests |
| `packages/` | Installation payloads / bundled resources |

## Adding a new extractor / phase

1. Create the extractor module under `core/extractors/<lang>/`.
2. Add the phase name to `core/language_profiles.py`.
3. Route it in `ui/main_window.py::run_phase`.
4. Add a fixture mini-project and a golden test under `tests/`.

> Long term (Phase 2 of the roadmap) routing moves to an `Extractor` registry so it
> lives next to the extractor instead of in a central `if/elif` chain.

## Commit style

Conventional commits are preferred: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.

## License

By contributing you agree that your contributions are licensed under the MIT License.
