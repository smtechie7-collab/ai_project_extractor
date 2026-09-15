# 🧠 AI Context Extractor (v2.4)

**Bridge the gap between your local codebase and AI coding assistants.**

AI Context Extractor is a Python desktop application (PySide6/Qt) that analyses a
software project and generates context optimised for LLMs (ChatGPT, Claude, Gemini).

Instead of blindly pasting raw code, it extracts the **structural meaning** of your
project — database schemas, navigation graphs, data flows, dependency-injection
trees, call graphs and risk reports — so the AI can write accurate code with fewer
hallucinations.

> All analysis runs **locally**. No code is uploaded anywhere by this tool.

---

## ✨ Key features

### Deep static analysis

| Ecosystem | Extracted insight |
|-----------|-------------------|
| **Kotlin / Android** | Data flow tracer (ViewModel → Repository → DAO), Room DB schema, Jetpack Compose navigation graph, manual DI + Hilt/Dagger graph, UI map, outbox/cloud-sync audit, architecture digest, call graph, risk analysis |
| **JavaScript / TypeScript / Web** | Dependency graph, Firestore & backend schema, Web UI/DOM event map, hardware & service integrations, architecture/spec digest, risk analysis |
| **Python** | Module classification, call graph, AST-powered risk analysis, full source export |
| **Java** | Module classification, call graph, risk analysis |
| **C / C++ and "All Languages"** | Language-neutral module classification, full source export and heuristic risk analysis |

### Visual architecture
Generates **Mermaid.js** blocks (ER diagrams, navigation flowcharts) you can paste
straight into ChatGPT or Mermaid Live.

### Security & privacy
- **Safe Sanitizer** (on by default) redacts AWS keys, Google API keys, generic
  `api_key` / `token` / `password` assignments, bearer tokens, emails and
  non-private IPv4 addresses before content is copied or exported.
- 100% local processing.

### Developer workflow
- **Git diff mode** – analyse only modified / staged / untracked files.
- **Quick feature extraction** – type a feature name (`billing`, `kyc`, `auth` …) and
  pull only the related files, ranked by relevance and grouped by architectural layer.
- **Markdown merge** – combine many `.md` files into one AI-ready document.
- **Prompt templates** – one-click copy with "Find Bugs", "Security Audit", "Refactor",
  "Write Documentation", "Explain to Junior".
- **Exports** – active view (`.txt`), all phases, consolidated `.md`, or a full `.zip`.

---

## 🚀 Installation

> Requires **Python 3.11+**.

```bash
git clone https://github.com/smtechie7-collab/ai_project_extractor.git
cd ai_project_extractor

python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements.txt
```

### Run

```bash
python ai_project_extractor.py
```

Or install the package (adds an `aice` command):

```bash
pip install -e .
aice
```

---

## 📖 How to use

1. **Open Project** – click `📂 Open Project` (or drag & drop a folder) and pick your
   project root.
2. **Choose mode** – pick a **Language** in the toolbar. For a scoped analysis, tick
   **Git Diff Only** to analyse just your changed files.
3. **Run analysis** – click **▶ Run Deep Analysis**. Progress is shown per phase.
4. **Inspect** – use the **Phase** dropdown to view each report. The sidebar tracks
   each phase's state.
5. **Send to AI** – pick an **AI Task** template, keep **Safe Sanitizer** on, and click
   **📋 Copy with Prompt**. Paste into ChatGPT / Claude / Gemini.

---

## 🛠️ Technology stack

- **Language:** Python 3.11+
- **GUI:** PySide6 (Qt for Python)
- **Analysis:** stdlib `ast`, `re`, `os`, `subprocess` (git)
- **State:** module-level `AppState` with reactive UI updates *(migration to an
  immutable `ScanConfig` is on the roadmap)*

---

## 🧪 Development

```bash
pip install -r requirements-dev.txt

ruff check .          # lint
mypy core state models
pytest                # tests
```

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full workflow and
**[SECURITY.md](SECURITY.md)** to report vulnerabilities.
Changes are tracked in **[CHANGELOG.md](CHANGELOG.md)**.

---

## 🗺️ Roadmap (highlights)

- Real-time **token budgeting** with per-provider context limits.
- **Impact analysis** — changed files + their transitive dependents.
- Standalone **secrets scan** phase.
- **CLI mode** and CI integration.
- Headless **MCP server** mode and direct AI-provider integration.
- More ecosystems (Flutter, Swift, Go, Rust, C#, PHP) and infra (Docker, K8s, Terraform).

---

## 🤝 Contributing

Contributions are welcome! Please open a Pull Request.

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
