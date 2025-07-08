# Related work

Automated testing, and especially automated fuzzing and automated harness creation have a long research history. Still, a lot of ground remains to be covered until true automation of these tasks is achieved. Until the introduction of transformers [@vaswani2023] and the 2020's boom of commercial GPTs [@chatgpt], automation regarding testing and fuzzing was mainly attempted through static and dynamic program analysis methods. 


- An established tool from that era is KLEE [@klee], introduced in 2008. KLEE as a system leverages symbolic execution to explore and cover the code of a program, with the goal of generating a test for it automatically. 
- FUDGE [@fudge], a closed-source tool for automatic harness generation of C/C++ projects based on existing client code. FUDGE uses program slicing [@sasirekha2011Slicing] to extract useful code snippets and through ~~synthesis~~ it turns them into harnesses. Each generated harness is compiled and later evaluated, with the final results being presented to the user through a custom web-based UI.


## Automatic Harnesses

Where we are right now. SOTA projects. Similar projects using LLMs in the fuzzing space [@fuzzgpt;@titanfuzz;@iris].

[TODO]{.mark}

## Google

FuzzGen, FUDGE, OSS-Fuzz-Gen [@fuzzgen;@fudge;@oss-fuzz;@oss-fuzz-gen].

### OSS-Fuzz-Gen

Features/caveats. `from_scratch` branch^[commit `171aac2`].
