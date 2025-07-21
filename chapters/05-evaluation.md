# Evaluation {#sec-eval}

To thoroughly assess the performance and effectiveness of OverHAuL, we established four *research questions* to direct our investigative efforts. These questions are designed to provide a structured framework for our inquiry and to ensure that our research remains focused on the key aspects of OverHAuL's functionality and impact within its intended domain. By addressing these questions, we aim to uncover valuable insights that will contribute to a deeper understanding of OverHAuL's capabilities and its position in contemporary automatic fuzzing applications:

- **RQ1**: Can OverHAuL generate working harnesses for unfuzzed C projects?

- **RQ2**: What characteristics do these harnesses have? Are they similar to man-made harnesses?

- **RQ3**: How do LLM usage patterns influence the generated harnesses?

- **RQ4**: How do different symbolic techniques affect the generated harnesses?

## Experimental Benchmark {#sec-benchmark}

To evaluate OverHAuL, a benchmarking script was implemented^[<https://github.com/kchousos/OverHAuL/blob/master/benchmarks/benchmark.sh>] and a corpus of ten open-source C libraries was assembled. This collection comprises of: Firstly, GitHub user dhvar's dateparse library, which is also used as a running example in OSS-Fuzz-Gen's [@oss-fuzz-gen] experimental from-scratch harnessing feature (@sec-ofg). Secondly, nine other libraries chosen randomly^[From the subset of libraries that do not have exotic external dependencies, like the X11 development toolchain.] from the package catalog of Clib, a "package manager for the C programming language" [@clibs; @clib]. All libraries can be seen @tbl-projects, along with their descriptions.

::: {#tbl-projects fig-scap='Benchmark corpus'}

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
