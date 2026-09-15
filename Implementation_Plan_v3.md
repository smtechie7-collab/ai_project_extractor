# 🛠️ AI Context Extractor — Full Implementation Plan (v2.4 → v3.0 "Production Perfect")

**Owner:** Lead Developer + Software Manager
**Basis:** Code & Product Audit (2026-09-15)
**Scope:** Repo hygiene, stability, architecture refactor, testing/CI, feature completion, platform/scale
**Runtime deps today:** PySide6 only (verified — सब बाकी stdlib/AST/regex)

---

## 0. How to read this plan

- हर task का ID (P0-1, P1-4 …) है, files, "Done when" (acceptance criteria), effort (dev-days), और dependencies।
- Phases order में हैं, पर **P0 + P1 = release-blocking**, ये पहले करो। P2+ parallelizable हैं।
- `tasks.csv` (साथ में attached) GitHub Issues / Linear / Jira में direct import हो जाएगी।
- Effort 1 developer ke liye realistic estimate hai.

---

## 1. Goal — "Perfect" का मतलब (Definition of Done)

Tool tab "perfect" माना जाएगा जब:

1. Fresh machine पर `pip install -r requirements.txt && python -m aice` **बिना error** चले।
2. Repo में **कोई junk / personal data / committed build artifact** न हो।
3. हर language-mode अपने **सही** extractor चलाए (कोई silent wrong analysis नहीं)।
4. सभी outputs **run-scoped** हों — project switch पर कोई stale data leak न हो।
5. **CI green**: ruff + mypy + pytest (≥70% coverage core पर) तीनों OS पर।
6. हर extractor का **unit + golden test** हो।
7. No silent `except Exception: pass` — सब logged + user-co-visible।
8. Deep/large repo पर analysis **cancel-able**, parallel, और incremental।
9. Real **token budgeting** काम करे (README के दावे सच हों)।
10. Distribution **one-file exe / MSI** के रूप में हो, signed + auto-update।

---

## 2. Target architecture (after refactor)

```
ai_project_extractor/
├─ pyproject.toml              # NEW — build, deps, ruff/mypy/pytest config
├─ requirements.txt            # NEW — pinned runtime deps
├─ requirements-dev.txt        # NEW
├─ README.md                   # REWRITTEN
├─ CHANGELOG.md  CONTRIBUTING.md  SECURITY.md   # NEW
├─ .github/workflows/ci.yml    # NEW
├─ .pre-commit-config.yaml     # NEW
├─ src/aice/                   # NEW package root (src-layout)
│  ├─ __main__.py              # python -m aice (GUI entry)
│  ├─ cli.py                   # NEW — headless CLI mode
│  ├─ config.py                # NEW — ScanConfig (frozen dataclass)
│  ├─ context.py               # NEW — AnalysisContext (tree, cache, logger)
│  ├─ logging_setup.py         # NEW
│  ├─ core/                    # scanner, model, cache, registry
│  ├─ extractors/
│  │  ├─ base.py               # NEW — Extractor Protocol + registry
│  │  ├─ kotlin/  js_ts/  python/  generic/   # generic/ = NEW (cpp, all, fallback)
│  ├─ features/                # token_budget, impact_analysis, secrets_scan
│  ├─ exporters/
│  └─ ui/
├─ tests/                      # NEW — unit + golden + fixtures
│  └─ fixtures/                # sample mini-projects
└─ packaging/                  # NEW — PyInstaller spec, installer
```

Key new abstractions:

```python
# config.py
@dataclass(frozen=True, slots=True)
class ScanConfig:
    project_root: Path
    language: str
    git_only: bool = False
    max_file_kb: int = 512
    whitelist: frozenset[str] = frozenset()
    include_tests: bool = True

# extractors/base.py
@runtime_checkable
class Extractor(Protocol):
    phase: str
    languages: tuple[str, ...]
    def run(self, ctx: "AnalysisContext") -> str: ...

REGISTRY: dict[str, Extractor] = {}    # phase -> extractor
def register(cls): REGISTRY[cls.phase] = cls(); return cls
```

---

