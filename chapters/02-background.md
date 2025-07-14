# Background

## Fuzzing

Introduced in 1990 [@miller1990].

Discovering vulnerabilities in the development stage instead of in production.

Discovering vulnerabilities ourselves before attackers do.

Borrowing definitions from [@manes2019]:

Goal: trigger unexpected behavior (e.g., crashes, hangs, memory errors).



> The purpose of fuzzing relies on the assumption that there are bugs within every program, which are waiting to be discovered. Therefore, a systematic approach should find them sooner or later.
>
> --- [OWASP Foundation](https://owasp.org/www-community/Fuzzing)


Fuzz testing is valuable for:

1. Software that receives inputs from untrusted sources (security)
2. Sanity checking the equivalence of two complex algorithms (correctness)
3. Verifying the stability of a high-volume API that takes complex inputs (stability), e.g. a decompressor, even if all the inputs are trusted.


::: {#def-fuzzing}
#### Fuzzing
Fuzzing is the execution of a Program Under Test (PUT) using input(s) sampled from an input space (the "fuzz input space") that protrudes the expected input space of the PUT.
:::

::: {#def-fuzz-testing}
#### Fuzz Testing
Fuzz testing is the use of fuzzing to test if a PUT violates a security policy.
:::

::: {#def-fuzzer}
#### Fuzzer
A fuzzer is a program that performs fuzz testing on a PUT.
:::

::: {#def-campaign}
#### Fuzz Campaign
A fuzz campaign is a specific execution of a fuzzer on a PUT with a specific security policy.
:::

::: {#def-oracle}
#### Bug Oracle
A bug oracle is a program, perhaps as part of a fuzzer, that determines whether a given execution of the PUT violates a specific security policy.
:::

::: {#def-blackbox}
#### Black-box fuzzer
A black-box fuzzer is a testing tool that inputs random or specified data into a software application without knowledge of its internal workings, aiming to uncover vulnerabilities or bugs by observing the program's behavior in response to various inputs.
:::

::: {#def-whitebox}
#### White-box fuzzer
A white-box fuzzer is a testing tool that analyzes the internal structure and logic of a program to generate test inputs. It uses knowledge of the code, such as control flow and data paths, to systematically explore all possible execution paths and identify vulnerabilities more effectively.
:::

::: {#def-greybox}
#### Grey-box fuzzer
A grey-box fuzzer is a testing tool that combines aspects of both black-box and white-box fuzzing. It has limited knowledge of the internal workings of the application, often using some code coverage information or program analysis to generate more targeted inputs, thereby improving the efficiency of vulnerability detection.
:::

::: {#def-generational}
#### Generational fuzzing
Generationbased fuzzers produce test cases based on a given model that describes the inputs expected by the PUT, e.g. a Backus--Naur form (BNF) grammar [@backus1959].
:::

::: {#def-mutational}
#### Mutational fuzzing
mutation-based fuzzers produce test cases by mutating a given seed input.
:::

terminology: fuzz campaign [@def-campaign], harness, driver, target, corpus

Why fuzz?

### Fuzzing success stories

- Heartbleed vulnerability, OpenSSL[@heartbleed] ([CVE-2014-0160](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2014-0160))
  - Easily found with fuzzing ⇒ Preventable
- Shellshock vulnerabilities, Bash ([CVE-2014-6271](https://nvd.nist.gov/vuln/detail/CVE-2014-6271))
- [Mayhem](https://www.mayhem.security/) (FKA ForAllSecure) [@simonite2020mayhem]
  1.  Cloudflare
  2.  OpenWRT

### Fuzzer engines

C/C++: AFL [@afl] & AFL++ [@afl++]. LibFuzzer [@libfuzzer]. [@honggfuzz].

Python: Atheris [@atheris].

> LibFuzzer is an in-process, coverage-guided, evolutionary fuzzing engine. LibFuzzer is linked with the library under test, and feeds fuzzed inputs to the library via a specific fuzzing entrypoint (fuzz target).
  - In-process, coverage-guided, mutation-based fuzzer.

Used to fuzz library functions. The programmer writes a fuzz target to test their implementation.

:::{#def-target}
#### Fuzz target
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
