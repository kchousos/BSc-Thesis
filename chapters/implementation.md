# Implementation {#sec-implementation}

In creating the codebase oracle, we employ the "libclang" Python package [@he2025] to slice functions based on the AST capability provided by Clang. As detailed in @sec-oracle, the intermediate output consists of a list of Python dictionaries, with each dictionary storing a function’s body, signature, and corresponding file path. Each chunk of function code is then converted into an embedding using OpenAI's "text-embedding-3-small" model [@openaidocs2025a] and stored in a FAISS vector store index [@faiss]. This index is mapped to a metadata structure that contains the aforementioned function data—specifically the actual function body, signature, and file path. When a search is conducted on the index, the results returned are the embeddings. The responses that the LLM agent receives are derived from the corresponding metadata entries of each embedding.

All LLM agents and components are developed using the DSPy library, a declarative Python framework for LLM programming created by Stanford’s NLP research team [@dspy]. DSPy offers built-in modules and abstractions that facilitate the composition of LLMs and prompting techniques, such as Chain of Thought and ReAct (@lst-dspy). Each agent within OverHAuL is an instance of DSPy's ReAct module [@stanfordnlpteam2025], accompanied by a custom Signature [@stanfordnlpteam2025a]---displayed in @sec-signatures. DSPy was selected over other contemporary LLM libraries, such as LangChain and Llamaindex [@langchain; @llamaindex], because of its user-friendliness, logical abstractions, and efficient development process---qualities that are often lacking in these alternative libraries [@both2024; @woolf2023; @woyera2023].

::: {#lst-dspy fig-scap='DSPy example'}
```python
import dspy
lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_OPENAI_API_KEY')
dspy.configure(lm=lm)

math = dspy.ChainOfThought("question -> answer: float")
math(question="Two dice are tossed. What is the probability that the sum equals two?")
```

Sample DSPy program.
:::

Repository cloning is executed using the `--depth 1` flag to minimize disk storage usage and reduce the size of artifacts.

The current implementation of OverHAuL sits at 1,254 source lines of Python code.

## Development Tools

The development of OverHAuL incorporates a variety of tools aimed at enhancing functionality and efficiency. Notably, "uv" is a Python package and project manager written in Rust that serves as a replacement for Poetry. Additionally, "Ruff," a code linter and formatter also developed in Rust, contributes to code quality by enforcing consistent formatting standards. The project also employs "MyPy," the widely-used static type checker for Python, to ensure type correctness. Testing is facilitated through "PyTest," a robust  Python testing framework. Lastly, "pdoc" is utilized as a Static Site Generator (SSG) to automate the creation of API documentation^[Available at <https://kchousos.github.io/OverHAuL/>.] [@astral2025; @astral2025a; @cortesi2025; @pytestdevteam2025; @pythonsoftwarefoundation2025].

## Reproducibility


OverHAuL's source code is available at <https://github.com/kchousos/OverHAuL>. Each benchmark run was conducted within the framework of a GitHub Actions workflow, resulting in a detailed summary accompanied by an artifact containing all cloned repositories. These artifacts are the compressed result directories described in @sec-local and provide the essential components necessary for the reproducibility each project's results, as described in @sec-install. All benchmark runs can be conveniently accessed at <https://github.com/kchousos/OverHAuL/actions/workflows/benchmarks.yml>.
