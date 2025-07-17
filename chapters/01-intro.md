\pagenumbering{arabic}

# Introduction

## Motivation

- Memory unsafety is and will be prevalent
- Software is safe until it’s not
- Humans make mistakes
- Humans now use Large Language Models (LLMs) to write software
- LLMs make mistakes [@perry2023]

Result: Bugs exist

## Goal

A system that:

1. Takes a bare C project as input
2. Generates a new fuzzing harness from scratch using LLMs
3. Compiles it
4. Executes it and evaluates it

## Preview of following sections (rename)
