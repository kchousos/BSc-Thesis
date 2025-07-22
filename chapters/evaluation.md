# Evaluation {#sec-eval}

To thoroughly assess the performance and effectiveness of OverHAuL, we established four *research questions* to direct our investigative efforts. These questions are designed to provide a structured framework for our inquiry and to ensure that our research remains focused on the key aspects of OverHAuL's functionality and impact within its intended domain. By addressing these questions, we aim to uncover valuable insights that will contribute to a deeper understanding of OverHAuL's capabilities and its position in contemporary automatic fuzzing applications:

- **RQ1**: Can OverHAuL generate working harnesses for unfuzzed C projects?

- **RQ2**: What characteristics do these harnesses have? Are they similar to man-made harnesses?

- **RQ3**: How do LLM usage patterns influence the generated harnesses?

- **RQ4**: How do different symbolic techniques affect the generated harnesses?

## Experimental Benchmark {#sec-benchmark}

To evaluate OverHAuL, a benchmarking script was implemented^[Available at <https://github.com/kchousos/OverHAuL/blob/master/benchmarks/benchmark.sh>.] and a corpus of ten open-source C libraries was assembled. This collection comprises firstly of user dhvar's "dateparse" library, which is also used as a running example in OSS-Fuzz-Gen's [@oss-fuzz-gen] experimental from-scratch harnessing feature (@sec-ofg). Secondly, nine other libraries chosen randomly^[From the subset of libraries that do not have exotic external dependencies, like the X11 development toolchain.] from the package catalog of Clib, a "package manager for the C programming language" [@clibs; @clib]. All libraries can be seen @tbl-projects, along with their descriptions. 

OverHAuL was evaluated through the experimental benchmark from 6th of June, 2025 to 18th of July, 2025, using OpenAI's gpt-4.1-mini model [@openaidocs2025]. For these runs, each OverHAuL execution was configured with a 5 minute harness execution timeout and an iteration budget of 10. Each benchmark run was executed as a GitHub Actions workflow on Linux virtual machines with 4-vCPUs and 16GiB of memory hosted on Microsoft Azure [@githubdocs2025a; @githubdocs2025]. The result directory (described in @sec-local) for each is available as a downloadable artifact in the corresponding GitHub Actions entry. 

::: {#tbl-projects fig-scap='Benchmark corpus' tbl-colwidths="[25,60,7,8]"}

| Project                                                             | Description                                                                | Stars | SLOC |
|:--------------------------------------------------------------------|:---------------------------------------------------------------------------|------:|-----:|
| [dvhar/dateparse](https://github.com/dvhar/dateparse)               | A library that allows parsing dates without knowing the format in advance. |     2 | 2272 |
| [clibs/buffer](https://github.com/clibs/buffer)                     | A string manipulation library.                                             |   204 |  354 |
| [jwerle/libbeaufort](https://github.com/jwerle/libbeaufort)         | A library implementation of the Beaufort cipher [@franksen1993].           |    13 |  321 |
| [jwerle/libbacon](https://github.com/jwerle/libbacon)               | A library implementation of the Baconian cipher [@bacon1861].              |     8 |  191 |
| [jwerle/chfreq.c](https://github.com/jwerle/chfreq.c)               | A library for computing the character frequency in a string.               |     5 |   55 |
| [jwerle/progress.c](https://github.com/jwerle/progress.c)           | A library for displaying progress bars in the terminal.                    |    76 |  357 |
| [willemt/cbuffer](https://github.com/willemt/cbuffer)               | A circular buffer implementation.                                          |   261 |  170 |
| [willemt/torrent-reader](https://github.com/willemt/torrent-reader) | A torrent-file reader library.                                             |     6 |  294 |
| [orangeduck/mpc](https://github.com/orangeduck/mpc)                 | A type-generic parser combinator library.                                  | 2,753 | 3632 |
| [h2non/semver.c](https://github.com/h2non/semver.c)                 | A semantic version v2.0 parsing and rendering library [@semver].           |   190 |  608 |

The benchmark project corpus. Each project name links to its corresponding GitHub repository. Each is followed by a short description and its GitHub stars count, as of July 18th, 2025.
:::

### Local Benchmarking {#sec-local}

To run the benchmark locally, one would need to follow the installation instructions in @sec-install and then execute the benchmarking script, like so:

```text
$ ./benchmarks/benchmark.sh
```

The cloned repositories with their corresponding harnesses will then be located in a subdirectory of `benchmark_results`, which will have the name format of `mini__<timestamp>__ReAct__<llm-model>__<max-exec-time>__<iter-budget>`. "Mini" corresponds to the benchmark project corpus described above, since a 30-project corpus was initially created and is now coined as "full" benchmark. Both the mini and full benchmarks are located in `benchmarks/repos.txt` and `benchmarks/repos-mini.txt` respectively. To execute the benchmark for the "full" corpus, users can add the `-b full` flag in the script's invocation. Also, the LLM model used can be defined with the `-m` command-line flag.

## Results {#sec-results}

In @fig-results, the results of the aforementioned benchmark runs are showcased.

:::{#fig-results}
![](../resources/results.png){fig-scap='Benchmark Results'}

The benchmark results for OverHAuL are illustrated with the $y$-axis depicting the ten-project corpus outlined in @sec-benchmark. The $x$-axis represents the various benchmark runs. Each label constitutes a unique hash identifier corresponding to a specific GitHub Actions workflow run, which can be accessed at <https://github.com/kchousos/OverHAuL/actions/runs/HASH>. An overview of all benchmark runs is available at <https://github.com/kchousos/OverHAuL/actions/workflows/benchmarks.yml>. In this matrix, a green/1 block indicates that OverHAuL successfully generated a new harness for the project and was able to find a crash input. On the other hand, an orange/0 block indicates that while a compilable harness was produced, no crash input was found within the five-minute execution period. Importantly, there are no red/-1 blocks, which would indicate cases where a compilable harness could not be generated.
:::

### RQ 1: Can OverHAuL generate working harnesses for unfuzzed C projects?

We can deduce the following facts from @fig-results: Firstly, OverHAuL has a very high success rate in finding crash inputs for the given programs, specifically one of **92.5%**. Secondly, although according strictly to these results OverHAuL never generates an un-compilable harness, we can err on the side of caution and infer that OverHAuL not being able to generate a compilable harness is a rare occurrence. These conclusions can safely answer RQ1 with a resounding yes.

### RQ2: What characteristics do these harnesses have? Are they similar to man-made harnesses?

From sampling OverHAuL's generated harnesses, the answer to RQ2 remains unclear. Most of the time, the fuzz targets that are produced are understandable and similar to something a software engineer might program. Take for example @lst-sample-dateparse. Nonetheless, sometimes generated harnesses contain usage of inexplicable or arbitrary constants and peculiar control flow checks. This makes them harder to understand and quite possibly incorrect in many cases, thus diverging from seeming human-written. RQ2's answer remains an unclear "it depends", given the variance in OverHAuL's results.

::: {#lst-sample-dateparse fig-scap='Sample dateparse harness'}
```C
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "dateparse.h"

// No artificial size limit to allow fuzzer to explore full input size for boundaries

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Allocate buffer with extra byte for null termination
    char *input_str = (char *)malloc(size + 1);
    if (!input_str) {
        return 0;
    }

    memcpy(input_str, data, size);
    input_str[size] = '\0';

    date_t parsed_date = 0;
    int offset = 0;

    // Array of string lengths targeting boundary conditions (including 0 = internal strlen)
    size_t test_lens[] = {0, size, size > 0 ? size - 1 : 0, 12, 13, 14};

    for (size_t i = 0; i < sizeof(test_lens) / sizeof(test_lens[0]); i++) {
        size_t len = test_lens[i];
        if (len <= size) {
            dateparse(input_str, &parsed_date, &offset, (int)len);
        }
    }

    free(input_str);
    return 0;
}
```

Sample harness for dateparse, generated by OverHAuL.
:::

### RQ3: How do LLM usage patterns influence the generated harnesses?

In exploring the utilization of LLMs, two critical dimensions warrant examination: the selection of the LLM model itself and the prompting techniques employed. Within the context of model selection, all benchmark tests conducted on GitHub's infrastructure utilized OpenAI's gpt-4.1-mini. Additionally, early local testing involved gpt-4.1, gpt-4o, gpt-4, and gpt-3.5-turbo. The results indicate that both gpt-4.1 and gpt-4.1-mini demonstrated comparable positive outcomes, while gpt-4o produced semi-average results. In contrast, gpt-4 and gpt-3.5-turbo exhibited significantly poorer performance, averaging approximately 2 out of 10 successfully harnessed projects per benchmark run. For these reasons, subpar-performing models were rejected early in development. This underscores the considerable impact that the size and capabilities of the underlying LLM model have on OverHAuL's effectiveness. Consequently, gpt-4o emerges as a contemporary cut-off point in LLM development concerning OverHAuL's performance, suggesting that advancements in LLM technologies will likely enhance OverHAuL's capabilities rapidly.

Regarding the prompting techniques adopted, ReAct prompting has yielded the most favorable outcomes in the current version of OverHAuL [@reAct]. As detailed in @sec-abandoned, both zero-shot prompting and Chain-of-Thought (COT) prompting [@chainofthought] produced similarly unsatisfactory results. A primary challenge in automatic harness generation is ensuring that the generated harness aligns with real-world conditions, particularly in terms of compilation success and effective runtime behavior. This alignment can only be validated through LLM--environment interaction, i.e. within agentic workflows [@giannone2025]. Furthermore, the superior results associated with ReAct prompting can be attributed to its inherent capacity for more sophisticated code exploration.

In summary, the response to RQ3 comes to be that ongoing advancements in LLM models will enable systems like OverHAuL to generate increasingly effective outcomes. Additionally, architectures that incorporate agentic modules capable of environment assessment and feedback gathering will surpass more traditional applications of LLMs, particularly in the domain of automatic fuzzing.

### RQ4: How do different symbolic techniques affect the generated harnesses?

Throughout the development of OverHAuL and its various iterations, numerous programming techniques were assessed in pursuit of answering RQ4 (@sec-abandoned). Simple source code concatenation and its subsequent injection into LLM prompts revealed significant limitations, primarily due to the constraints of context windows. Conversely, the usage of tools capable of retrieving file contents marked a meaningful advancement. Nonetheless, this approach still encountered challenges, such as inaccessible code blocks and exploration that lacked semantic relevance. In response to these difficulties, the implementation of a function-level vector store functioning as a codebase oracle is proposed as a highly scalable solution. This strategy not only enhances the organization of larger files but also accommodates expanding project sizes, facilitating more semantically meaningful code examination.

## Discussion

As discussed in Section @sec-results, the capabilities and effectiveness of OverHAuL are closely tied to the choice of the underlying large language model. OverHAuL's modular architecture ensures that advances in LLM research will directly enhance its performance. Each release of a new, more capable model can be readily integrated, thereby amplifying OverHAuL's effectiveness without the need for substantial redesign.

A noteworthy consideration in our benchmarking setup is the possibility that some of the open-source libraries evaluated may have been included in the LLM's training data. This introduces a risk of overestimating OverHAuL's performance on code that is unseen or proprietary. Results for closed-source or less widely available libraries could therefore be weaker. Nonetheless, this potential limitation can theoretically be addressed through targeted fine-tuning of the LLM [@openaidocs2025b; @kim2025].

### Threats to Validity

Our evaluation of OverHAuL was conducted on ten relatively obscure open-source C libraries representing a range of application domains and functionalities. While this selection reduces the likelihood that these projects were used in LLM training and thus minimizes potential bias, it remains uncertain how transferable our results are to larger, more complex, or structurally different codebases. Factors such as varying design paradigms, architectural patterns, or real-world deployment contexts may pose new challenges for OverHAuL's scalability and effectiveness. 

Additionally, the risk that LLMs could hallucinate constitutes an internal threat to validity. Such hallucinations may require multiple attempts or occasional manual adjustments to produce valid and useful fuzz drivers. However, because LLMs---and thus OverHAuL---operate in a non-deterministic manner, it is possible to rerun the process and obtain alternative results. The inherent stochasticity of the underlying LLMs thus allows users to recover from initial failures, ensuring that the impact of hallucinations remains limited to efficiency rather than undermining the core applicability of the approach.

In summary, while our findings demonstrate the potential of OverHAuL, they also highlight important limitations and directions for future work, especially in improving robustness and evaluating performance across a broader spectrum of software projects.
