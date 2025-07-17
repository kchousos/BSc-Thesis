# Implementation {#sec-implementation}

--depth 1
output/<repo-name>

embedder model openai
Source code is processed and chunked using Clang [33]. The chunks are function-level units, found to be a sweet-spot between semantic significance and size [@zhao2024; @chen2021].
This results in a list of Python dicts, each containing a function’s body, signature and filepath.
Each chunk’s function code is then turned into an embedding using OpenAI’s “text-embedding-3-small” model.
faiss store and index
A FAISS [36] vector store is created. Each function embedding is stored in it (with the same order, as to correspond with the previous list containing the metadata).

same order code chunks

Prompting techniques used (callback to @sec-prompting).
Sample prompt

[@dspy]

1.  Why instead of langchain or llamaindex? [@langchain; @llamaindex]

libclang Python package

## Development environment

uv, ruff, mypy, pytest, pdoc

## Equipment

desktop pc cpu, memory

## models used

gpt-4.1

## Reproducibility

github workflow actions, artifacts, summary
