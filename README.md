# Quantum Scientific Computing (QSC2026)

Lecture notes for a graduate / senior-undergraduate course, **Quantum Scientific
Computing**, taught in the Fall 2026–2027 term. The audience is senior
mathematics and physics undergraduates and graduate students comfortable with
linear algebra, numerical analysis, and basic quantum mechanics, but not assumed
to have prior quantum-computing coursework.

The course runs over 15 three-hour meetings, organized into **20 lecture units**
across five parts. These notes are a living document, filled in lecture by
lecture; sections still in progress are marked in the source.

## Course outline

- **Part I — Foundations (L1–L5):** quantum computation basics; channels,
  distances, and statistics; Grover search & amplitude amplification; the
  quantum Fourier transform & phase estimation; applications of phase estimation.
- **Part II — Quantum Numerical Linear Algebra (L6–L10):** input models & block
  encoding; linear combination of unitaries (LCU) & block-encoding arithmetic;
  qubitization & quantum signal processing (QSP); the quantum singular value
  transformation (QSVT) & matrix functions; quantum linear systems (QLSP).
- **Part III — Differential Equations & Simulation (L11–L14):** Hamiltonian
  simulation via product formulas; block-encoding simulation methods; linear
  ODE/PDE algorithms; open systems & nonlinear PDEs.
- **Part IV — Tensor Networks (L15–L17):** matrix product states (MPS); DMRG &
  ground states; tensor-network time evolution (TEBD/TDVP).
- **Part V — Optimization & Quantum Machine Learning (L18–L20):** variational
  algorithms & QAOA; quantum LP & SDP solvers; quantum machine learning.

## Building the notes

The entry point is `main.tex` (a `book`-class master, compiled with pdfLaTeX).
It loads `preamble.tex` and includes the 20 lecture files under `lectures/`.
Compile twice so cross-references and the table of contents settle:

```bash
pdflatex main.tex && pdflatex main.tex
```

Or, with latexmk (recommended):

```bash
latexmk -pdf main.tex
```

To draft a single lecture faster, use the `\includeonly{...}` line in `main.tex`.

## Repository layout

| Path | Contents |
|---|---|
| `main.tex`, `preamble.tex` | Master document and shared macros / theorem environments |
| `lectures/` | One `\chapter` per lecture unit (`lec01`…`lec20`) |
| `notebooks/` | Companion Jupyter notebooks (numerical demos) |
| `animations/` | Interactive HTML / GIF visualizations (e.g. Grover's search) |
| `slides/` | Supplementary slide decks |
| `teaching/` | Teacher's notes (chalk-delivery plans) |
| `syllabus/`, `solutions/`, `figs/` | Syllabus, exercise solutions, figures |

## Status

Work in progress. Part I (Lectures 1–5) is the most developed; later parts are
being filled in over the term.
