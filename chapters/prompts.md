# DSPy Custom Signatures {#sec-signatures}

```python
class GenerateHarness(dspy.Signature):
    """
    You are an experienced C/C++ security testing engineer. You must write a
    libFuzzer-compatible `int LLVMFuzzerTestOneInput(const uint8_t *data, size_t
    size)` harness for a function of the given C project. Your goal is for the
    harness to be ready for compilation and for it to find successfully a bug in
    the function-under-test. Write verbose (within reason) and helpful comments
    on each step/decision you take/make, especially if you use "weird" constants
    or values that have something to do with the project.

    You have access to a rag_tool, which contains a vector store of
    function-level chunks of the project. Use it to write better harnesses. Keep
    in mind that it can only reply with function chunks, do not ask it to
    combine stuff.

    The rag_tool does not store any information on which lines the functions
    are. So do not ask questions based on lines.

    Make sure that you only fuzz an existing function. You will know that a
    functions exists when the rag_tool returns to you its signature and body.
    """

    static: str = dspy.InputField(
        desc=""" Output of static analysis tools for the project. If you find it
        helpful, write your harness so that it leverages some of the potential
        vulnerabilities described below.  """
    )
    new_harness: str = dspy.OutputField(
        desc=""" C code for a libFuzzer-compatible harness. Output only the C
        code, **DO NOT format it in a markdown code cell with backticks**, so
        that it will be ready for compilation.

        <important>
        
        Add **all** the necessary includes, either project-specific or standard
        libraries like <string.h>, <stdint.h> and <stdlib.h>. Also include any
        header files that are part of the project and are probably useful. Most
        projects have a header file with the same name as the project at the
        root.

        **The function to be fuzzed absolutely must be part of the source
        code**, do not write a harness for your own functions or speculate about
        existing ones. You must be sure that the function that is fuzzed exists
        in the source code. Use your rag tool to query the source code.

        Do not try to fuzz functions of the project that are static, since they
        are only visible in the file that they were declared. Choose other
        user-facing functions instead.

        </important>

        **Do not truncate the input to a smaller size that the original**,
        e.g. for avoiding large stack usage or to avoid excessive buffers. Opt
        to using the heap when possible to increase the chance of exposing
        memory errors of the library, e.g. mmap instead of declaring
        buf[1024]. Any edge cases should be handled by the library itself, not
        the harness. On the other hand, do not write code that will most
        probably crash irregardless of the library under test. The point is for
        a function of the library under test to crash, not the harness
        itself. Use and take advantage of any custom structs that the library
        declares.

        Do not copy function declarations inside the harness. The harness will
        be compiled in the root directory of the project.  """
    )


class FixHarness(dspy.Signature):
    """
    You are an experienced C/C++ security testing engineer. Given a
    libFuzzer-compatible harness that fails to compile and its compilation
    errors, rewrite it so that it compiles successfully. Analyze the compilation
    errors carefully and find the root causes. Add any missing #includes like
    <string.h>, <stdint.h> and <stdlib.h> and #define required macros or
    constants in the fuzz target. If needed, re-declare functions or struct
    types. Add verbose comments to explain what you changed and why.
    """

    old_harness: str = dspy.InputField(desc="The harness to be fixed.")
    error: str = dspy.InputField(desc="The compilaton error of the harness.")
    new_harness: str = dspy.OutputField(
        desc="""The newly created harness with the necessary modifications for
        correct compilation."""
    )


class ImproveHarness(dspy.Signature):
    f"""
    You are an experienced C/C++ security testing engineer. Given a
    libFuzzer-compatible harness that does not find any bug/does not crash (even
    after running for {Config.EXECUTION_TIMEOUT} seconds) or has memory leaks
    (generates leak files), you are called to rewrite it and improve it so that
    a bug can be found more easily and/or memory is managed correctly. Determine
    the information you need to write an effective fuzz target and understand
    constraints and edge cases in the source code to do it more
    effectively. Reply only with the source code --- without backticks.  Add
    verbose comments to explain what you changed and why.
    """

    old_harness: str = dspy.InputField(
        desc="The harness to be improved so it can find a bug more quickly."
    )
    output: str = dspy.InputField(desc="The output of the harness' execution.")
    new_harness: str = dspy.OutputField(
        desc="""The newly created harness with the necessary modifications for
        quicker bug-finding. If the provided harness has unnecessary input
        limitations regarding size or format etc., remove them."""
    )
```
