<h1 align="center">OverHAuL: Harnessing Automation for C Libraries with Large Language Models</h1>
<p>
<a href="https://pergamos.lib.uoa.gr/uoa/dl/object/5300250"><img src="https://img.shields.io/badge/uoadl-5300250-blue" alt="uoadl:5300250" /></a>
<a href="https://kchousos.github.io/BSc-Thesis/"><img src="https://img.shields.io/badge/HTML-View_the_html_manuscript-green" alt="html" /></a>
<a href="https://kchousos.github.io/BSc-Thesis/thesis.pdf"><img src="https://img.shields.io/badge/PDF-View_the_pdf_manuscript-red" alt="pdf" /></a>
<a href="https://kchousos.github.io/overhaul-presentation/"><img alt="Slides" src="https://img.shields.io/badge/Slides-Defense_presentation-orange"/></a>
<a href="https://github.com/kchousos/OverHAuL"><img alt="Repo" src="https://img.shields.io/badge/Repo-Implementation-purple?logo=github"/></a>
</p>

### Abstract

Software vulnerabilities remain pervasive and challenging to detect, making robust testing approaches imperative. Fuzzing is an established software testing method for uncovering such vulnerabilities, through random input execution. Recent research has leveraged Large Language Models (LLMs) to enhance fuzz driver generation. However, most contemporary tools rely on additional resources beyond the target code, such as client programs or preexisting harnesses, limiting their scalability and applicability. In this thesis, we present OverHAuL, a neurosymbolic AI system that employs LLM agents to automatically generate fuzzing harnesses directly from library code, eliminating the need for auxiliary artifacts. To comprehensively evaluate OverHAuL, we construct a benchmark suite consisting of ten open-source C libraries. Our empirical analysis demonstrates that OverHAuL achieves an 81.25% success rate in harness generation across the evaluated projects, underscoring its effectiveness and potential to facilitate more efficient vulnerability discovery.

### Preface

This thesis was prepared in Athens, Greece, during the academic year 2024–2025, fulfilling a requirement for the Bachelor of Science degree at the [Department of Informatics and Telecommunications](https://www.di.uoa.gr/en) of the [National and Kapodistrian University of Athens](https://en.uoa.gr/). The research presented herein was carried out under the supervision of Prof. [Thanassis Avgerinos](https://cgi.di.uoa.gr/~thanassis/) and in accordance with the guidelines stipulated by the department. All processes and methodologies adopted during the research adhere to the academic and ethical standards of the university. The final version of this thesis is [hosted online](https://kchousos.github.io/BSc-Thesis/) and is also archived in the department's records, made publicly accessible through the university’s digital repository [Pergamos](https://pergamos.lib.uoa.gr/uoa/dl/object/5300250).

### Citation

 BibLaTeX citation:

```bibtex
@thesis{chousos2025,
  type = {BSc Thesis},
  title = {{{OverHAuL}}: {{Harnessing}} Automation for {{C}} Libraries with Large Language Models},
  shorttitle = {{{OverHAuL}}},
  author = {Chousos, Konstantinos},
  date = {2025-07-27},
  institution = {{National and Kapodistrian University of Athens}},
  location = {Athens, Greece},
  url = {https://pergamos.lib.uoa.gr/uoa/dl/object/5300250},
  langid = {english},
  pagetotal = {79},
  note = {Also available at: \href{https://kchousos.github.io/BSc-Thesis/}{https://kchousos.github.io/BSc-Thesis/}}
}
```

 For attribution, please cite this work as:
 
 ```
K. Chousos, “OverHAuL: Harnessing automation for C libraries with large language models,” BSc Thesis, National and Kapodistrian University of Athens, Athens, Greece, 2025. [Online]. Available: https://pergamos.lib.uoa.gr/uoa/dl/object/5300250
 ```
