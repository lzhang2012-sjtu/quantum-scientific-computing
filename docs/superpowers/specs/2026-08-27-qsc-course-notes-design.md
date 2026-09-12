# Design: Quantum Scientific Computing — Course Notes (Fall 2026–2027)

## Purpose

Lecture notes for a graduate/senior-undergraduate course **Quantum Scientific
Computing**, taught over 15 three-hour class meetings in the Fall 2026–2027
term. The notes are organized as **20 lecture units** (some 3-hour meetings
cover more than one unit), typeset in LaTeX and synced to Overleaf.

- **Audience:** senior math and physics undergraduates + graduate students.
  Comfortable with linear algebra, some numerical analysis and quantum
  mechanics; not assumed to have prior quantum-computing coursework.
- **Deliverable now:** the course *structure* and a compiling LaTeX *scaffold*
  (one file per lecture, with objectives / exercises / reading map). Detailed
  content is filled in later.

## Source material (in repo)

| File | What it is | Role |
|---|---|---|
| `qasc_notes.pdf` | Lin Lin, *Lecture Notes on Quantum Algorithms for Scientific Computation* (132 pp, 8 ch) | Core foundations + QNLA backbone |
| `live_notes_0429.pdf` | Expanded "live" version (447 pp, 21 ch, 4 parts) | Deeper QNLA, differential equations, open systems, statistics |
| `talk_QNLA_tutorial_0411.tex` | Dong An, *Quantum Numerical Linear Algebra* beamer talk | QNLA lecture framing (block encoding, LCU, QSVT, QLSP) |
| `material/ChildsA_Lecture Notes on Quantum Algorithms.pdf` | Childs, *Lecture Notes on Quantum Algorithms* | Supplementary algorithms reference |

**Topics NOT in the references** (written from scratch): tensor networks
(MPS/DMRG/TEBD), QAOA/variational algorithms, quantum LP & SDP solvers,
quantum machine learning.

## Syllabus (20 lecture units)

Allocation confirmed with the instructor: **5 foundations · 5 QNLA · 4 PDEs ·
3 tensor networks · 3 optimization & QML.**

### Part I — Foundations (L1–L5)
1. Quantum computation basics: qubits, gates, circuits, measurement, no-cloning, density operators, complexity
2. Quantum channels, distances, and statistical estimates (sampling, concentration, Cramér–Rao)
3. Grover's algorithm and amplitude amplification; query complexity
4. Quantum Fourier transform and quantum phase estimation; Hadamard test
5. Applications of QPE: amplitude estimation, ground-state energy, eigenvalue problems

### Part II — Quantum Numerical Linear Algebra (L6–L10)
6. Input models: state preparation and block encoding (sparse / structured matrices)
7. Linear combination of unitaries; block-encoding arithmetic (addition, multiplication)
8. Qubitization, Chebyshev transformations, and quantum signal processing (QSP)
9. Quantum singular value transformation (QSVT) and matrix functions; phase-factor finding
10. Quantum linear systems (QLSP): HHL, QSVT, adiabatic / Zeno; complexity landscape

### Part III — Differential Equations & Simulation (L11–L14)
11. Hamiltonian simulation I: Trotter / product formulas and commutator bounds
12. Hamiltonian simulation II: truncated Taylor/Dyson, QSVT, time-dependent, optimal scaling
13. Quantum algorithms for linear ODEs/PDEs: linear-system method, time-marching, LCHS, Schrödingerization; heat equation
14. Open quantum systems and Lindblad dynamics; nonlinear PDEs (Carleman / Cole–Hopf) overview

### Part IV — Tensor Networks (L15–L17)
15. Tensor-network states: MPS, Schmidt decomposition, canonical forms, contraction cost
16. DMRG and ground states; matrix product operators
17. Time evolution with tensor networks: TEBD, TDVP; tensor networks for simulating quantum circuits

### Part V — Optimization & Quantum Machine Learning (L18–L20)
18. Variational quantum algorithms: VQE and QAOA; adiabatic connection
19. Quantum algorithms for LP and SDP: quantum interior-point, multiplicative-weights / Gibbs-sampling SDP solvers
20. Quantum machine learning: quantum kernels, variational classifiers, data loading, barren plateaus and caveats

## LaTeX architecture

- **`main.tex`** — master, `book` class, loads `preamble.tex` and `\include`s
  the 20 lecture files under `lectures/`. Also the Overleaf entry point.
- **`preamble.tex`** — packages, quantum-computing macros (`\ket`, `\bra`,
  `\braket`, `\tr`, `\E`, `\R`, `\norm`, `\bigo`, block-encoding helpers) and
  `amsthm` theorem environments (theorem/lemma/definition/example/remark).
- **`lectures/lecNN_slug.tex`** — one `\chapter` per lecture unit. Each file
  scaffolds, per instructor's request:
  - **Learning objectives** — short bulleted goals list at the top.
  - Body sections with `\todo{...}` placeholders (content filled later).
  - **Exercises** — end-of-lecture problem section.
  - **Further reading** — per-lecture map back to Lin Lin chapters, the Dong An
    talk, Childs' notes, and key papers.
- **`figs/`** — figures (created empty for now).
- A `\todo` macro (bold red marker) flags unfinished content during drafting.

### Design principles
- One file per lecture so a single lecture can be edited/compiled in isolation.
- Consistent macro set across all lectures (defined once in `preamble.tex`).
- The scaffold must compile from day one; placeholders are visible `\todo`
  markers, never broken references.

## Overleaf integration

- New project: `https://git.overleaf.com/6a90352dd7ac4f1473c9cab5`.
- Entry point `main.tex`, compiler **pdfLaTeX**, no BibTeX (references handled
  per-lecture / inline or a later shared `.bib` — decided when content lands).
- Push sources (`main.tex`, `preamble.tex`, `lectures/*.tex`, `figs/*`); do not
  push build artifacts.

## Out of scope (now)
- Detailed lecture content (prose, proofs, worked examples) — filled per lecture later.
- Problem-set solutions.
- Slides / beamer versions.
