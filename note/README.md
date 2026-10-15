# Lecture notes as Jupyter notebooks

These notebooks are an automatic conversion of the LaTeX lecture notes
(`lectures/lecNN_*.tex`) into readable Jupyter form, one notebook per lecture
(`lecNN.ipynb`). They are generated from the `.tex` sources, not hand-written.

## How to read them

- The **first cell** of each notebook defines the course's math macros (`\ket`,
  `\bra`, `\QFT`, `\id`, …) for MathJax. Run/render it first (it displays nothing)
  so the mathematics in later cells renders correctly.
- Prose, definitions, theorems, lemmas, examples, remarks, and proofs are rendered
  as Markdown; equations render via MathJax.

## Known limitations of the conversion

- **Quantum circuits** (drawn with `quantikz` in the LaTeX) do not render in
  Jupyter and appear as the placeholder *"[quantum circuit — see the PDF]"*. Consult
  `main.pdf` for the circuit diagrams.
- **Cross-references** (`\cref{…}`) are reduced to plain phrases ("that theorem",
  "that section", …) since notebook cells are not numbered like the PDF.
- Lectures 1–5 are fully developed; later chapters are still scaffolds.

For runnable numerical demos, see the companion notebooks in
`../demo/lecNN_*.ipynb`.
