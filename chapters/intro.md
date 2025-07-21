\pagenumbering{arabic}

# Introduction

Modern society's reliance on software systems continues to grow, particularly in mission-critical environments such as healthcare, aerospace, and industrial infrastructure. The reliability of these systems is crucial---failures or vulnerabilities can lead to severe financial losses and even endanger lives. A significant portion of this foundational software is still written in C, a language created by Dennis Ritchie in 1972 [@kernighan1978; @ritchie1978]. Although C has been instrumental in the evolution of software, its lack of safeguards---especially around memory management---is notorious. Memory safety bugs remain a persistent vulnerability, and producing provably and verifiably safe code in C is exceptionally challenging---take for example the stringent guidelines required by organizations like NASA for safety-critical applications [@holzmann2006].

To address these challenges, programming languages with built-in memory safety features, such as Ada and Rust, have been introduced [@adadevelopers2022; @rustprojectdevelopers2025]. Nevertheless, no language offers absolute immunity from such vulnerabilities. In addition, much of the global software infrastructure remains written in memory-unsafe languages, with C-based codebases unlikely to disappear in the near future. Ultimately, the potential for human error grows in tandem with increasing software complexity, meaning software is only as safe as its weakest link.

The advent of Large Language Models (LLMs) has profoundly influenced software development. Developers have began to regularly use LLMs for code generation, refactoring, and documentation assistance. These models at large demonstrate remarkable programming capabilities. Still, they can often introduce subtle errors that may go unnoticed by even experienced developers. Many researchers argue that the use of such technologies inherently contributes to the generation of insecure code [@perry2023; @kosmyna2025; @lee2025]. As LLM-generated code becomes more pervasive, so does the likelihood of unnoticed software errors escaping traditional human review.

Within this landscape, the need to detect vulnerabilities and ensure software quality is more urgent than ever. Fuzzing, a technique that generates and executes a vast array of test cases to identify potential bugs, has emerged as a vital approach for detecting memory safety violations. However, the necessity of manually-written harnesses---programs designed to exercise the Application Programming Interface (API) of the software under examination---poses a significant barrier to its broader adoption. As a result, the field of fuzzing automation through LLMs has gained considerable traction in recent years. Despite extensive advances in automating fuzzing, significant hurdles remain. Most current automatic-fuzzing systems require pre-existing fuzz harnesses [@oss-fuzz-gen] or depend on sample client code to exercise the target program [@utopia; @fuzzgen; @fudge]. Often, these tools still rely on developers for integration or final evaluation, leaving parts of the process manual and incomplete. Consequently, the application of LLMs to harness generation and end-to-end fuzzing remains a developing field.

This thesis aims to push the boundaries of fuzzing automation by leveraging the code synthesis and most importantly reasoning strengths of modern LLMs. We introduce OverHAuL, a system that accepts a bare and previously unfuzzed C project, utilizes LLM agents to author a new fuzzing harness from scratch and evaluates its efficacy in a closed iterative feedback loop. In this loop, said feedback is constantly utilized to improve the generated harness. This end-to-end approach is designed to minimize manual effort and accelerate vulnerability detection in C codebases.

## Thesis Structure

qqqqqqqq: Refactor when structure stabilizes

This thesis begins by outlining the foundational concepts necessary to understand its context (@sec-background) and progresses to a thorough survey of existing research in the field of automated fuzzing (@sec-related). We illustrate that the majority of contemporary fuzzing systems either depend on pre-existing harnesses or utilize client code, frequently placing the burden of validation and integration on the user. Next, we present the OverHAuL system, detailing its architecture and the innovative techniques that underpin its implementation, as well as their contributions to the advancement of automated harness generation (@sec-overhaul). Lastly, we compile a benchmark dataset consisting of ten open-source C projects and rigorously assess OverHAuL's performance ([@sec-eval;-@sec-results]).

## Summary of Contributions

This thesis presents the following key contributions:

1. The introduction of OverHAuL, a framework that enables fully automated end-to-end fuzzing harness generation using LLMs. It introduces novel techniques like an iterative feedback loop between LLM agents and the usage of a codebase oracle for code exploration.
2. Empirical validation through benchmarking experiments using ten real-world open source projects. We demonstrate that OverHAuL successfully generates effective fuzzing harnesses with a chance of **92.5%**.
3. Full open sourcing of all research artifacts, datasets, and code at <https://github.com/kchousos/OverHAuL> to encourage further research and ensure reproducibility.

This work aims to advance the use of LLMs in automated software testing, particularly for legacy codebases where building harnesses by hand is impractical or costly. By doing so, we strive to enhance software security and reliability in sectors where correctness is imperative.
