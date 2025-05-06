\pagenumbering{arabic}

# Introduction

{{<lipsum 1 >}} [@manesArtScienceEngineering2019;@yaoTreeThoughtsDeliberate2023].

{{<lipsum 6 >}}^[testing footnotes].

## Neurosymbolic AI

::: {#lst-test}
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

{{<lipsum 4 >}}

## Large Language Models (LLMs)

{{<lipsum 5 >}}
