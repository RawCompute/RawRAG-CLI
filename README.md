```text
██████╗  █████╗ ██╗    ██╗██████╗  █████╗  ██████╗      ██████╗██╗     ██╗
██╔══██╗██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔════╝     ██╔════╝██║     ██║
██████╔╝███████║██║ █╗ ██║██████╔╝███████║██║  ███╗    ██║     ██║     ██║
██╔══██╗██╔══██║██║███╗██║██╔══██╗██╔══██║██║   ██║    ██║     ██║     ██║
██║  ██║██║  ██║╚███╔███╔╝██║  ██║██║  ██║╚██████╔╝    ╚██████╗███████╗██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚═════╝╚══════╝╚═╝
```

# RawRAG-CLI: First-Principles Codebase RAG

RawRAG-CLI is a zero-dependency, local Retrieval-Augmented Generation (RAG) command-line tool designed for developers. Instead of relying on bloated frameworks like LangChain or heavy vector databases like ChromaDB, RawRAG-CLI is built from first principles using pure **NumPy** matrix math and **SQLite**. 

Scan your local codebase, compute embeddings on your CPU, and query your code using local LLMs—all completely offline, ensuring your proprietary code never leaves your machine.

## Core Features

* **100% Offline & Private:** Uses `sentence-transformers` for local CPU embeddings and integrates with `Ollama` for local LLM generation. 
* **First-Principles Engine:** No black-box frameworks. Vector search is implemented using pure NumPy cosine similarity. Metadata and chunk mapping are handled by a lightweight SQLite schema.
* **Frictionless DX:** Built on `Typer` and `Rich` for a heavily typed, beautifully formatted terminal experience.
* **Architecturally Transparent:** Major design choices are documented in the `docs/decisions/` (ADR) directory.

## Tech Stack

* **CLI Routing:** `Typer`
* **Formatting:** `Rich`
* **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
* **Vector Math:** `NumPy` (Float32 matrix operations)
* **Metadata Storage:** `SQLite3` (Native Python)
* **LLM Engine:** `Ollama` (HTTP POST interface)

---

## Installation & Setup

**Prerequisites:** 
1. Install [Ollama](https://ollama.com/) and pull a lightweight model: `ollama run llama3`
2. Ensure you have [uv](https://github.com/astral-sh/uv) installed for lightning-fast package management.

**Install the CLI:**
```bash
# Clone the repository
git clone https://github.com/your-org/RawRAG-CLI.git
cd RawRAG-CLI

# Install as an editable package using uv
uv pip install -e .
```

---

## Usage

RawRAG-CLI exposes two primary commands. Run them directly in your terminal from any codebase directory.

### 1. Indexing a Codebase
Scan the current directory, generate text chunks, compute 384-dimensional embeddings, and save the vector index locally.
```bash
rawrag index .
```

### 2. Querying the Codebase
Ask a natural language question about the indexed codebase. The CLI will retrieve the most relevant code chunks via cosine similarity and ping your local Ollama instance for the answer.
```bash
rawrag query "Where is the authentication logic handled?"
```

---

## Development Roadmap

- [x] **Phase 1: Architecture Pivot:** Migrate from FastAPI web-app to Typer CLI.
- [x] **Phase 2: Local AI Integration:** Replace Google GenAI with Sentence Transformers and Ollama.
- [ ] **Phase 3: Multi-Extension Support:** Expand chunking logic beyond `.py` to support `.md`, `.ts`, `.rs`, and `.go`.
- [ ] **Phase 4: AST-Aware Chunking:** Move from naive sliding-window text chunking to Abstract Syntax Tree (AST) parsing to ensure functions and classes aren't split across chunks.
- [ ] **Phase 5: Evaluation Suite:** Build a gold-standard evaluation dataset (`data/evals.json`) and benchmarking script to formally measure retrieval accuracy (Recall@K).
- [ ] **Phase 6: Watch Mode:** Add an optional daemon mode to auto-reindex files when changes are detected in the directory.

---

## Contributing

We welcome contributions from developers who share our passion for lean, understandable systems engineering. 

**Rules of Engagement:**
1. **Keep it Framework-Free:** Do not introduce heavy abstractions (LlamaIndex, LangChain, SQLAlchemy). We write raw math and raw SQL.
2. **Write ADRs:** If you propose a major structural change or a new dependency, write an Architecture Decision Record in `docs/decisions/` first.
3. **Branching:** Fork the repo and create a feature branch (`feature/ast-chunking` or `fix/sqlite-locks`).
4. **Testing:** Ensure the core `addvector` and `similarity` matrix operations pass existing tests before submitting a PR.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.