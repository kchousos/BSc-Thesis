\pagenumbering{arabic}

# Introduction

Memory-safe languages, like Ada or Rust [@adadevelopers2022; @rustprojectdevelopers2025]---not absolutely safe themselves

NASA safety-critical code guidelines [@holzmann2006]

C by Dennis Ritchie in 1972 [@kernighan1978; @ritchie1978]

- Motivation
  - Memory unsafety is and will be prevalent
  - Software is safe until it’s not
  - Humans make mistakes
- LLMs have become very powerful
  - They are used more and more
  - Humans now use Large Language Models (LLMs) to write software
  - LLMs make mistakes [@perry2023]
- Result: Bugs exist
- Fuzzing is a popular software testing strategy
  - LLM applications and capabilities are still explored
    - One of which is automatic harnessing

- Goal
  - A system that:
    1. Takes a bare C project as input
    2. Generates a new fuzzing harness from scratch using LLMs
    3. Compiles it
    4. Executes it and evaluates it

- Thesis Structure
  - We examine the state of automatic fuzzing projects
    - Most automatic fuzzers rely on existings harnesses [@oss-fuzz-gen] or preexisting client code [@utopia; @fuzzgen; @fudge]
    - No evaluation step, it is left to the developer/user
  - To address these challenges, we introduce OverHAuL
    - We explain its design architecture, the techniques that emerged in its development and how they are implemented
    - We construct a dataset of 10 open-source projects and evaluate OverHAuL with them
    - We examine the results and try to answer our research questions <!-- Insert here? -->

- Summary of Contributions
  - We propose OverHAuL, a new automatic fuzzing framework
  - Experimental benchmarks show a 92.5% chance of successful harness generation
  - Code and artifacts are available in the project's repo <https://github.com/kchousos/OverHAuL>
