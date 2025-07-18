---
keywords: [LLMs, Fuzzing, Automation, Security, Neurosymbolic AI]
date-modified: today
---
# Preface {.unlisted .unnumbered}

This thesis was written as part of the requirements for the Bachelor of Science program in the Department of Informatics and Telecommunications at the National and Kapodistrian University of Athens during the academic year 2024--2025. The research was conducted under the supervision of Prof. Thanassis Avgerinos. The completed thesis is also available through the university's digital repository Pergamos. ~~A refined version of this work is currently being prepared for publication~~.

{{< pagebreak >}}

<!-- Inscription/dedication -->
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

A special *thank you* goes to my parents, Christina, and my friends for their constant support and understanding. Their patience and encouragement helped me persevere through this challenging period.

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
  title = {LLM-Driven Fuzzing: Automatic Harness Generation for Crypto Libraries},
  shorttitle = {LLM-Driven Fuzzing},
  author = {Chousos, Konstantinos},
  date = {2025-07},
  institution = {{National and Kapodistrian University of Athens}},
  location = {Athens, Greece},
  url = {https://kchousos.github.io/BSc-Thesis/},
  langid = {en, el}
}</code></pre>
<div class="quarto-appendix-secondary-label">For attribution, please cite this work as:</div><div id="ref-chousos2025" class="csl-entry quarto-appendix-citeas">
K. Chousos, <span>“LLM-Driven Fuzzing: Automatic Harness Generation for Crypto Libraries,”</span> Bachelor Thesis, National and Kapodistrian University of Athens, Athens, Greece, 2025. [Online]. Available: <a href="https://kchousos.github.io/thesis">https://kchousos.github.io/BSc-Thesis/</a>
</div></div></section></div>

:::
