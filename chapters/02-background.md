# Background

## Fuzz Testing

**Fuzzing** is an automated software-testing technique in which a *Program Under Test* (PUT) is executed with (pseudo-)random inputs in the hope of exposing undefined behavior. When such behavior manifests as a crash, hang, or memory-safety violation, the corresponding input constitutes a *test-case* that reveals a bug and often a vulnerability [@manes2019]. In essence, fuzzing is a form of adversarial, penetration-style testing carried out by the defender before the adversary has an opportunity to do so. Interest in the technique surged after the publication of three practitioner-oriented books in 2007--2008 [@takanen2018; @sutton2007; @rathaus2007].

Historically, the term was coined by Miller et al. in 1990, who used "fuzz" to describe a program that "generates a stream of random characters to be consumed by a target program" [@miller1990]. More rigorously---borrowing Manes et al.'s definitions [@manes2019]:

::: {#def-fuzzing}
###### Fuzzing
Fuzzing is the execution of a Program Under Test (PUT) using input(s) sampled from an input space (the *fuzz input space*) that protrudes the expected input space of the PUT.
:::

An individual execution (or bounded set of executions) that meets this definition is a *fuzzing run*. When such runs are performed systematically and at scale to test whether the PUT violates a specified security policy, we speak of **fuzz testing** (or simply *fuzzing* in common parlance):

::: {#def-fuzz-testing}
###### Fuzz Testing
Fuzz testing is the use of fuzzing to test whether a PUT violates a security policy.
:::

A **fuzzer engine** orchestrates a **fuzz campaign**---one concrete instantiation of a fuzzer running against a single PUT under a particular policy:

::: {#def-fuzzer}
###### Fuzzer, Fuzzer Engine
A fuzzer is a program that performs fuzz testing on a PUT.
:::

::: {#def-campaign}
###### Fuzz Campaign
A fuzz campaign is a specific execution of a fuzzer on a PUT with a specific security policy.
:::

During each execution the **bug oracle** decides whether the observed behaviour constitutes a policy violation:

::: {#def-oracle}
###### Bug Oracle
A bug oracle is a component (often inside the fuzzer) that determines whether a given execution of the PUT violates a specific security policy.
:::

In practice, many oracles are based on runtime instrumentation such as fatal POSIX signals (e.g., `SIGSEGV`) or sanitizers like AddressSanitizer (ASan) [@serebryany2012], as used by LibFuzzer [@libfuzzer].

### Seeds, Mutation, and the Seed-Selection Problem

A campaign usually begins with one or more **seeds**---well-formed inputs that belong to the PUT's expected input space. The fuzzer mutates these seeds to explore the larger fuzz input space:

::: {#def-seed}
###### Seed
An input given to the PUT that is mutated by the fuzzer to produce new test cases. During a fuzz campaign ([@def-campaign]) all seeds are stored in a seed *pool* or *corpus*.
:::

Selecting an initial corpus that leads to fast, wide code-coverage is non-trivial and has been studied as the *seed-selection problem* [@rebert2014].

### Taxonomies of Fuzzing

Fuzzers are traditionally classified along two orthogonal dimensions. Namely, in regards to the knowledge of the PUT they have access to and the strategy used for the input generation.

#### Knowledge of the PUT

::: {#def-blackbox}
###### Black-box fuzzer
Operates solely on program binaries, with no knowledge of internal structure; input generation is guided only by external observations.
:::
::: {#def-greybox}
###### Grey-box fuzzer
Gains limited insight---typically lightweight coverage metrics---via instrumentation, allowing more informed mutations while retaining scalability.
:::
::: {#def-whitebox}
###### White-box fuzzer
Has full source-level visibility and employs heavy program analysis (symbolic execution, constraint solving, etc.) to systematically enumerate paths.
:::

#### Test-case Generation Strategy

::: {#def-generational}
###### Generational fuzzing
Produces inputs from a structural model (e.g., a BNF grammar [@backus1959]) or protocol description, ensuring that test-cases are syntactically valid yet semantically diverse.
:::
::: {#def-mutational}
###### Mutational fuzzing
Starts from existing seeds and applies stochastic mutations (bit-flips, block insertions, splice operations). Coverage-guided mutational fuzzers such as AFL have proved especially effective.
:::

These axes can be combined: e.g., AFL [@afl] is a grey-box, mutational fuzzer; Honggfuzz [@honggfuzz] with a grammar description becomes grey-box generational.

### Why Fuzz?

> The purpose of fuzzing relies on the assumption that there are bugs within every program, which are waiting to be discovered. Therefore, a systematic approach should find them sooner or later.
>
> --- OWASP Foundation [@owaspfoundation]

Fuzz testing offers several tangible benefits:

1. **Early vulnerability discovery.** Detecting defects during development is cheaper and safer than addressing exploits in production.
2. **Adversary-parity.** Performing the same randomised stress that attackers employ allows defenders to pre-empt zero-days.
3. **Robustness and correctness.** Beyond security, fuzzing exposes logic errors and stability issues in complex, high-throughput APIs (e.g., decompressors) even when inputs are *expected* to be well-formed.
4. **Regression prevention.** Re-running a corpus of crashing inputs as part of continuous integration ensures that fixed bugs remain fixed.

### Success Stories

*Heartbleed* (CVE-2014-0160) [@heartbleed; @heartbleed-cve] arose from a buffer over-read in OpenSSL [@theopensslproject2025] introduced on 1 February 2012 and unnoticed until 1 April 2014. Post-mortem analyses showed that a simple fuzz campaign exercising the TLS heartbeat extension would have revealed the defect almost immediately [@wheeler2014].

Likewise, the *Shellshock* (or *Bashdoor*) family of bugs in GNU Bash [@bash] enabled arbitrary command execution on many UNIX systems. While the initial flaw was fixed promptly, subsequent bug variants were discovered by Google's Michał Zalewski using fuzzing in late 2014 [@saarinen2014].

On the defensive tooling side, the security tool named *Mayhem*---developed by the company of the same name---has since been adopted by the US Air Force, the Pentagon, Cloudflare, and numerous open-source communities. It has found and facilitated the remediation of thousands of previously unknown vulnerabilities [@simonite2020mayhem].

These cases underscore the central thesis of fuzz testing: exhaustive manual review is infeasible, but scalable stochastic exploration reliably surfaces the critical few defects that matter most.

qqqqqq

### How to Fuzz?

### Fuzzer engines

C/C++: AFL [@afl] & AFL++ [@afl++]. LibFuzzer [@libfuzzer]. [@honggfuzz].

Python: Atheris [@atheris].

> LibFuzzer is an in-process, coverage-guided, evolutionary fuzzing engine. LibFuzzer is linked with the library under test, and feeds fuzzed inputs to the library via a specific fuzzing entrypoint (fuzz target).
  - In-process, coverage-guided, mutation-based fuzzer.

Used to fuzz library functions. The programmer writes a fuzz target to test their implementation.

:::{#def-target}
###### Fuzz target
A function that accepts an array of bytes and does something interesting with these bytes using the API under test [@libfuzzer].

AKA fuzz driver, fuzzer entry point, harness.
:::

Fuzz target structure

- Entry point called repeatedly with mutated inputs.
- Feedback-driven: uses coverage to guide mutations.
- Best for libraries, not full programs.

``` cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  DoSomethingWithData(Data, Size);
  return 0;
}
```

An example of a fuzz target/harness can be seen in [@lst-fuzzing-example] [@libfuzzer].

::: {#lst-fuzzing-example}

```c
cat << EOF > test_fuzzer.cc
#include <stdint.h>
#include <stddef.h>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size > 0 && data[0] == 'H')
    if (size > 1 && data[1] == 'I')
       if (size > 2 && data[2] == '!')
       __builtin_trap();
  return 0;
}
EOF
# Build test_fuzzer.cc with asan and link against libFuzzer.
clang++ -fsanitize=address,fuzzer test_fuzzer.cc
# Run the fuzzer with no corpus.
./a.out
```

A simple function that does something interesting if it receives the input "HI!".
:::

- *American Fuzzy Lop* (AFL) [@afl].
  - Instrumented binaries for edge coverage.
  - Adds more fuzzing strategies, better speed, and QEMU/Unicorn
    support.
  - Superseded by *AFL++* [@aflpp].

AFL fuzzes programs/binaries. The inputs are taken from the `seeds_dir` and their mutations.

``` bash
$ ./afl-fuzz -i seeds_dir -o output_dir -- /path/to/tested/program
```

-   Works on black-box or instrumented binaries.
-   Uses fork-server model for speed.
-   Supports persistent mode, QEMU, and Unicorn modes.

Μπορεί επίσης να χρησιμοποιηθεί για fuzzing βιβλιοθηκών κτλ., απλά αντί για `LLVMFuzzerTestOneInput` έχουμε την `main`.

Μπορεί να χρησιμοποιήσει και `LLVMFuzzerTestOneInput` harnesses.

OSS-Fuzz: 2016, after heartbleed.

### Difficulties

- Relatively unknown practice, especially compared to TDD
- Upfront cost of writing harnesses
- Cost of examining and evaluating crashes

## Large Language Models (LLMs)

Transformers [@vaswani2023], 2017--2025. ChatGPT/OpenAI history & context. Claude, Llama (1--3) etc.

### What are they?

[@li2022] Transformers [@vaswani2023]

### Biggest GPTs

- Closed-source ChatGPT, Claude, Gemini [@chatgpt; @claude; @gemini]
- Open-source (i.e. open-weights)

Llama{1,..,3}, Deepseek [@grattafiori2024; @deepseek-ai2025]

### Prompting {#sec-prompting}

- Zero-shot
- Few-shot [@brown2020]
- RAG [@lewis2021]
- chain of thought [@chainofthought]
- tree of thought [@yao2023]
- reAct [@reAct]

Comparison, strengths weaknesses etc. [@laban2025].

### For coding

LLM-assisted IDEs [@cursor; @ghcopilot; @chen2021] Vibecoding [@sarkar2025]

### For fuzzing

They don\'t work

The above problems can be solved with NS AI

[@perry2023]

### LLM Programming Libraries (?)

Langchain & LangGraph, LlamaIndex [@langchain;@langgraph;@llamaindex]. DSPy [@dspy].

Comparison, relevance to our usecase.

## Neurosymbolic AI

[TODO]{.mark} [@ganguly2024; @garcez2020; @gaur2023; @grov2024; @sheth2023; @tilwani2024].

### What is it?

[@sheth2023; @gaur2023] Neurosymbolic AI for attribution in LLMs [@tilwani2024]

### What does it solve?

### Its state

restatement of overarching goal, segue to section 2
