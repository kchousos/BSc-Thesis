# Background {#sec-background}

This chapter provides the foundational and necessary background for this thesis, by exploring the core concepts and technological advances central to modern fuzzing and Large Language Models (LLMs). It begins with an in-depth definition and overview of fuzz testing---an automated technique for uncovering software bugs and vulnerabilities through randomized input generation---highlighting its methodology, tools, and impact. What follows is a discussion on LLMs and their transformative influence on natural language processing, programming, and code generation. Challenges and opportunities in applying LLMs to tasks such as fuzzing harness generation are examined, leading to a discussion of Neurosymbolic AI, an emerging approach that combines neural and symbolic reasoning to address the limitations of current AI systems. This multifaceted background establishes the context necessary for understanding the research and innovations presented in subsequent chapters.

## Fuzz Testing

*Fuzzing* is an automated software-testing technique in which a *Program Under Test* (PUT) is executed with (pseudo-)random inputs in the hope of exposing undefined behavior. When such behavior manifests as a crash, hang, or memory-safety violation, the corresponding input constitutes a *test-case* that reveals a bug and often a vulnerability [@manes2019]. In a certain sense, fuzzing is a form of adversarial, penetration-style testing carried out by the defender before the adversary has an opportunity to do so. Interest in the technique surged after the publication of three practitioner-oriented books in 2007--2008 [@takanen2018; @sutton2007; @rathaus2007].

Historically, the term was coined by Miller et al. in 1990, who used "fuzz" to describe a program that "generates a stream of random characters to be consumed by a target program" [@miller1990]. This informal usage captured the essence of what fuzzing aims to do: stress test software by bombarding it with unexpected inputs to reveal bugs. To formalize this concept, we adopt Manes et al.'s rigorous definitions [@manes2019]:

