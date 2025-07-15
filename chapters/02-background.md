# Background

## Fuzz Testing

*Fuzzing* is an automated software-testing technique in which a *Program Under Test* (PUT) is executed with (pseudo-)random inputs in the hope of exposing undefined behavior. When such behavior manifests as a crash, hang, or memory-safety violation, the corresponding input constitutes a *test-case* that reveals a bug and often a vulnerability [@manes2019]. In essence, fuzzing is a form of adversarial, penetration-style testing carried out by the defender before the adversary has an opportunity to do so. Interest in the technique surged after the publication of three practitioner-oriented books in 2007--2008 [@takanen2018; @sutton2007; @rathaus2007].

Historically, the term was coined by Miller et al. in 1990, who used "fuzz" to describe a program that "generates a stream of random characters to be consumed by a target program" [@miller1990]. This informal usage captured the essence of what fuzzing aims to do: stress test software by bombarding it with unexpected inputs to reveal bugs. To formalize this concept, we adopt Manes et al.'s rigorous definitions [@manes2019]:

::: {#def-fuzzing}
###### Fuzzing
Fuzzing is the execution of a Program Under Test (PUT) using input(s) sampled from an input space (the *fuzz input space*) that protrudes the expected input space of the PUT.
:::

This means fuzzing involves running the target program on inputs that go beyond those it is typically designed to handle, aiming to uncover hidden issues. An individual instance of such execution---or a bounded sequence thereof---is called a *fuzzing run*. When these runs are conducted systematically and at scale with the specific goal of detecting violations of a security policy, the activity is known as *fuzz testing* (or simply *fuzzing*):

::: {#def-fuzz-testing}
###### Fuzz Testing
Fuzz testing is the use of fuzzing to test whether a PUT violates a security policy.
:::

This distinction highlights that fuzz testing is fuzzing with an explicit focus on security properties and policy enforcement. Central to managing this process is the *fuzzer engine*, which orchestrates the execution of one or more fuzzing runs as part of a *fuzz campaign*. A fuzz campaign represents a concrete instance of fuzz testing tailored to a particular program and security policy:

::: {#def-fuzzer}
###### Fuzzer, Fuzzer Engine
A fuzzer is a program that performs fuzz testing on a PUT.
:::

::: {#def-campaign}
###### Fuzz Campaign
A fuzz campaign is a specific execution of a fuzzer on a PUT with a specific security policy.
:::

Throughout each execution within a campaign, a *bug oracle* plays a critical role in evaluating the program's behavior to determine whether it violates the defined security policy:

::: {#def-oracle}
###### Bug Oracle
A bug oracle is a component (often inside the fuzzer) that determines whether a given execution of the PUT violates a specific security policy.
:::

In practice, bug oracles often rely on runtime instrumentation techniques, such as monitoring for fatal POSIX signals (e.g., `SIGSEGV`) or using sanitizers like AddressSanitizer (ASan) [@serebryany2012]. Tools like LibFuzzer [@libfuzzer] commonly incorporate such instrumentation to reliably identify crashes or memory errors during fuzzing.

Most fuzz campaigns begin with a set of *seeds*---inputs that are well-formed and belong to the PUT's expected input space---called a *seed corpus*. These seeds serve as starting points from which the fuzzer generates new test cases by applying transformations or mutations, thereby exploring a broader input space:

::: {#def-seed}
###### Seed
An input given to the PUT that is mutated by the fuzzer to produce new test cases. During a fuzz campaign ([@def-campaign]) all seeds are stored in a seed *pool* or *corpus*.
:::

The process of selecting an effective initial corpus is crucial because it directly impacts how quickly and thoroughly the fuzzer can cover the target program's code. This challenge---studied as the *seed-selection problem*---involves identifying seeds that enable rapid discovery of diverse execution paths and is non-trivial [@rebert2014]. A well-chosen seed set often accelerates bug discovery and improves overall fuzzing efficiency.

### Taxonomies of Fuzzing

To better understand fuzzers, researchers traditionally classify them along two orthogonal axes: the level of knowledge about the PUT that they possess, and the strategy they use to generate test inputs.

#### Knowledge of the PUT {.unnumbered}

Fuzzers differ in how much information they leverage about the program under test:

::: {#def-blackbox}
###### Black-box fuzzer
Operates solely on program binaries, with no knowledge of internal structure; input generation is guided only by external observations.
:::

Black-box fuzzers treat the PUT as a black box, generating inputs without insights into program internals. This makes them simple but often less efficient in uncovering deep bugs.

::: {#def-greybox}
###### Grey-box fuzzer
Gains limited insight---typically lightweight coverage metrics---via instrumentation, allowing more informed mutations while retaining scalability.
:::

Grey-box fuzzers strike a balance by collecting partial information, such as execution coverage via lightweight instrumentation, enabling more targeted input mutations that improve effectiveness.

::: {#def-whitebox}
###### White-box fuzzer
Has full source-level visibility and employs heavy program analysis (symbolic execution, constraint solving, etc.) to systematically enumerate paths.
:::

White-box fuzzers exploit full program knowledge, using advanced techniques like symbolic execution to methodically explore program paths, but often at the cost of reduced scalability.

#### Test-case Generation Strategy {.unnumbered}

The second axis concerns how fuzzers generate test inputs:

::: {#def-generational}
###### Generational fuzzing
Produces inputs from a structural model or protocol description, ensuring that test-cases are syntactically valid yet semantically diverse.
:::

Generational fuzzing leverages knowledge of input formats (e.g., a BNF grammar [@backus1959]) to produce well-formed test cases derived from formal specifications or models, improving the likelihood of meaningful program behavior.

::: {#def-mutational}
###### Mutational fuzzing
Starts from existing seeds and applies stochastic mutations (bit-flips, block insertions, splice operations). Coverage-guided mutational fuzzers such as AFL have proved especially effective.
:::

Mutational fuzzing begins with seeds and applies random or guided mutations to explore nearby input space regions. Techniques like coverage-guided fuzzing have greatly enhanced the efficiency of this approach.

These two dimensions are often combined to tailor fuzzers to specific scenarios. For example, AFL [@afl] is a grey-box, mutational fuzzer that uses coverage feedback to guide input mutations, while Honggfuzz [@honggfuzz] can operate as a grey-box generational fuzzer when provided with grammar-based input models. This flexibility allows fuzzers to adapt to varied testing goals and program characteristics.

### Motivation

> The purpose of fuzzing relies on the assumption that there are bugs within every program, which are waiting to be discovered. Therefore, a systematic approach should find them sooner or later.
>
> --- OWASP Foundation [@owaspfoundation]

Fuzz testing offers several tangible benefits:

1. **Early vulnerability discovery**: Detecting defects during development is cheaper and safer than addressing exploits in production.
2. **Adversary-parity**: Performing the same randomised stress that attackers employ allows defenders to pre-empt zero-days.
3. **Robustness and correctness**: Beyond security, fuzzing exposes logic errors and stability issues in complex, high-throughput APIs (e.g., decompressors) even when inputs are *expected* to be well-formed.
4. **Regression prevention**: Re-running a corpus of crashing inputs as part of continuous integration ensures that fixed bugs remain fixed.

#### Success Stories

*Heartbleed* (CVE-2014-0160) [@heartbleed; @heartbleed-cve] arose from a buffer over-read^[<https://xkcd.com/1354/>] in OpenSSL [@theopensslproject2025] introduced on 1 February 2012 and unnoticed until 1 April 2014. Post-mortem analyses showed that a simple fuzz campaign exercising the TLS heartbeat extension would have revealed the defect almost immediately [@wheeler2014].

Likewise, the *Shellshock* (or *Bashdoor*) family of bugs in GNU Bash [@bash] enabled arbitrary command execution on many UNIX systems. While the initial flaw was fixed promptly, subsequent bug variants were discovered by Google's Michał Zalewski using his own fuzzer [@afl] in late 2014 [@saarinen2014].

On the defensive tooling side, the security tool named *Mayhem*---developed by the company of the same name---has since been adopted by the US Air Force, the Pentagon, Cloudflare, and numerous open-source communities. It has found and facilitated the remediation of thousands of previously unknown vulnerabilities [@simonite2020mayhem].

These cases underscore the central thesis of fuzz testing: exhaustive manual review is infeasible, but scalable stochastic exploration reliably surfaces the critical few defects that matter most.

### Methodology

As previously discussed, fuzz testing of a program under test (PUT) is typically conducted using a dedicated fuzzing engine (see [@def-fuzzer]). Among the most widely adopted fuzzers for C and C++ projects and libraries are AFL [@afl]---which has since evolved into AFL++ [@aflpp]---and LibFuzzer [@libfuzzer]. Within the OverHAuL framework, LibFuzzer is preferred owing to its superior suitability for library fuzzing, whereas AFL++ predominantly targets executables and binary fuzzing.

#### LibFuzzer

LibFuzzer [@libfuzzer] is an in-process, coverage-guided evolutionary fuzzing engine primarily designed for testing libraries. It forms part of the LLVM ecosystem [@llvm] and operates by linking directly with the library under evaluation. The fuzzer delivers mutated input data to the library through a designated fuzzing entry point, commonly referred to as the *fuzz target*.

:::{#def-target}
###### Fuzz target
A function that accepts a byte array as input and exercises the application programming interface (API) under test using these inputs [@libfuzzer]. This construct is also known as a *fuzz driver*, *fuzzer entry point*, or *fuzzing harness*.
:::

For the remainder of this thesis, the terms presented in @def-target will be used interchangeably.

To effectively validate an implementation or library, developers are required to author a fuzzing harness that invokes the target library's API functions utilizing the fuzz-generated inputs. This harness serves as the principal interface for the fuzzer and is executed iteratively, each time with mutated input designed to maximize code coverage and uncover defects. To comply with LibFuzzer's interface requirements, a harness must conform to the following function signature:

::: {#lst-basic-example}

```c
int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  DoSomethingInterestingWithData(Data, Size);
  return 0;
}
```

This function receives the fuzzing input via a pointer to an array of bytes (`Data`) and its associated size (`Size`). Efficiency in fuzzing is achieved by invoking the API of interest within the body of this function, thereby allowing the fuzzer to explore a broad spectrum of behavior through systematic input mutation.
:::

A more illustrative example of such a harness is provided in [@lst-fuzzing-example].

::: {#lst-fuzzing-example}

```cpp
// test_fuzzer.cpp
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size > 0 && data[0] == 'H')
    if (size > 1 && data[1] == 'I')
      if (size > 2 && data[2] == '!')
        __builtin_trap();
  return 0;
}
```

This example demonstrates a minimal harness that triggers a controlled crash upon receiving `HI!` as input.
:::

To compile and link such a harness with LibFuzzer, the Clang compiler---also part of the LLVM project [@llvm]---must be used alongside appropriate compiler flags. For instance, compiling the harness in [@lst-fuzzing-example] can be achieved as follows:

::: {#lst-harness-compilation}

```sh
# Compile test_fuzzer.cc with AddressSanitizer and link against LibFuzzer.
clang++ -fsanitize=address,fuzzer test_fuzzer.cc
# Execute the fuzzer without any pre-existing seed corpus.
./a.out
```

This example illustrates the compilation and execution workflow necessary for deploying a LibFuzzer-based fuzzing harness.
:::

#### AFL and AFL++

*American Fuzzy Lop* (AFL) [@afl], developed by Michał Zalewski, is a seminal fuzzer targeting C and C++ applications. Its core methodology relies on instrumented binaries to provide edge coverage feedback, thereby guiding input mutation towards unexplored program paths. AFL supports several emulation backends including QEMU [@bellard2025]---an open-source CPU emulator facilitating fuzzing on diverse architectures---and Unicorn [@unicornengine2025], a lightweight multi-platform CPU emulator. While AFL established itself as a foundational tool within the fuzzing community, its successor AFL++ [@aflpp] incorporates numerous enhancements and additional features to improve fuzzing efficacy.

AFL operates by ingesting seed inputs from a specified directory (`seeds_dir`), applying mutations, and then executing the target binary to discover novel execution paths. Execution can be initiated using the following command-line syntax:

```bash
./afl-fuzz -i seeds_dir -o output_dir -- /path/to/tested/program
```

AFL is capable of fuzzing both black-box and instrumented binaries, employing a fork-server mechanism to optimize performance. It additionally supports persistent mode execution as well as modes leveraging QEMU and Unicorn emulators, thereby providing extensive flexibility for different testing environments.

Although AFL is traditionally utilized for fuzzing standalone programs or binaries, it is also capable of fuzzing libraries and other software components. In such scenarios, rather than implementing the `LLVMFuzzerTestOneInput` style harness, AFL can use the standard `main()` function as the fuzzing entry point. Nonetheless, AFL also accommodates integration with `LLVMFuzzerTestOneInput`-based harnesses, underscoring its adaptability across varied fuzzing use cases.

### Challenges in Adoption

Despite its potential for uncovering software vulnerabilities, fuzzing remains a relatively underutilized testing technique compared to more established methodologies such as Test-Driven Development (TDD). This limited adoption can be attributed, in part, to the substantial initial investment required to design and implement appropriate test harnesses that enable effective fuzzing processes. Furthermore, the interpretation of fuzzing outcomes---particularly the identification, diagnostic analysis, and prioritization of program crashes---demands considerable resources and specialized expertise. These factors collectively pose significant barriers to the widespread integration of fuzzing within standard software development and testing practices.

## Large Language Models (LLMs)

qqqqqqq

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
