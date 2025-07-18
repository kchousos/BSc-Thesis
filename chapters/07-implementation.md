# Implementation {#sec-implementation}

Repository cloning is performed using the `--depth 1` flag for less usage of disk storage and smaller artifacts size.

When creating the codebase oracle, the "libclang" Python package is utilized [@he2025] for slicing the functions based on the AST provided by Clang. As elaborated in @sec-oracle, the intermediate result is a list of Python dictionaries, each containing a function’s body, signature, and corresponding file-path. Each chunk's function code is then turned into an embedding using OpenAI's "text-embedding-3-small" model^[<https://platform.openai.com/docs/models/text-embedding-3-small>] and stored in a FAISS vector store index [@faiss]. This index is ID mapped to a metadata structure which contains the aforementioned function data---actual function body, signature, file-path. When a search is performed upon the index, the returned results are embeddings. The answers that the LLM agent receives are coming from each embedding's corresponding metadata entry.

Prompting techniques used (callback to @sec-prompting).
Sample prompt

[@dspy]

1.  Why instead of langchain or llamaindex? [@langchain; @llamaindex]

- models used
  gpt-4.1

## Development environment

uv, ruff, mypy, pytest, pdoc

## Reproducibility

github workflow actions, artifacts, summary