## PHASE 0 — Repo hygiene & baseline  ⏱ 1 day  🔴 blocker

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P0-1 | `requirements.txt` बनाओ, PySide6 pin करो | `requirements.txt` | `pip install -r requirements.txt` clean install करे | 0.2 | — |
| P0-2 | `pyproject.toml` (PEP 621) — name, version, entry-point, build backend | `pyproject.toml` | `pip install -e .` काम करे, `aice` कमांड बने | 0.3 | P0-1 |
| P0-3 | `.gitignore` harden | `.gitignore` | `.vs/`, `*.suo`, `*.vsidx`, `*.user`, `.analysis_cache.json`, `*.spec.bak` ignored | 0.1 | — |
| P0-4 | Committed junk untrack करो (history नहीं, working tree) | git index | `.vs/**`, `**/__pycache__/**`, `core/New Text Document.txt` index से बाहर | 0.2 | P0-3 |
| P0-5 | Personal data हटाओ (phone, personal Gmail, PayPal) → config/constants से | `ui/main_window.py`, `aice/constants.py` | repo में कोई personal PII नहीं; About में generic support link | 0.2 | — |
| P0-6 | `qr.jpg` + base64 embed को assets/ में move + lazy load | `assets/`, `ui/main_window.py` | inline 4KB base64 string gone | 0.2 | P0-5 |
| P0-7 | README rewrite — सही repo name, सही entry command, केवल real features | `README.md` | README के हर claim का कोड सबूत हो | 0.4 | — |
| P0-8 | `CHANGELOG.md` (Keep a Changelog) + `CONTRIBUTING.md` + `SECURITY.md` | root | मौजूद, version 2.4 se entry | 0.3 | — |
| P0-9 | `LICENSE` verify + copyright header standards | `LICENSE` | MIT consistent, headers में author correct | 0.1 | — |
| P0-10 | `core/New Text Document.txt` delete, empty dirs clean | repo | कोई stray file नहीं | 0.1 | — |

**Phase 0 Exit:** fresh clone → install → run, और repo में कोई junk/PII नहीं।

---