::: {#def-fuzzing}
###### Fuzzing
Fuzzing is the execution of a Program Under Test (PUT) using input(s) sampled from an input space (the *fuzz input space*) that protrudes the expected input space of the PUT [@manes2019]. 
:::

This means fuzzing involves running the target program on inputs that go beyond those it is typically designed to handle, aiming to uncover hidden issues. An individual instance of such execution---or a bounded sequence thereof---is called a *fuzzing run*. When these runs are conducted systematically and at scale with the specific goal of detecting violations of a security policy, the activity is known as *fuzz testing* (or simply *fuzzing*):

::: {#def-fuzz-testing}
###### Fuzz Testing
Fuzz testing is the use of fuzzing to test whether a PUT violates a security policy [@manes2019].
:::

This distinction highlights that fuzz testing is fuzzing with an explicit focus on security properties and policy enforcement. Central to managing this process is the *fuzzer engine*, which orchestrates the execution of one or more fuzzing runs as part of a *fuzz campaign*. A fuzz campaign represents a concrete instance of fuzz testing tailored to a particular program and security policy:

::: {#def-fuzzer}
###### Fuzzer, Fuzzer Engine
A fuzzer is a program that performs fuzz testing on a PUT [@manes2019].
:::

::: {#def-campaign}
###### Fuzz Campaign
A fuzz campaign is a specific execution of a fuzzer on a PUT with a specific security policy [@manes2019].
:::

Throughout each execution within a campaign, a *bug oracle* plays a critical role in evaluating the program's behavior to determine whether it violates the defined security policy:

::: {#def-oracle}
###### Bug Oracle
A bug oracle is a component (often inside the fuzzer) that determines whether a given execution of the PUT violates a specific security policy [@manes2019].
:::

In practice, bug oracles often rely on runtime instrumentation techniques, such as monitoring for fatal POSIX signals (e.g., `SIGSEGV`) or using sanitizers like AddressSanitizer (ASan) [@serebryany2012]. Tools like LibFuzzer [@libfuzzer] commonly incorporate such instrumentation to reliably identify crashes or memory errors during fuzzing.

Most fuzz campaigns begin with a set of *seeds*---inputs that are well-formed and belong to the PUT's expected input space---called a *seed corpus*. These seeds serve as starting points from which the fuzzer generates new test cases by applying transformations or mutations, thereby exploring a broader input space:

::: {#def-seed}
###### Seed
An input given to the PUT that is mutated by the fuzzer to produce new test cases. During a fuzz campaign ([@def-campaign]) all seeds are stored in a seed *pool* or *corpus* [@manes2019].
:::

The process of selecting an effective initial corpus is crucial because it directly impacts how quickly and thoroughly the fuzzer can cover the target program's code. This challenge---studied as the *seed-selection problem*---involves identifying seeds that enable rapid discovery of diverse execution paths and is non-trivial [@rebert2014]. A well-chosen seed set often accelerates bug discovery and improves overall fuzzing efficiency.

### Motivation

> The purpose of fuzzing relies on the assumption that there are bugs within every program, which are waiting to be discovered. Therefore, a systematic approach should find them sooner or later.
>
> --- OWASP Foundation [@owaspfoundation]

Fuzz testing provides several key advantages that contribute substantially to software quality and security. First, by uncovering vulnerabilities early in the development cycle, fuzzing reduces both the cost and risk associated with addressing security flaws after deployment. This proactive approach not only minimizes potential exposure but also streamlines the remediation process. Additionally, by subjecting software to the same randomized, adversarial inputs that malicious actors might use, fuzz testing puts defenders on equal footing with attackers, enhancing preparedness against emerging zero-day threats.

Beyond security, fuzzing plays a crucial role in improving the robustness and correctness of software systems. It is particularly effective at identifying logical errors and stability issues in complex, high-throughput APIs---such as decompressors and parsers---especially when these systems are expected to handle only well-formed inputs. Moreover, the integration of fuzz testing into continuous integration pipelines provides an effective guard against regressions. By systematically re-executing a corpus of previously discovered crashing inputs, developers can ensure that resolved bugs do not resurface in subsequent releases, thereby maintaining a consistent level of software reliability over time.

#### Success Stories

*Heartbleed* (CVE-2014-0160) [@heartbleed; @heartbleed-cve] arose from a buffer over-read^[<https://xkcd.com/1354/> provides a concise illustration.] in the TLS implementation of the OpenSSL library [@theopensslproject2025], introduced on 1st of February 2012 and unnoticed until 1st of April 2014. Later analysis showed that a simple fuzz campaign exercising the TLS heartbeat extension would have revealed the defect almost immediately [@wheeler2014].

Likewise, the *Shellshock* (or *Bashdoor*) family of bugs in GNU Bash [@bash] enabled arbitrary command execution on many UNIX systems. While the initial flaw was fixed promptly, subsequent bug variants were discovered by Google's Michał Zalewski using his own fuzzer---the now ubiquitous AFL fuzzer  [@afl]---in late 2014 [@saarinen2014].

On the defensive tooling side, the security tool named *Mayhem* [@avgerinos2018; @cha2012]---developed by the company of the same name, formerly known as ForAllSecure---has since been adopted by the US Air Force, the Pentagon, Cloudflare, and numerous open-source communities. It has found and facilitated the remediation of thousands of previously unknown vulnerabilities, from errors in Cloudflare's infrastructure to bugs in open-source projects like OpenWRT [@simonite2020mayhem].

These cases underscore the central thesis of fuzz testing: exhaustive manual review is infeasible, but scalable stochastic exploration reliably surfaces the critical few defects that matter most.

### Methodology

As previously discussed, fuzz testing of a PUT is typically conducted using a dedicated fuzzing engine ([@def-fuzzer]). Among the most widely adopted fuzzers for C and C++ projects and libraries are AFL [@afl]---which has since evolved into AFL++ [@aflpp]---and LibFuzzer [@libfuzzer]. Within the OverHAuL framework, LibFuzzer is preferred due to its superior suitability for library fuzzing, whereas AFL++ predominantly targets executables and binary fuzzing.

#### LibFuzzer

LibFuzzer [@libfuzzer] is an in-process, coverage-guided evolutionary fuzzing engine primarily designed for testing libraries. It forms part of the LLVM ecosystem [@llvm] and operates by linking directly with the library under evaluation. The fuzzer delivers mutated input data to the library through a designated fuzzing entry point, commonly referred to as the *fuzz target* or *harness*.

:::{#def-target}
###### Fuzz target
A function that accepts a byte array as input and exercises the application programming interface (API) under test using these inputs [@libfuzzer]. This construct is also known as a *fuzz driver*, *fuzzer entry point*, or *fuzzing harness*.
:::

For the remainder of this thesis, the terms presented in @def-target will be used interchangeably.

To effectively validate an implementation or library, developers are required to author a fuzzing harness that invokes the target library's API functions utilizing the fuzz-generated inputs. This harness serves as the principal interface for the fuzzer and is executed iteratively, each time with mutated input designed to maximize code coverage and uncover defects. To comply with LibFuzzer's interface requirements, a harness must conform to the function signature shown in @lst-basic-example. A more illustrative example of such a harness is provided in @lst-fuzzing-example.

::: {#lst-basic-example fig-scap='Fuzzing harness format'}

```c
int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  DoSomethingInterestingWithData(Data, Size);
  return 0;
}
```

This function receives the fuzzing input via a pointer to an array of bytes (`Data`) and its associated size (`Size`). Efficiency in fuzzing is achieved by invoking the API of interest within the body of this function, thereby allowing the fuzzer to explore a broad spectrum of behavior through systematic input mutation.
:::

::: {#lst-fuzzing-example fig-scap='Example fuzzing harness'}

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

To compile and link such a harness with LibFuzzer, the Clang compiler---also part of the LLVM project [@llvm]---must be used alongside appropriate compiler flags. For instance, compiling the harness in @lst-fuzzing-example can be achieved as shown in @lst-harness-compilation.

::: {#lst-harness-compilation fig-scap='Compilation of harness'}

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

Despite its potential for uncovering software vulnerabilities, fuzzing remains a relatively underutilized testing technique compared to more established methodologies such as Test-Driven Development (TDD). This limited adoption can be attributed, in part, to the substantial initial investment required to design and implement appropriate test harnesses that enable effective fuzzing processes. Furthermore, the interpretation of fuzzing outcomes---particularly the identification, diagnostic analysis, and prioritization of program crashes---demands considerable resources and specialized expertise. These factors collectively pose significant barriers to the widespread integration of fuzzing within standard software development and testing practices. OverHAuL addresses this challenge by facilitating the seamless integration of fuzzing into developers' workflows, minimizing initial barriers and reducing upfront costs to an almost negligible level.

## Large Language Models

Natural Language Processing (NLP), a subfield of AI, has a rich and ongoing history that has evolved significantly since its beginning in the 1990s [@li2022; @wang2025]. Among the most notable---and recent---advancements in this domain are LLMs, which have transformed the landscape of NLP and AI in general.

At the core of many LLMs is the attention mechanism, which was introduced by Bahdanau et al. in 2014 [@bahdanau2016]. This pivotal innovation enabled models to focus on relevant parts of the input sequence when making predictions, significantly improving language understanding and generation tasks. Building on this foundation, the Transformer architecture was proposed by Vaswani et al. in 2017 [@vaswani2023]. This architecture has become the backbone of most contemporary LLMs, as it efficiently processes sequences of data, capturing long-range dependencies without being hindered by sequential processing limitations.

One of the first major breakthroughs utilizing the Transformer architecture was BERT (Bidirectional Encoder Representations from Transformers), developed by Devlin et al. in 2019 [@devlin2019]. BERT's bi-directional understanding allowed it to capture the context of words from both directions, which improved the accuracy of various NLP tasks. Following this, the Generative Pre-trained Transformer (GPT) series, initiated by OpenAI with the original GPT model in 2018 [@radford2018], further pushed the boundaries. Subsequent iterations, including GPT-2 [@radford2019], GPT-3 [@brown2020], and the most current GPT-4 [@openai2024], have continued to enhance performance by scaling model size, data, and training techniques.

In addition to OpenAI's contributions, other significant models have emerged, such as Claude, DeepSeek-R1 and the Llama series (1 through 3) [@claude; @deepseek-ai2025; @grattafiori2024]. The proliferation of LLMs has sparked an active discourse about their capabilities, applications, and implications in various fields.

### State-of-the-art GPTs

User-facing LLMs are generally categorized between closed-source and open-source models. Closed-source LLMs like ChatGPT, Claude, and Gemini [@chatgpt; @claude; @gemini] represent commercially developed systems often optimized for specific tasks without public access to their underlying weights. In contrast, open-source models^[The term "open-source" models is somewhat misleading, since these are better termed as *open-weights* models. While their weights are publicly available, their training data and underlying code are often proprietary. This terminology reflects community usage but fails to capture the limitations of transparency and accessibility inherent in these models.], including the Llama series [@grattafiori2024] and Deepseek [@deepseek-ai2025], provide researchers and practitioners with access to model weights, allowing for greater transparency and adaptability.

### Prompting {#sec-prompting}

Interaction with LLMs typically occurs through chat-like interfaces where the user gives queries and tasks for the LLM to answer and complete, a process commonly referred to as *prompting*. A critical aspect of effective engagement with LLMs is the usage of different prompting strategies, which can significantly influence the quality and relevance of the generated outputs. Various approaches to prompting have been developed and studied, including zero-shot and few-shot prompting. In zero-shot prompting, the model is expected to perform the given task without any provided examples, while in few-shot prompting, the user offers a limited number of examples to guide the model's responses [@brown2020].

To enhance performance on more complex tasks, several advanced prompting techniques have emerged. One notable strategy is the *Chain of Thought* approach (COT) [@chainofthought], which entails presenting the model with sample thought processes for solving a given task. This method encourages the model to generate more coherent and logical reasoning by mimicking human-like cognitive pathways. A more refined but complex variant of this approach is the *Tree of Thoughts* technique [@yao2023], which enables the LLM to explore multiple lines of reasoning concurrently, thereby facilitating the selection of the most promising train of thought for further exploration.

In addition to these cognitive strategies, Retrieval-Augmented Generation (RAG) [@lewis2021] is another innovative technique that enhances the model's capacity to provide accurate information by incorporating external knowledge not present in its training dataset. RAG operates by integrating the LLM with an external storage system---often a vector store containing relevant documents---that the model can query in real-time. This allows the LLM to pull up pertinent and/or proprietary information in response to user queries, resulting in more comprehensive and accurate answers.

Moreover, the ReAct framework [@reAct], which stands for Reasoning and Acting, empowers LLMs by granting access to external tools. This capability allows LLM instances to function as intelligent agents that can interact meaningfully with their environment through user-defined functions. For instance, a ReAct tool could be a function that returns a weather forecast based on the user's current location. In this scenario, the LLM can provide accurate and truthful predictions, thereby mitigating risks associated with hallucinated responses.

### LLMs for Coding {#sec-llm-coding}

The impact of LLMs in software development in recent years is apparent, with hundreds of LLM-assistance extensions and Integrated Development Environments (IDEs) being published. Notable instances include tools like GitHub Copilot and IDEs such as Cursor [@cursor; @ghcopilot], which leverage LLM capabilities to provide developers with coding suggestions, auto-completions, and even real-time debugging assistance. Such innovations have introduced a layer of interaction that enhances productivity and fosters a more intuitive coding experience. Additionally, more and more LLMs are now specifically trained for usage in code-generation tasks [@nijkamp2023a; @nijkamp2023; @openai2025a].

One exemplary product of this innovation is *vibecoding* and the no-code movement, which describe the development of software by only prompting and tasking an LLM, i.e. without any actual programming required by the user. This constitutes a showcase of how LLMs can be used to elevate the coding experience by supporting developers as they navigate complex programming tasks [@sarkar2025]. By analyzing the context of the code being written, these sophisticated models can provide contextualized insights and relevant snippets, effectively streamlining the development process. Developers can benefit from reduced cognitive load, as they receive suggestions that not only cater to immediate coding needs but also promote adherence to best practices and coding standards.

Despite these advancements, it is crucial to recognize the inherent limitations of LLMs when applied to software development. While they can help in many aspects of coding, they are not immune to generating erroneous outputs---a phenomenon often referred to as "hallucination" [@huang2025]. Hallucinations occur when LLMs produce information that is unfounded or inaccurate, which can stem from several factors, including the limitations of their training data and the constrained context window within which they operate. As LLMs generate code suggestions based on the patterns learned from vast datasets, they may inadvertently propose solutions that do not align with the specific requirements of a task or that utilize outdated programming paradigms.

Moreover, the challenge of limited context windows can lead to suboptimal suggestions [@kaddour2023]. LLMs generally process a fixed amount of text when generating responses, which can impact their ability to fully grasp the nuances of complex coding scenarios. This may result in outputs that lack the necessary depth and specificity required for successful implementation. As a consequence, developers must exercise caution and critically evaluate the suggestions offered by these models, as reliance on them without due diligence could lead to the introduction of bugs or other issues in the code.

### LLMs for Fuzzing

In the domain of fuzzing, recent research has explored the application of LLMs primarily along two axes: employing LLMs to generate seeds and inputs for the program under test [@titanfuzz; @black2024; @shi2024; @fuzzgpt] and leveraging them to generate the fuzz driver itself (@sec-related). This thesis focuses on the latter, recognizing that while using LLMs for seed generation offers certain advantages, the challenge of automating harness generation represents a deeper and more meaningful frontier. Significant limitations such as restricted context windows and the propensity for LLMs to hallucinate remain central concerns in this area [@huang2025; @kaddour2023].

The process of constructing a fuzzing harness is inherently complex, demanding a profound understanding of the target library and the nuanced interactions among its components. Achieving this level of comprehension is often beyond the reach of LLMs when deployed in isolation. Empirical evidence by Jiang et al. [@jiang2024] demonstrates that zero-shot harness generation with LLMs is both ineffective and prone to significant errors. Specifically, LLMs tend to rely heavily on patterns encountered during training, which leads to the erroneous invocation of APIs, particularly when their context window is pushed to its limits. This over-reliance on training data exacerbates the risk of hallucination, compounding the challenge of generating correct and robust fuzz drivers.

Compounding this issue is the inherent risk introduced by error-prone code synthesized by LLMs. In the context of fuzzing, a fundamental requirement is the clear attribution of observed failures: developers must be confident that detected crashes stem from vulnerabilities in the tested software rather than flaws or bugs inadvertently introduced by the harness. This necessity imposes an additional verification burden, increasing developers' cognitive load and diverting attention from the primary goal of meaningful software evaluation and improvement.

Enhancing the reliability of LLM-generated harnesses thus necessitates systematic and programmatic evaluation and 
validation of generated artifacts [@tilwani2024]. Such validation involves implementing structured techniques to rigorously assess both the accuracy and robustness of the code, confirming that it interacts correctly with the relevant software components and behaves as intended. This approach aligns with the emerging framework of Neurosymbolic AI (@sec-nesy), which integrates the statistical learning capabilities of neural networks with the rigor and precision of symbolic reasoning. By leveraging the strengths of both paradigms, neuroscience-inspired symbolic methods [@kahneman2011] may offer pathways toward more reliable and effective LLM-generated fuzzing harnesses, facilitating a smoother integration of automated testing practices into established software development pipelines [@mastropaolo2025; @velasco2025].

## Neurosymbolic AI {#sec-nesy}

Neurosymbolic AI represents a groundbreaking fusion of neural network methodologies with symbolic execution techniques and tools, providing a multi-faceted approach to overcoming the inherent limitations of traditional AI paradigms [@sheth2023; @garcez2020]. This innovative synthesis seeks to combine the strengths of both neural networks, which excel in pattern recognition and data-driven learning, and symbolic systems, which offer structured reasoning and interpretability. By integrating these two approaches, neurosymbolic AI aims to create cognitive models that are not only more accurate but also more robust in problem-solving contexts.

At its core, Neurosymbolic AI facilitates the development of AI systems that are capable of understanding and interpreting feedback in real-world scenarios [@ganguly2024]. This characteristic is particularly significant in the current landscape of artificial intelligence, where LLMs are predominant. In this context, Neurosymbolic AI is increasingly viewed as a critical solution to pressing issues related to explainability, attribution, and reliability in AI systems [@gaur2023; @tilwani2024]. These challenges are essential for ensuring that AI systems can be trusted and effectively utilized in various applications, from business to healthcare.

The burgeoning field of neurosymbolic AI is still in its nascent stages, with ongoing research and development actively exploring its potential to enhance attribution methodologies within large language models. By addressing these critical challenges, Neurosymbolic AI can significantly contribute to the broader landscape of trustworthy AI systems, allowing for more transparent and accountable decision-making processes [@sheth2023; @gaur2023; @tilwani2024].

Moreover, the application of neurosymbolic AI within the domain of fuzzing is gaining traction, paving the way for innovative explorations. This integration of LLMs with symbolic systems opens up new avenues for research. Currently, there are only a limited number of tools that support such hybrid approaches (@sec-related). Among these, OverHAuL constitutes a Neuro[Symbolic] tool, as classified by Henry Kautz's taxonomy [@sarker2022; @kautz2020]. This means that the neural model---specifically the LLM---can leverage symbolic reasoning tools---in this case a source code explorer (@sec-implementation)---to augment its reasoning capabilities. This symbiotic relationship enhances the overall efficacy and versatility of LLMs for fuzzing harnesses generation, demonstrating the profound potential held by the fusion of neural and symbolic methodologies.
