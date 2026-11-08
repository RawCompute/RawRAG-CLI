# ADR 001: Typer over Argparse for CLI Routing

**Status:** Accepted
**Date:** 2026-11-08

## Context
RawRAG is transitioning from a FastAPI web application to a zero-dependency, local codebase CLI tool. The command-line interface is the primary entry point for users interacting with the vector database and retrieval engine. The Python standard library provides `argparse`, and `click` is a widely used third-party alternative. We needed a framework that minimizes boilerplate while maximizing the developer experience (DX) for both the maintainer and the end user.

## Decision
We will use Typer to build the CLI routing and command structure instead of `argparse` or `click`.

## Reasoning
* **Type Hint Integration:** Typer relies on standard Python type hints to parse and validate arguments. Since the original RawRAG codebase was built on FastAPI (by the same creator as Typer), this maintains architectural consistency and keeps the code strictly typed.
* **Boilerplate Reduction:** `argparse` requires heavy setup and manual type conversion for every flag and argument. Typer binds command-line arguments directly to function parameters, significantly shrinking the size of `cli.py`.
* **Native Rich Support:** The CLI requires a custom 3D ASCII header and stylized output prompts. Typer integrates natively with `rich`, allowing seamless terminal formatting and colour output without overlapping library responsibilities.
* **Auto-Generated Documentation:** Typer automatically generates clean, comprehensive `--help` menus based on function docstrings and parameter type hints, ensuring the CLI is self-documenting for users.

## Consequences
* **Positive:** Faster iteration speed on CLI commands and a highly readable entry-point file.
* **Negative:** Introduces an external dependency to the project rather than relying purely on the Python standard library. However, the reduction in maintenance overhead and the improvement in user experience heavily outweigh the cost of one lightweight dependency.