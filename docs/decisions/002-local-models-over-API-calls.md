# ADR 002: Local Models Over API Calls

**Status:** Accepted  
**Date:** 2026-11-09  

## Context
The original RawRAG web application relies on Google GenAI APIs to handle machine learning tasks:
* `embedding-001`: For generating embeddings as NumPy arrays from text chunks.
* `gemini-1.5-flash` (or similar): For generating context-aware answers to user queries.

For RawRAG-CLI, the target audience is developers. We need a system that allows users to ingest entire proprietary codebases and run queries directly from their terminal without managing API keys, network latency, or external dependencies.

## Decision
We will replace cloud-based API calls with local, offline model execution.
* **Embeddings:** We will use `all-MiniLM-L6-v2` via the `sentence-transformers` library to generate 384-dimensional embeddings directly on the CPU.
* **Generation:** We will route text generation to a local Ollama server (`http://localhost:11434`), targeting lightweight, pre-installed models like `llama3`. 

## Reasoning
* **Data Privacy & IP Security:** Proprietary source code is highly sensitive. Processing queries and indexing context locally guarantees that code never leaves the developer's system, maintaining complete data integrity and compliance.
* **Air-Gapped Execution:** Local models allow developers to use the CLI tool completely offline on their own systems without network connectivity or third-party service outages disrupting their workflow.
* **Cost Efficiency:** Running embedding loops over thousands of lines of code locally eliminates all token-based API costs.

## Consequences
* **Positive:** Total data sovereignty and faster retrieval times due to zero network latency.
* **Negative:** Shifts the compute burden to the user's hardware. The user is now responsible for having Ollama installed and sufficient RAM (typically 8GB+) to run a model like Llama 3 smoothly.