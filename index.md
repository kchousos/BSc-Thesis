---
keywords: [LLMs, Fuzzing, Automation, Security, Neurosymbolic AI]
---
# Preface {.unlisted .unnumbered}

This thesis was prepared in Athens, Greece, during the academic year 2024--2025, fulfilling a requirement for the Bachelor of Science degree at the [Department of Informatics and Telecommunications](https://www.di.uoa.gr/en) of the [National and Kapodistrian University of Athens](https://en.uoa.gr/). The research presented herein was carried out under the supervision of Prof. [Thanassis Avgerinos](https://cgi.di.uoa.gr/~thanassis/) and in accordance with the guidelines stipulated by the department. All processes and methodologies adopted during the research adhere to the academic and ethical standards of the university. The final version of this thesis is [hosted online](https://kchousos.github.io/BSc-Thesis/) and is also archived in the department's records, made publicly accessible through the university’s digital repository [Pergamos](https://pergamos.lib.uoa.gr/uoa/dl/object/5300250).

{{< pagebreak >}}

<!-- Inscription/dedication page for pdf output -->
::: {.content-visible when-format="latex"}
\clearpage
\thispagestyle{empty}
\vspace*{0.3\textheight}
\begin{flushright}
\itshape
 
To my beloved parents who, through their example, taught me patience, resilience and perseverance.

\end{flushright}
\newpage
:::

# Acknowledgments {.unlisted .unnumbered}

I would like to express my gratitude to my supervisor, Prof. Thanassis Avgerinos, for his insightful guidance, patience, and unwavering encouragement throughout this journey. His openness and our shared passion for the subject greatly enhanced my enjoyment of the thesis process.

I am also thankful to my fellow group members in Prof. Avgerinos' weekly meetings, whose willingness to exchange ideas and offer support was invaluable. My appreciation extends to Jorgen and Phaedon, friends who provided thoughtful input and advice along the way.

A special *thank you* goes to my parents Giannis and Gianna, Christina, and my friends for their constant support and understanding. Their patience and encouragement helped me persevere through this challenging period.

{{< pagebreak >}}

\tableofcontents
\listoffigures
\listoflistings
\listoftables

{{< pagebreak >}}

::: {.content-visible when-format="html"}

<div id="quarto-appendix" class="default">
<section class="quarto-appendix-contents" id="quarto-citation"><h2 class="anchored quarto-appendix-heading" id="citation">Citation</h2><div><div class="quarto-appendix-secondary-label">BibTeX citation:</div>
<pre class="sourceCode code-with-copy quarto-appendix-bibtex"><code class="sourceCode bibtex">@thesis{chousos2025,
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
}</code></pre>
<div class="quarto-appendix-secondary-label">For attribution, please cite this work as:</div><div id="ref-chousos2025" class="csl-entry quarto-appendix-citeas">
K. Chousos, “OverHAuL: Harnessing automation for C libraries with large language models,” BSc Thesis, National and Kapodistrian University of Athens, Athens, Greece, 2025. [Online]. Available: <a href="https://pergamos.lib.uoa.gr/uoa/dl/object/5300250">https://pergamos.lib.uoa.gr/uoa/dl/object/5300250</a></div></div></section></div>

:::