## PHASE 1 — Stability & correctness  ⏱ 3–4 days  🔴 blocker

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P1-1 | Auto-install bootstrap हटाओ → friendly error dialog + startup dependency check | `aice/__main__.py` | PySide6 missing पर dialog "run pip install", कोई `os.execv` नहीं | 0.3 | P0-2 |
| P1-2 | `run_phase` routing fix — `cpp` + `all` + unknown का dedicated `generic` extractor | `aice/ui/main_window.py`, `extractors/generic/*` | C++ पर Python output नहीं; unsupported = clear message | 0.6 | — |
| P1-3 | `OutputRegistry` lifecycle — `clear()` project load / new run पर, widget reset | `state/output_registry.py`, `ui/main_window.py`, `ui/workspace.py` | Project switch पर dropdown stale entries नहीं | 0.3 | — |
| P1-4 | Iterative scan (recursion remove) — `os.walk`-based | `core/scanner.py` | 50-level deep tree पर `RecursionError` नहीं | 0.4 | — |
| P1-5 | Global logging setup (`logging`, rotating file + stderr) | `aice/logging_setup.py` | सारे modules `logger = getLogger(__name__)` use करें | 0.4 | — |
| P1-6 | Bare `except Exception:` साफ़ करो (~40 जगह) → `logger.exception` + typed except | सभी modules | `ruff` rule `BLE001` enabled और pass | 1.0 | P1-5 |
| P1-7 | Per-phase error isolation — एक phase fail हो तो बाकी चलें + UI warning badge | `ui/worker.py`, `ui/main_window.py`, `ui/sidebar.py` | Fail phase लाल दिखे, run रुके नहीं | 0.5 | — |
| P1-8 | Cancellation support — Stop button, worker cooperative cancel | `ui/worker.py`, `ui/workspace.py` | Long scan बीच में cancel हो, resources clean | 0.6 | — |
| P1-9 | Progress fix — real weighted progress + phase timing + ETA | `ui/worker.py`, `ui/workspace.py` | पहले phase पर 0% stuck नहीं; "% done" सही | 0.4 | P1-8 |
| P1-10 | Sidebar state machine: pending/running/done/**failed** अलग | `ui/sidebar.py` | `mark_all_done` semantics सही | 0.3 | P1-7 |
| P1-11 | Content read cache (mtime+size key, LRU) wire करो | `state/performance_cache.py` → `aice/core/cache.py` | एक run में file एक बार पढ़े जाए | 0.6 | P1-4 |
| P1-12 | File-size / binary / encoding guards consistent (max kb config से) | `core/utils/file_reader.py` | हर extractor same guard use करे | 0.3 | P1-11 |
| P1-13 | Git-scan hardening — `git status --porcelain=v1 -z`, binary-safe, errors surfaced | `core/git_scanner.py` | Unicode filenames + spaces काम करें | 0.4 | — |

**Phase 1 Exit:** कोई crash नहीं, कोई silent failure नहीं, cancel/progress सही, large repo पर stable।

---

## PHASE 2 — Architecture refactor  ⏱ 5–7 days  🟠

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P2-1 | `ScanConfig` frozen dataclass introduce; functions को param में pass | `aice/config.py` + सभी extractors | extractors में `AppState` import **zero** | 1.5 | P1-* |
| P2-2 | `AnalysisContext` object (tree, config, cache, logger, progress_cb) | `aice/context.py` | हर extractor signature `run(self, ctx)` | 0.8 | P2-1 |
| P2-3 | Global `AppState` हटाओ → UI-local state object | `state/app_state.py`, `ui/*` | AppState file deleted, tests parallel-safe | 0.8 | P2-1 |
| P2-4 | Unified tree model — `models/tree_node.py` बनाओ, `scanner.Node` हटाओ | `models/`, `core/scanner.py`, extractors | एक ही Node class पूरे repo में | 0.8 | P2-2 |
| P2-5 | Extractor registry + `base.Extractor` Protocol | `extractors/base.py`, `main_window.py` | नया phase जोड़ना = सिर्फ class register | 1.0 | P2-2 |
| P2-6 | Duplicate logic merge: 4× `risk_analyzer` → shared engine + per-lang rules | `extractors/**/risk_analyzer.py`, `aice/features/risk/` | एक engine, N rule-sets | 1.0 | P2-5 |
| P2-7 | `executive_summary` vs `_v2` merge | `core/summary/` | एक ही implementation | 0.3 | — |
| P2-8 | Dead code resolve — wire या delete (classifier/rules/role_exporter, backend_domain_*, contract_*, coupling_*, entry_*, di_*, async_*, graphviz/*, ui/menus.py, ui/header.py, guided_workspace.py, onboarding_dialog.py) | repo | `vulture` clean; onboarding_dialog wired | 1.0 | P2-5 |
| P2-9 | Type hints पूरे public API पर + `from __future__ import annotations` | सभी modules | mypy strict pass (core), relaxed UI | 1.0 | P2-5 |
| P2-10 | Extractors को package-wise isolate + language-agnostic helpers shared | `extractors/` | circular imports शून्य | 0.5 | P2-5 |

**Phase 2 Exit:** कोई global mutable state नहीं, duplicate logic नहीं, plugin-ready extractor registry।

---

## PHASE 3 — Testing & CI  ⏱ 4–5 days  🟠

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P3-1 | pytest setup + `conftest.py` + `tests/fixtures/` mini-repos (kotlin/js/python/cpp) | `tests/` | `pytest` चले, fixtures reusable | 0.6 | P2-* |
| P3-2 | Unit tests: scanner, cache, config, git_scanner, file_reader | `tests/unit/` | edge-cases covered (perm, binary, deep tree) | 0.8 | P3-1 |
| P3-3 | Extractor unit tests (per language, parse correctness) | `tests/extractors/` | हर extractor ≥5 assertions | 1.2 | P3-1 |
| P3-4 | **Golden/snapshot tests** — fixture input → approved output diff | `tests/golden/` | `--update-golden` flag काम करे | 0.8 | P3-3 |
| P3-5 | Sanitizer tests (secrets redaction + false positives) | `tests/unit/test_sanitizer.py` | known keys redact, normal text untouched | 0.4 | P3-1 |
| P3-6 | UI smoke tests (pytest-qt) — window खुले, project load, phase switch | `tests/ui/` | CI headless (offscreen) पास | 0.8 | P3-1 |
| P3-7 | Coverage config + gate (core ≥70%) | `pyproject.toml` | coverage fail CI break करे | 0.2 | P3-3 |
| P3-8 | ruff config (lint + format) + `pre-commit` hooks | `pyproject.toml`, `.pre-commit-config.yaml` | `ruff check` clean | 0.3 | P1-6 |
| P3-9 | mypy config + CI enforcement | `pyproject.toml` | core strict pass | 0.3 | P2-9 |
| P3-10 | GitHub Actions CI — matrix (Win/Ubuntu × Py3.11/3.12/3.13), cache pip | `.github/workflows/ci.yml` | PR पर lint+type+test हर matrix green | 0.5 | P3-8/9 |
| P3-11 | Release workflow — tag पर build + artifacts + CHANGELOG check | `.github/workflows/release.yml` | `v*` tag → artifacts attach | 0.5 | P3-10 |
| P3-12 | Test-data generator script (random project) | `tests/gen_sample.py` | CI में volume test | 0.3 | P3-1 |

**Phase 3 Exit:** CI green, कोई regression बिना test के merge न हो।

---

## PHASE 4 — Core feature completion  ⏱ 6–8 days  🟢 (differentiation)

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P4-1 | **Token Budget Engine** — per-phase + total token count, per-provider context presets (GPT/Claude/Gemini), budget bar, overflow warning | `aice/features/token_budget.py`, `ui/workspace.py` | README का "real-time token usage" सच हो | 1.0 | P2-5 |
| P4-2 | Auto-trim / smart-summarize जब budget exceed (largest-file drop + notice) | `aice/features/token_budget.py` | Overflow पर valid context मिले | 0.8 | P4-1 |
| P4-3 | **Impact Analysis** — changed files + reverse transitive dependents (BFS) | `aice/features/impact_analysis.py` | "इस change से कौन प्रभावित" list आए | 1.2 | P4-1 |
| P4-4 | Dependency graph extraction unified (imports → graph JSON) | `aice/features/depgraph.py` | graph reusable by impact+cycles | 0.8 | P4-3 |
| P4-5 | **Secrets Scan phase** — expanded patterns (AWS/GCP/GitHub/JWT/`sk-`/private keys/.env/high-entropy) | `aice/features/secrets_scan.py` | copy से पहले + standalone phase | 0.8 | P3-5 |
| P4-6 | Output viewer: Ctrl+F search, line numbers, jump-to-match, copy-raw | `ui/workspace.py` | large output में navigate हो | 0.8 | — |
| P4-7 | Run history + run-to-run diff ("क्या बदला") | `aice/features/run_history.py`, `ui/` | पिछले run से diff दिखे | 0.8 | P1-3 |
| P4-8 | Language/framework auto-detect + monorepo (multi-profile) | `aice/detect.py`, `ui/action_bar.py` | Android+web repo दोनों profiles | 1.0 | P2-1 |
| P4-9 | i18n — Hinglish strings हटाओ, `QTranslator` + `.ts` (en + hi optional) | `ui/*`, `i18n/` | UI language-consistent | 0.6 | — |
| P4-10 | Per-project presets (language+phases+template याद रखो) | `aice/presets.py`, `ui/` | project reopen पर settings restore | 0.5 | P4-8 |
| P4-11 | Onboarding dialog wire (पहली बार) + empty-states | `ui/onboarding_dialog.py`, `ui/` | first-run guide दिखे | 0.3 | P2-8 |

**Phase 4 Exit:** Token budgeting + impact analysis + secrets scan live; UI search/history/presets।

---

## PHASE 5 — Platform & scale  ⏱ 7–10 days  🔵

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P5-1 | **Headless CLI** — `aice scan --project . --lang kotlin --out ctx.md [--phases ...]` | `aice/cli.py` | CI/scripts से run हो | 1.0 | P2-5 |
| P5-2 | Parallel extraction — `ThreadPoolExecutor` per-file / per-phase | `aice/core/runner.py` | बड़े repo पर ≥2× speed | 1.0 | P2-2 |
| P5-3 | Incremental analysis (mtime cache persist `.aice_cache.json`) | `aice/core/cache.py` | दूसरी run तेज़ | 0.8 | P1-11 |
| P5-4 | Packaging: PyInstaller one-file + `--windowed`, spec checked-in | `packaging/aice.spec` | Windows exe बने, चले | 1.0 | P0-2 |
| P5-5 | MSI/installer (Inno Setup / WiX) + code-signing hook | `packaging/` | signed installer | 1.0 | P5-4 |
| P5-6 | Auto-update check (GitHub releases API) | `aice/updater.py` | new version prompt | 0.6 | P3-11 |
| P5-7 | **MCP server mode** — Claude/Cursor/Chatbox agents codebase query करें | `aice/mcp_server.py` | MCP client से list/read tools | 1.5 | P2-5 |
| P5-8 | Direct AI integration (OpenAI/Anthropic/Gemini), cost estimate inline | `aice/features/ai_client.py`, `ui/` | clipboard round-trip के बिना response | 1.5 | P4-1 |
| P5-9 | नए ecosystems: Flutter/Dart, Swift, Go, Rust, C#, PHP (regex-based start) | `extractors/<lang>/` | हर lang का detection + phases | 2.0 | P4-8 |
| P5-10 | Infra extractors: Dockerfile, K8s YAML, Terraform, SQL migrations | `extractors/infra/` | deploy surface map | 1.0 | P5-9 |
| P5-11 | Plugin system — third-party extractor loading (entry-points) | `aice/plugins.py` | external package extractor जोड़े | 0.8 | P2-5 |
| P5-12 | Structured logging + "Export diagnostics bundle" | `aice/logging_setup.py`, `ui/` | bug report easy | 0.4 | P1-5 |

**Phase 5 Exit:** CLI + exe + MCP + AI integration + multi-ecosystem।

---

## PHASE 6 — Manager deliverables & polish  ⏱ 4–6 days  🟣

| ID | Task | Files | Done when | Est | Deps |
|----|------|-------|-----------|-----|------|
| P6-1 | Project health dashboard (risk + debt + coverage + coverage-gap) | `aice/features/dashboard.py`, `ui/` | एक नज़र में status | 1.2 | P4-* |
| P6-2 | Ownership map (git blame → per-module owners) | `aice/features/ownership.py` | "कौन maintainer" | 0.8 | P4-3 |
| P6-3 | Churn × Complexity refactor hotspots (git log + cyclomatic) | `aice/features/hotspots.py` | refactor priority list | 1.0 | P4-4 |
| P6-4 | Dead-code & duplication detection | `aice/features/deadcode.py` | unreferenced + dup blocks | 1.0 | P4-4 |
| P6-5 | Test coverage mapping (किन files का test नहीं) | `aice/features/coverage_map.py` | gap list | 0.8 | P3-* |
| P6-6 | Exports: PDF/HTML report, Confluence/Notion, Jira-ready tech-debt CSV | `exporters/` | manager-friendly deliverable | 1.0 | P6-1 |
| P6-7 | Onboarding doc generator (new-dev context pack) | `aice/features/onboarding_pack.py` | docs auto | 0.6 | P4-* |
| P6-8 | Semantic search index (local embeddings + SQLite) — optional | `aice/features/semantic.py` | natural-language query | 1.5 | P2-5 |
| P6-9 | Accessibility + keyboard shortcuts + tooltips audit | `ui/` | full keyboard nav | 0.5 | — |

---

## 3. Quality gates (हर phase में लागू)

| Gate | Tool | Threshold |
|------|------|-----------|
| Lint | ruff | 0 errors |
| Type | mypy | core strict, UI basic |
| Test | pytest | pass + coverage core ≥70% |
| Dead code | vulture | 0 unused (whitelisted) |
| Security | bandit + pip-audit | 0 high |
| Docs | README/CHANGELOG updated | PR template enforce |
| PR | 1 review + CI green | branch protection |

---

## 4. Milestones

| Milestone | Phases | Output | Est |
|-----------|--------|--------|-----|
| **M1 — Release Blockers Cleared** | P0 + P1 | Installable, stable, no junk | ~1 week |
| **M2 — Clean & Tested Core** | P2 + P3 | Refactored, CI green | ~2 weeks |
| **M3 — Differentiated Product** | P4 | Token budget, impact analysis, secrets scan | ~1.5 weeks |
| **M4 — Platform Ready** | P5 | CLI, exe, MCP, AI API, multi-lang | ~2 weeks |
| **M5 — Manager Suite** | P6 | Dashboard, ownership, exports | ~1 week |

**Total (1 dev, part-time assumptions flexible): ~7–8 weeks** to v3.0.
Fast path (P0+P1+P3 only, "stable & trustworthy"): **~1.5 weeks**.

---

## 5. Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Refactor (P2) से regressions | High | High | पहले P3 golden tests बनाओ, फिर refactor |
| Scope creep (P5 नए languages) | High | Med | Registry-based, हर language isolated PR |
| PyInstaller में PySide6 plugins miss | Med | Med | spec में hooks + CI build smoke test |
| MCP/AI API scope बढ़ना | Med | Med | Optional dependency, feature-flag |
| Single-dev bandwidth | High | Med | P0/P1/P3 पहले; P5/P6 backlog में |

---

## 6. Immediate next 5 tasks (आज शुरू करो)

1. **P0-1 / P0-2** — `requirements.txt` + `pyproject.toml`
2. **P0-3 / P0-4** — `.gitignore` + junk untrack
3. **P1-2** — C++/all routing fix (silent wrong analysis हटाओ)
4. **P1-3** — `OutputRegistry.clear()` lifecycle
5. **P3-1** — pytest + fixtures (refactor से पहले safety net)

---

## 7. Backlog (nice-to-have, बाद में)

- Web UI / VS Code extension
- Team mode (shared analysis server)
- Budget alerts / trends over time
- Graph visualization UI (interactive, mermaid + cytoscape)
- Multi-repo workspace analysis
