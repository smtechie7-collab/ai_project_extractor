🧠 AI Context Extractor (v2.4)

Bridge the gap between your local codebase and AI coding assistants.

AI Context Extractor is a Python-based desktop application (GUI) designed to analyze your software projects and generate optimized context for LLMs (ChatGPT, Claude, Gemini).

Instead of blindly pasting raw code files, this tool extracts the structural meaning of your project—database schemas, navigation graphs, data flows, and dependency injection trees—allowing AI to write accurate code without hallucinations.

✨ Key Features

🔍 Deep Static Analysis

Kotlin / Android:

Data Flow Tracer: Traces logic from ViewModel → Repository → DAO.

Room DB Schema: Extracts tables, columns, and relationships into SQL/ERD formats.

Navigation Graph: Maps NavHost routes and screen connections.

DI Graph: Visualizes Manual DI (AppContainer) and Hilt/Dagger modules.

Python: Call graphs and module classification.

JS/TS: Dependency graphs and risk analysis.

📊 Visual Architecture (Mermaid.js)

Automatically generates Mermaid.js code blocks. Simply copy-paste the output into ChatGPT or Mermaid Live to visualize:

Database Entity-Relationship Diagrams (ERD).

Screen Navigation Flowcharts.

🛡️ Security & Privacy

Safe Mode: Automatically sanitizes output by redacting API Keys, AWS Secrets, Emails, and IP addresses using regex patterns before copying to clipboard.

Local Processing: All analysis happens locally on your machine. No code is uploaded to any server.

⚡ Developer Workflow

Git Integration: Toggle "Git Changes Only" to analyze only the files you modified. Perfect for generating context for a specific bug fix or feature.

Prompt Templates: One-click copy with instructions like "Find Bugs", "Refactor", or "Write Documentation".

Token Budgeting: Real-time token usage estimation.

🚀 Installation

Clone the repository:

git clone [https://github.com/YOUR_USERNAME/ai-context-extractor.git](https://github.com/YOUR_USERNAME/ai-context-extractor.git)
cd ai-context-extractor


Install Dependencies:

pip install -r requirements.txt


Run the App:

python app.py


📖 How to Use

Select Project: Click "Select Project" and choose your root folder (e.g., your Android project).

Choose Mode:

Full Scan: Analyzes the entire codebase.

Git Mode: Check "Git Changes Only" to analyze only modified/staged files.

Run Analysis: Click the "Run Analysis" button.

Select Output: Use the dropdown to view specific insights (e.g., "Data Flow Tracer", "Database Schema").

Copy to AI:

Select a task (e.g., "🐛 Find Bugs").

Click "Copy w/ Prompt".

Paste into ChatGPT/Claude.

🛠️ Technology Stack

Language: Python 3

GUI Framework: PySide6 (Qt for Python)

State Management: Singleton pattern with Reactive UI updates.

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License

Distributed under the MIT License. See LICENSE for more information.