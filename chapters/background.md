# Background

## Fuzzing

What is fuzzing [@manes2019].

terminology: fuzz campaign, harness, driver, target, corpus

Why fuzz?

### Fuzzing examples

Heartbleed [@heartbleed], shellshock [@meyer2013].

### Fuzzer engines

C/C++: AFL [@afl] & AFL++ [@afl++]. LibFuzzer [@libfuzzer].

Python: Atheris [@atheris].

Java, Rust etc...

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

OSS-Fuzz: 2016, after heartbleed.

## Large Language Models (LLMs)

Transformers [@vaswani2023], 2017--2025. ChatGPT/OpenAI history & context. Claude, Llama (1--3) etc.

### Prompting {#sec-prompting}

Prompting techniques.

1. Zero-shot.
2. One-shot.
3. Chain of Thought [@chainofthought].
4. ReACt [@reAct].
5. Tree of Thoughts [@yao2023].

Comparison, strengths weaknesses etc. [@laban2025].

### LLM Programming Libraries (?)

Langchain & LangGraph, LlamaIndex [@langchain;@langgraph;@llamaindex]. DSPy [@dspy].

Comparison, relevance to our usecase.

## Neurosymbolic AI

[TODO]{.mark} [@ganguly2024; @garcez2020; @gaur2023; @grov2024; @sheth2023; @tilwani2024].
