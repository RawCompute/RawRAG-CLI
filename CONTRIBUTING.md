# Contributing to RawRAG-CLI

We welcome contributions from developers who share our passion for lean, understandable systems engineering.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/RawCompute/RawRAG-CLI.git
cd RawRAG-CLI
```

**Prerequisites:** Python 3.13+ and [uv](https://github.com/astral-sh/uv).

Set up your local environment:

```bash
uv venv
# Activate the virtual environment
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
uv pip install -e .
```

## Branching & Workflow

- Always assign yourself an active issue before starting work.
- Follow these branch naming conventions:
  - `feat/branch-name` for new features
  - `fix/branch-name` for bug fixes
  - `docs/branch-name` for documentation changes

## Local Testing

Test the indexing pipeline locally with:

```bash
rawrag index ./tests/dummy_code
```

**Important:** Never commit local `rawrag_index.db` or `rawrag_vectors.npy` files. Ensure they remain untracked.

## Pull Requests

- PR descriptions must link to the active issue (e.g., `Closes #3`).
- Code must be reviewed and approved by at least one other contributor before merging into `main`.
