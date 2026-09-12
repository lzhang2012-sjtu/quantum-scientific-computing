# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository holds the **LaTeX lecture notes for a graduate/senior-undergraduate course, "Quantum Scientific Computing," taught in the Fall 2026–2027 term.**

The course runs over **15 three-hour class meetings** and is organized into **20 lecture units** (some meetings cover more than one unit). The audience is senior math and physics undergraduates and graduate students, comfortable with linear algebra, numerical analysis, and basic quantum mechanics, but not assumed to have prior quantum-computing coursework.

The notes are a **work in progress**: the current state is a compiling *scaffold* — every lecture file has learning objectives, a section skeleton, exercise stubs, and a reading map — with detailed content (prose, proofs, worked examples) filled in lecture by lecture over time. Unfinished content is marked with the red `\todo{...}` macro.

### Course structure (20 lecture units)

- **Part I — Foundations (L1–L5):** quantum computation basics; channels/distances/statistics; Grover & amplitude amplification; QFT & phase estimation; QPE applications.
- **Part II — Quantum Numerical Linear Algebra (L6–L10):** input models & block encoding; LCU & block-encoding arithmetic; qubitization & QSP; QSVT & matrix functions; quantum linear systems (QLSP).
- **Part III — Differential Equations & Simulation (L11–L14):** Hamiltonian simulation via product formulas; block-encoding simulation methods; linear ODE/PDE algorithms (LSE, time-marching, LCHS, Schrödingerization); open systems & nonlinear PDEs.
- **Part IV — Tensor Networks (L15–L17):** tensor-network states (MPS); DMRG & ground states; tensor-network time evolution (TEBD/TDVP).
- **Part V — Optimization & Quantum Machine Learning (L18–L20):** variational algorithms & QAOA; quantum LP & SDP solvers; quantum machine learning.

## Source material

The notes draw on reference material stored in the repo. Use these when drafting lecture content:

| File | What it is | Primary use |
|---|---|---|
| `qasc_notes.pdf` | Lin Lin, *Lecture Notes on Quantum Algorithms for Scientific Computation* (132 pp, 8 ch) | Foundations + QNLA backbone |
| `live_notes_0429.pdf` | Expanded "live" version (447 pp, 21 ch, 4 parts) | Deeper QNLA, differential equations, open systems, statistics |
| `talk_QNLA_tutorial_0411.tex` | Dong An, *Quantum Numerical Linear Algebra* beamer talk | QNLA framing (block encoding, LCU, QSVT, QLSP) |
| `material/` | Childs' *Lecture Notes on Quantum Algorithms* and slide decks | Supplementary references |

**Topics not covered by the references** (tensor networks, QAOA/VQE, quantum LP/SDP, quantum machine learning) must be drafted from scratch using the external references listed in each lecture's "Further reading" section — verify citations before adding them.

## Build

The entry point is **`main.tex`** (a `book`-class master, compile with **pdfLaTeX**). It loads `preamble.tex` and `\include`s the 20 lecture files under `lectures/`. There is currently no `.bib` file — per-lecture references live in each lecture's "Further reading" list (a shared `.bib` may be introduced later). Compile twice so cross-references and the table of contents settle.

```bash
pdflatex main.tex && pdflatex main.tex
```

Or with latexmk (recommended):
```bash
latexmk -pdf main.tex
```

To draft/compile a single lecture faster, uncomment and edit the `\includeonly{...}` line in `main.tex`.

Clean auxiliary files:
```bash
latexmk -c
```

## File structure

- `main.tex` — master document and Overleaf entry point (`book` class, pdfLaTeX)
- `preamble.tex` — packages, quantum-computing macros, and theorem environments (loaded by `main.tex`)
- `lectures/lecNN_slug.tex` — one `\chapter` per lecture unit (`lec01`…`lec20`)
- `figs/` — figures (currently empty)
- `qasc_notes.pdf`, `live_notes_0429.pdf`, `talk_QNLA_tutorial_0411.tex` — reference material
- `talk_QNLA/` — sources and extracted images for the Dong An QNLA talk
- `material/` — supplementary references (Childs' notes, slide decks)
- `docs/superpowers/specs/` — the course design spec
- `OVERLEAF.md` — Overleaf git integration instructions and credentials
- `SKILLS.md` — record of editing and workflow conventions used in this project

## Overleaf Git Integration

This project is synced with Overleaf via git — see `OVERLEAF.md` for the project ID (`6a90352dd7ac4f1473c9cab5`), token, clone command, and push/pull workflow. Push sources (`main.tex`, `preamble.tex`, `lectures/*.tex`, figures under `figs/`); do **not** push build artifacts (`main.pdf`, `*.aux`, `*.log`, etc.).

## Editing conventions

- Use American English spelling throughout (Schrödingerization, discretization, neighborhood, etc.).
- This is a mathematics / quantum-computing course; keep the tone professional but pedagogical — these are teaching notes, so favor clear motivation and worked examples over terse formalism.
- Each lecture file follows the same skeleton: `\begin{objectives}` box → body `\section`s → `\exercisesection` → `\readingsection`. Preserve this structure when filling in content.
- Use the shared macros from `preamble.tex` (`\ket`, `\bra`, `\braket`, `\tr`, `\norm`, `\bigo`, `\R`, `\C`, `\E`, …) rather than redefining notation per lecture. Add new shared macros to `preamble.tex`, not to individual lectures.
- Keep terminology consistent with the references: "block encoding", "qubitization", "quantum signal processing (QSP)", "quantum singular value transformation (QSVT)", "linear combination of unitaries (LCU)", "quantum linear system problem (QLSP)".
- Mark unfinished content with `\todo{...}`; remove all `\todo` markers before treating a lecture as complete.
- Cross-reference chapters/sections with `\cref{ch:lecNN}` / `\cref{sec:lecNN-k}` (labels already scaffolded).
- When adding references to a lecture's "Further reading", verify authors, venue, volume, and year before committing.
- The scaffold must always compile — never leave a broken `\input`, `\ref`, or environment. Prefer visible `\todo` placeholders over commented-out or dangling content.

## Preamble macros and notation

`preamble.tex` defines, beyond standard AMS math:

| Macro | Meaning |
|---|---|
| `\todo{...}` | red bold `[TODO: ...]` draft marker (remove before completion) |
| `\note{...}` | small purple inline aside |
| `\ket{}`, `\bra{}`, `\braket{}{}` | Dirac notation (via `braket`) |
| `\proj{x}` | projector $\ket{x}\!\bra{x}$ |
| `\R`, `\C`, `\N`, `\Z`, `\E`, `\Prob`, `\Hilb` | $\mathbb{R},\mathbb{C},\mathbb{N},\mathbb{Z},\mathbb{E},\mathbb{P},\mathcal{H}$ |
| `\ii`, `\dd`, `\ee` | upright $\mathrm{i}$, $\mathrm{d}$, $\mathrm{e}$ |
| `\tr`, `\Tr`, `\Var`, `\Cov`, `\rank`, `\diag`, `\poly`, `\polylog` | operators |
| `\norm{}`, `\abs{}`, `\bigo`, `\id`, `\dg` | norm, absolute value, $\mathcal{O}$, identity, dagger |
| `objectives` env | the learning-objectives box at the top of each lecture |
| `\exercisesection`, `\readingsection` | the uniform closing sections of each lecture |

Theorem environments (`theorem`, `lemma`, `proposition`, `corollary`, `definition`, `example`, `remark`, `exercise`) are numbered per chapter.
