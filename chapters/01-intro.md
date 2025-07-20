\pagenumbering{arabic}

# Introduction

Modern society's reliance on software systems continues to grow, particularly in mission-critical environments such as healthcare, aerospace, and industrial infrastructure. The reliability of these systems is crucial---failures or vulnerabilities can lead to severe financial losses and even endanger lives. A significant portion of this foundational software is still written in C, a language created by Dennis Ritchie in 1972 [@kernighan1978; @ritchie1978]. Although C has been instrumental in the evolution of software, its minimal safeguards---especially around memory management---are notorious. Memory safety bugs remain a persistent vulnerability, and producing provably safe code in C is exceptionally challenging, as evidenced by the stringent guidelines required by organizations like NASA for safety-critical applications [@holzmann2006].

To address these challenges, programming languages with built-in memory safety features, such as Ada and Rust, have been introduced [@adadevelopers2022; @rustprojectdevelopers2025]. Nevertheless, no language offers absolute immunity from vulnerabilities. In addition, much of the global software infrastructure remains written in memory-unsafe languages, with C-based codebases unlikely to disappear in the near future. Ultimately, the potential for human error grows in tandem with increasing software complexity, meaning software is only as safe as its weakest link.

The advent of Large Language Models (LLMs) has profoundly influenced software development. Developers now regularly use LLMs for code generation, refactoring, and documentation assistance. While these models exhibit impressive capabilities, they can still introduce subtle mistakes [@perry2023]. As LLM-generated code becomes more pervasive, so does the likelihood of unnoticed software errors escaping traditional human review.

Within this landscape, the need to detect vulnerabilities and ensure software quality is more urgent than ever. Fuzzing---a technique that generates and executes large numbers of test cases to find bugs---has become a critical method for discovering memory safety violations. Despite extensive advances in automating fuzzing, significant hurdles remain. Most current fuzzers require pre-existing test harnesses [@oss-fuzz-gen] or depend on sample client code to exercise the target program [@utopia; @fuzzgen; @fudge]. Often, these tools still rely on developers for integration or final evaluation, leaving parts of the process manual and incomplete. The application of LLMs to harness generation and end-to-end fuzzing remains a developing field.

This thesis aims to push the boundaries of fuzzing automation by harnessing the code synthesis and reasoning strengths of modern LLMs. We introduce OverHAuL, a system that accepts a bare and previously unfuzzed C project, utilizes LLM agents to author a new fuzzing harness from scratch, and evaluates its efficacy in a closed iterative feedback loop. This end-to-end approach is designed to minimize manual effort and accelerate vulnerability detection in C codebases.

## Thesis Structure

The thesis first presents foundational concepts (@sec-background), followed by a comprehensive survey of existing work in automated fuzzing (@sec-related). We demonstrate that most current fuzzing systems either rely on pre-existing harnesses or employ client code, often leaving validation and integration tasks to the user. We then introduce the OverHAuL system, detailing its architecture, the novel techniques used in its implementation, and their contributions to advancing automated harness generation (@sec-overhaul). Finally, we assemble a benchmark dataset of ten open-source C projects and rigorously evaluate OverHAuL's performance ([@sec-eval;@sec-results]).

## Summary of Contributions

This thesis presents the following key contributions:

1. A comprehensive, up-to-date survey of leading LLM-driven automated fuzzing tools, detailing their respective strengths and limitations.
2. The introduction of OverHAuL, a novel framework that enables fully automated, end-to-end fuzzing harness generation using large language models (LLMs).
3. Empirical validation through benchmark experiments, demonstrating that OverHAuL successfully generates effective fuzzing harnesses in 92.5% of tested cases.
4. Full open sourcing of all research artifacts, datasets, and code at <https://github.com/kchousos/OverHAuL> to encourage further research and ensure reproducibility.

This work aims to advance the use of LLMs in automated software testing, particularly for legacy codebases where building harnesses by hand is impractical or costly. By doing so, we strive to enhance software security and reliability in sectors where correctness is imperative.
