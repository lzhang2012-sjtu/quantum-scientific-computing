# Lecture Content (L1–L5) + UnitaryLab Notebooks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the `\todo` bodies of lectures L1–L5 with full worked content adapted from the repo references, add a separate instructor solutions manual, and add a built-and-executed UnitaryLab companion notebook for Lecture 1 (plus outlines for L2–L5).

**Architecture:** The existing `book`-class `main.tex` + `preamble.tex` + `lectures/lecNN_*.tex` scaffold is filled in. Exercises stay in the lecture files; worked solutions live in a parallel `solutions.tex` master that `\include`s `solutions/solNN_*.tex` and pulls exercise numbers from `main.aux` via the `xr` package. Notebooks live in `notebooks/`, use `unitarylab` 1.1.4, and are narrative teaching companions.

**Tech Stack:** LaTeX (pdfLaTeX, TeX Live 2025, `latexmk`), `xr` package for cross-document refs; Python 3 + `unitarylab` 1.1.4 + Jupyter/`nbformat` for notebooks.

## Global Constraints

- American English spelling throughout (Schrödingerization, discretization, neighborhood).
- Use only shared macros from `preamble.tex` (`\ket`, `\bra`, `\braket`, `\tr`, `\norm`, `\bigo`, `\R`, `\C`, `\E`, …); add new shared macros to `preamble.tex`, never per-lecture.
- Preserve each lecture's skeleton: `objectives` box → body `\section`s → `\exercisesection` → `\readingsection`.
- Chapter label `\label{ch:lecNN}`; section labels `\label{sec:lecNN-k}`; exercise labels `\label{ex:lecNN-j}`.
- No `\todo` may remain in a completed lecture. The scaffold must always compile.
- Lecture files contain NO inline solutions; solutions go only in `solutions/`.
- Notebook API is exactly as verified (see Task 7 cheat sheet); `qc.execute(backend="numpy", dtype=np.complex128)` for deterministic statevector checks.

---

### Task 1: Build infrastructure — solution environment + solutions manual master

**Files:**
- Modify: `preamble.tex` (add `solution` environment)
- Create: `solutions.tex` (instructor manual master)
- Create: `solutions/sol00_placeholder.tex` (temporary, removed in Task 2)

**Interfaces:**
- Produces: `solution` env (unnumbered, italic "Solution." lead-in); `solutions.tex` master that uses `\usepackage{xr}`, `\externaldocument{main}`, reuses `preamble.tex`, and `\include`s `solutions/solNN_*` files. Later tasks add `solutions/solNN_*.tex` and one `\include` line each.

- [ ] **Step 1: Add the `solution` environment to `preamble.tex`**

Append after the theorem environments block:

```latex
% Solution environment (unnumbered, italic "Solution." lead-in) — used only in solutions.tex.
\newenvironment{solution}{\begin{proof}[\normalfont\itshape Solution.]}{\end{proof}}
```

- [ ] **Step 2: Create the solutions manual master `solutions.tex`**

```latex
% solutions.tex — Instructor solutions manual (build separately from main.tex).
% Reuses the shared preamble; pulls exercise numbers from main.aux via xr.
\documentclass[11pt,openany]{book}
\input{preamble}
\usepackage{xr}
\externaldocument{main}   % requires main.aux to exist (compile main.tex first)

\title{\textbf{Quantum Scientific Computing}\\[0.5em]\large Solutions Manual (Instructor)}
\author{Course Instructor}
\date{Fall 2026--2027}

\begin{document}
\frontmatter
\maketitle
\tableofcontents
\mainmatter

\include{solutions/sol00_placeholder}
% Task 2+ append: \include{solutions/solNN_slug}

\end{document}
```

- [ ] **Step 3: Create a temporary placeholder so the master compiles**

Create `solutions/sol00_placeholder.tex`:

```latex
\chapter*{About this manual}
This manual collects worked solutions to the exercises in the lecture notes.
Compile \texttt{main.tex} first so that exercise numbers resolve via \texttt{xr}.
```

- [ ] **Step 4: Verify both masters compile**

Run:
```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
```
Expected: both produce PDFs, exit 0. (Solutions PDF has only the "About" page for now.)

- [ ] **Step 5: Commit**

```bash
git add preamble.tex solutions.tex solutions/sol00_placeholder.tex
git commit -m "build: add solution environment and separate solutions manual master"
```

---

### Task 2: Lecture 1 content + solutions — Quantum Computation Basics

**Files:**
- Modify: `lectures/lec01_quantum_computation_basics.tex` (replace all `\todo` bodies)
- Create: `solutions/sol01_quantum_computation_basics.tex`
- Modify: `solutions.tex` (add `\include{solutions/sol01_quantum_computation_basics}`; delete the `sol00_placeholder` include)
- Delete: `solutions/sol00_placeholder.tex`
- Source: `material/notes/lecture1.tex`, `material/notes/lecture2.tex`; density-operator/complexity material from `qasc_notes.pdf` Ch.1 / `live_notes_0429.pdf` Ch.2

**Interfaces:**
- Consumes: `solution` env and `solutions.tex` from Task 1.
- Produces: exercise labels `ex:lec01-1 … ex:lec01-N` referenced by `sol01`.

- [ ] **Step 1: Rewrite the six L1 sections with full content**

Keep the existing `objectives` box. Replace the intro `\todo` and each section `\todo` with adapted prose from the sources, in this order (preserve the existing `\section` titles and `\label{sec:lec01-k}`):

1. *Qubits, superposition, and measurement* — adapt `notes/lecture1.tex` §"Finite-Dimensional Hilbert Spaces" + §"Dirac Notation and Quantum States": inner-product space, Dirac notation, computational basis, Born rule, global vs relative phase, Bloch parametrization (Def/Prop/proofs as in source).
2. *Multi-qubit systems and tensor products* — adapt `notes/lecture1.tex` §"Multi-Qubit Systems and Entanglement": tensor product, product vs entangled, Bell state + entanglement theorem with proof.
3. *Gates, universal gate sets, and circuits* — adapt `notes/lecture2.tex` §"Unitary Operators as Gates", §"Single-Qubit Gates", §"Multi-Qubit Gates", §"Reading Quantum Circuits", §"Building a Bell State", §"Universal Gate Sets and Compilation".
4. *The no-cloning theorem and reversibility* — adapt `notes/lecture2.tex` §"The No-Cloning Theorem" (statement + proof); add a paragraph on reversibility of unitaries.
5. *Density operators and mixed states* — write from `qasc` Ch.1.2 / `live` Ch.2.3: density operator, purity, partial trace, reduced state of a Bell pair as worked example.
6. *Complexity of quantum algorithms* — write from `qasc` Ch.1.10: query vs gate complexity, circuit depth, `\bigo` notation recap.

Rules: use `preamble.tex` macros; convert any `\ketbra` uses (preamble lacks it) to `\proj{}` or `\ket{}\!\bra{}`; do not copy `notes/` `\providecommand{\ketbra}` lines. Leave no `\todo`.

- [ ] **Step 2: Replace the three exercise stubs with 5–7 real exercises**

Reuse the problems from `notes/lecture1.tex` and `notes/lecture2.tex` (norm/normalization, ± basis, Cauchy–Schwarz equality, projector, Bloch angles, separability, Bell measurement, plus one density-operator/partial-trace problem). Each gets `\label{ex:lec01-j}`. No solutions here.

- [ ] **Step 3: Update the `\readingsection`**

Point to Lin Lin *qasc* Ch.1, *live* Ch.2, Childs Ch.1–2 (already present; refine wording).

- [ ] **Step 4: Write `solutions/sol01_quantum_computation_basics.tex`**

```latex
\chapter{Quantum Computation Basics}
% Solutions to the exercises of \cref{ch:lec01}.

\begin{solution}[Exercise~\ref{ex:lec01-1}]
% worked solution adapted from notes/lecture1.tex Solutions section
\end{solution}
% ... one solution per exercise label ex:lec01-j, adapting the worked
% solutions already present in notes/lecture1.tex and notes/lecture2.tex,
% writing fresh solutions for the density-operator problem.
```

Fill in every solution fully (no placeholders) — adapt the "Solutions" sections that already exist in `notes/lecture1.tex` (and `lecture2` if present); write the density-operator solution from scratch.

- [ ] **Step 5: Wire the solution into `solutions.tex` and drop the placeholder**

In `solutions.tex` replace `\include{solutions/sol00_placeholder}` with `\include{solutions/sol01_quantum_computation_basics}`, then `git rm solutions/sol00_placeholder.tex`.

- [ ] **Step 6: Verify compile + no leftover todo**

Run:
```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
grep -n "TODO" lectures/lec01_quantum_computation_basics.tex || echo "no TODO in lec01"
grep -c "undefined" main.log solutions.log || true
```
Expected: both PDFs build; "no TODO in lec01"; no "There were undefined references" for `ex:lec01-*` in `solutions.log`.

- [ ] **Step 7: Commit**

```bash
git add lectures/lec01_quantum_computation_basics.tex solutions/sol01_quantum_computation_basics.tex solutions.tex
git rm solutions/sol00_placeholder.tex
git commit -m "content: write Lecture 1 (quantum computation basics) + solutions"
```

---

### Task 3: Lecture 2 content + solutions — Quantum Channels, Distances & Statistical Estimates

**Files:**
- Modify: `lectures/lec02_channels_distances_statistics.tex`
- Create: `solutions/sol02_channels_distances_statistics.tex`
- Modify: `solutions.tex` (add include)
- Source: `live_notes_0429.pdf` Ch.3 (channels/distances) and Ch.8 (statistics). No `notes/` source — write fresh.

**Interfaces:**
- Consumes: Task 1 infra.
- Produces: labels `ex:lec02-1 … ex:lec02-N`.

- [ ] **Step 1: Read the source pages**

Extract the relevant text with the project's Python/PyPDF2 approach (pdftotext is unavailable):
```bash
python3 - <<'EOF'
import PyPDF2
r=PyPDF2.PdfReader("live_notes_0429.pdf")
# Ch.3 ~ printed pages; locate by searching text
for i,p in enumerate(r.pages):
    t=p.extract_text() or ""
    if "quantum channel" in t.lower() or "trace distance" in t.lower():
        print("PAGE",i); print(t[:1500]); print("="*40)
EOF
```
Use this to ground definitions/theorems.

- [ ] **Step 2: Write the five L2 sections (full depth)**

Preserve existing titles/labels. Content:
1. *Quantum channels (CPTP maps)* — definition, Kraus representation, examples (unitary, depolarizing, dephasing, measurement channel), Stinespring dilation statement.
2. *Distances between states and channels* — trace distance (definition + operational meaning), fidelity, relation `1-F ≤ D ≤ √(1-F²)`, diamond norm for channels.
3. *Elementary concentration inequalities* — Markov, Chebyshev, Hoeffding; statement + short proofs.
4. *Statistical amplification and shot budgets* — median-of-means / majority-vote amplification; number of shots for additive error ε at confidence 1−δ.
5. *Parameter estimation and the Cramér–Rao bound* — Fisher information, classical CR bound; brief note on the quantum CR bound / Heisenberg vs standard-quantum-limit scaling (forward-reference L4).

- [ ] **Step 3: Add 5–6 exercises** with labels `ex:lec02-j` (e.g., verify a channel is CPTP; compute trace distance of two qubit states; Hoeffding shot count; Fisher information of a biased-coin/Hadamard-test estimator). No solutions inline.

- [ ] **Step 4: Update `\readingsection`** → *live_notes* Ch.3 and Ch.8.

- [ ] **Step 5: Write `solutions/sol02_...tex`** — a `\chapter{...}` with one fully worked `solution` per `ex:lec02-j`.

- [ ] **Step 6: Add `\include{solutions/sol02_channels_distances_statistics}` to `solutions.tex`.**

- [ ] **Step 7: Verify + commit**

```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
grep -n "TODO" lectures/lec02_channels_distances_statistics.tex || echo "no TODO in lec02"
git add lectures/lec02_channels_distances_statistics.tex solutions/sol02_channels_distances_statistics.tex solutions.tex
git commit -m "content: write Lecture 2 (channels, distances, statistics) + solutions"
```

---

### Task 4: Lecture 3 content + solutions — Grover & Amplitude Amplification

**Files:**
- Modify: `lectures/lec03_grover_amplitude_amplification.tex`
- Create: `solutions/sol03_grover_amplitude_amplification.tex`
- Modify: `solutions.tex`
- Source: `material/notes/lecture3.tex` (oracles, Deutsch/DJ/BV) + `material/notes/lecture4.tex` (Grover, AA, lower bound)

**Interfaces:**
- Consumes: Task 1 infra.
- Produces: labels `ex:lec03-1 … ex:lec03-N`.

- [ ] **Step 1: Write the five L3 sections**, preserving titles/labels:
1. *Deutsch's algorithm* — adapt `notes/lecture3.tex` §"Query and Oracle Model", §"Phase Kickback", §"Hadamard Transform", §"Deutsch"; include Deutsch–Jozsa and Bernstein–Vazirani as the oracle-model warm-up (from the same file).
2. *The unstructured search problem* — adapt `notes/lecture4.tex` §"The Unstructured Search Problem".
3. *The Grover iteration* — adapt §"The Two Reflections and the Grover Iterate" + §"The Invariant Plane and the Rotation Picture" (with proof).
4. *Amplitude amplification* — adapt §"Optimal Iteration Count..." + §"Multiple Solutions and Amplitude Amplification".
5. *Query complexity lower bounds* — adapt §"Optimality: the Ω(√N) Lower Bound".

- [ ] **Step 2: Add exercises** (reuse `notes/lecture3.tex` and `lecture4.tex` Problems) with labels `ex:lec03-j`.

- [ ] **Step 3: `\readingsection`** → *qasc* Ch.2, *live* Ch.11, Childs.

- [ ] **Step 4: Write `solutions/sol03_...tex`** — adapt the existing "Solutions" section of `notes/lecture3.tex`; write solutions for lecture4 problems.

- [ ] **Step 5: Add include to `solutions.tex`.**

- [ ] **Step 6: Verify + commit**

```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
grep -n "TODO" lectures/lec03_grover_amplitude_amplification.tex || echo "no TODO in lec03"
git add lectures/lec03_grover_amplitude_amplification.tex solutions/sol03_grover_amplitude_amplification.tex solutions.tex
git commit -m "content: write Lecture 3 (Grover & amplitude amplification) + solutions"
```

---

### Task 5: Lecture 4 content + solutions — QFT & Phase Estimation

**Files:**
- Modify: `lectures/lec04_qft_phase_estimation.tex`
- Create: `solutions/sol04_qft_phase_estimation.tex`
- Modify: `solutions.tex`
- Source: `material/notes/lecture5.tex` (QFT) + `material/notes/lecture6.tex` (QPE)

**Interfaces:**
- Consumes: Task 1 infra.
- Produces: labels `ex:lec04-1 … ex:lec04-N`.

- [ ] **Step 1: Write the five L4 sections**, preserving titles/labels:
1. *The Hadamard test* — adapt `notes/lecture6.tex` §"The Hadamard Test".
2. *The quantum Fourier transform* — adapt `notes/lecture5.tex` (definition, unitarity, product representation, circuit, gate count).
3. *Quantum phase estimation via the QFT* — adapt `notes/lecture6.tex` §"Controlled Powers and the Phase Register" + §"Standard QPE and Exact Readout".
4. *Analysis of phase estimation* — adapt §"Precision Analysis"; include Kitaev bit-by-bit method (§"Kitaev's Bit-by-Bit Method").
5. *Heisenberg-limited and iterative variants* — adapt §"Eigenstate-Preparation Considerations"; brief iterative-PE note linking to L2 Fisher-information.

- [ ] **Step 2: Add exercises** (reuse `notes/lecture5.tex` and `lecture6.tex` Problems) with labels `ex:lec04-j`.

- [ ] **Step 3: `\readingsection`** → *qasc* Ch.3, *live* Ch.16.

- [ ] **Step 4: Write `solutions/sol04_...tex`** (write fresh solutions; `notes/lec5,6` list Problems without full solutions).

- [ ] **Step 5: Add include to `solutions.tex`.**

- [ ] **Step 6: Verify + commit**

```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
grep -n "TODO" lectures/lec04_qft_phase_estimation.tex || echo "no TODO in lec04"
git add lectures/lec04_qft_phase_estimation.tex solutions/sol04_qft_phase_estimation.tex solutions.tex
git commit -m "content: write Lecture 4 (QFT & phase estimation) + solutions"
```

---

### Task 6: Lecture 5 content + solutions — Applications of Phase Estimation

**Files:**
- Modify: `lectures/lec05_qpe_applications.tex`
- Create: `solutions/sol05_qpe_applications.tex`
- Modify: `solutions.tex`
- Source: `qasc_notes.pdf` Ch.4 + `live_notes_0429.pdf` Ch.16, Ch.18. Write fresh.

**Interfaces:**
- Consumes: Task 1 infra.
- Produces: labels `ex:lec05-1 … ex:lec05-N`.

- [ ] **Step 1: Extract source pages** (PyPDF2 approach as in Task 3) for qasc Ch.4 (ground-state energy, amplitude estimation, HHL, Poisson) and live Ch.16/18.

- [ ] **Step 2: Write the four L5 sections**, preserving titles/labels:
1. *Ground-state energy estimation* — QPE applied to `e^{-iHt}`, eigenphase → energy; success probability vs overlap.
2. *Amplitude estimation* — reduction to phase estimation of the Grover iterate; quadratic advantage over sampling; connect to L3.
3. *Eigenvalue problems and ground-state preparation* — filtering / near-optimal ground-state preparation (statement-level), overlap and gap dependence.
4. *Lower bounds* — brief: no-fast-forwarding / detectability limits at statement level, forward-referencing Part III.

- [ ] **Step 3: Add 4–6 exercises** with labels `ex:lec05-j` (e.g., energy resolution vs number of ancillas; amplitude-estimation query count for target error; overlap requirement for success probability ≥ 1/2).

- [ ] **Step 4: `\readingsection`** → *qasc* Ch.4, *live* Ch.16 & Ch.18.

- [ ] **Step 5: Write `solutions/sol05_...tex`** — full worked solutions.

- [ ] **Step 6: Add include to `solutions.tex`.**

- [ ] **Step 7: Verify + commit**

```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
grep -rn "TODO" lectures/lec0[1-5]*.tex || echo "no TODO in L1-L5"
git add lectures/lec05_qpe_applications.tex solutions/sol05_qpe_applications.tex solutions.tex
git commit -m "content: write Lecture 5 (applications of phase estimation) + solutions"
```

---

### Task 7: Lecture-1 UnitaryLab notebook (built + executed) and README

**Files:**
- Create: `notebooks/README.md`
- Create: `notebooks/lec01_quantum_computation_basics.ipynb`

**Interfaces:**
- Consumes: nothing from other tasks (self-contained; concepts mirror L1).
- Produces: an executed notebook whose outputs are real.

- [ ] **Step 1: Write `notebooks/README.md`** with install + the verified API cheat sheet:

````markdown
# Companion notebooks (UnitaryLab)

Install:
```bash
pip install unitarylab unitarylab-algorithms
```
Verified against `unitarylab` 1.1.4.

## API cheat sheet
```python
from unitarylab.core import Circuit          # Register also available
qc = Circuit(n, name="...")                   # n qubits
qc.h(0); qc.x(1); qc.z(0); qc.cx(0,1); qc.rx(theta,0); qc.mcx([0,1],2); qc.swap(0,1)
qc.initialize(vec, target=[...])              # load explicit amplitudes
qc.append(sub, target=[...]); qc.dagger()
res = qc.execute(backend="numpy", device="cpu", dtype=np.complex128)  # 'torch' also works
res.state            # complex statevector
res.probabilities    # {bitstring: prob}
res.counts           # sampled counts (pass shots=...)
qc.draw(); qc.to_qasm()
```
One notebook per lecture: `lecNN_slug.ipynb`. Lecture 1 is executed; L2–L5 are outlines.
````

- [ ] **Step 2: Author the notebook programmatically with nbformat**

Create and run a builder that emits the notebook, then execute it. Use `backend="numpy"` for deterministic checks. The builder script (run once, not committed):

```python
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
nb = new_notebook()
c = []
c.append(new_markdown_cell("# Lecture 1 — Quantum Computation Basics (UnitaryLab companion)\n\nThis notebook demonstrates the concepts of Lecture 1 using the UnitaryLab simulator (v1.1.4)."))
c.append(new_code_cell("import numpy as np\nfrom unitarylab.core import Circuit"))
# 1. A qubit state + amplitudes/normalization
c.append(new_markdown_cell("## 1. A qubit, amplitudes, and measurement\nPrepare $|+\\rangle=(|0\\rangle+|1\\rangle)/\\sqrt2$ and read off measurement probabilities."))
c.append(new_code_cell("qc = Circuit(1, name='plus')\nqc.h(0)\nres = qc.execute(backend='numpy', dtype=np.complex128)\nprint('state:', np.round(res.state,3))\nprint('probabilities:', res.probabilities)"))
# 2. Single-qubit gates X,Z,H acting; verify vs hand calc
c.append(new_markdown_cell("## 2. Single-qubit gates\nCheck $X|0\\rangle=|1\\rangle$ and $HZH=X$ on $|0\\rangle$."))
c.append(new_code_cell("qc = Circuit(1); qc.x(0)\nprint('X|0> =', np.round(qc.execute(backend='numpy').state,3))\nqc2 = Circuit(1); qc2.h(0); qc2.z(0); qc2.h(0)\nprint('HZH|0> =', np.round(qc2.execute(backend='numpy').state,3), '(expect |1>)')"))
# 3. Two qubits + Bell state + entanglement
c.append(new_markdown_cell("## 3. Two qubits, CNOT, and the Bell state\n$|B^+\\rangle=(|00\\rangle+|11\\rangle)/\\sqrt2$ shows perfectly correlated outcomes."))
c.append(new_code_cell("qc = Circuit(2, name='Bell'); qc.h(0); qc.cx(0,1)\nres = qc.execute(backend='numpy', dtype=np.complex128)\nprint('state:', np.round(res.state,3))\nprint('probabilities:', res.probabilities)\nassert abs(res.probabilities.get('00',0)-0.5)<1e-9 and abs(res.probabilities.get('11',0)-0.5)<1e-9\nprint('Bell correlations verified.')"))
# 4. initialize + Bloch angles numeric check
c.append(new_markdown_cell("## 4. Arbitrary state and Bloch angles\nLoad $\\cos(\\theta/2)|0\\rangle+e^{i\\varphi}\\sin(\\theta/2)|1\\rangle$ and recover $(\\theta,\\varphi)$."))
c.append(new_code_cell("theta, phi = np.pi/3, np.pi/4\nvec = np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)], dtype=complex)\nqc = Circuit(1); qc.initialize(vec, target=[0])\ns = qc.execute(backend='numpy', dtype=np.complex128).state\nth = 2*np.arccos(abs(s[0])); ph = np.angle(s[1])-np.angle(s[0])\nprint('recovered theta,phi =', round(th,4), round(ph,4), '(expected', round(theta,4), round(phi,4),')')"))
# 5. your turn
c.append(new_markdown_cell("## 5. Your turn\nRe-create $|-\\rangle$, verify $\\langle +|-\\rangle=0$, and build the other three Bell states. See the Lecture 1 exercises."))
nb['cells'] = c
nbf.write(nb, "notebooks/lec01_quantum_computation_basics.ipynb")
print("wrote notebook")
```

- [ ] **Step 3: Execute the notebook end-to-end and fail on error**

Run:
```bash
cd /Users/work/Overleaf/QSC2026
jupyter nbconvert --to notebook --execute --inplace notebooks/lec01_quantum_computation_basics.ipynb --ExecutePreprocessor.timeout=120
```
Expected: exit 0, no traceback; the Bell assertion and Bloch recovery print expected values.

- [ ] **Step 4: Sanity-check the executed outputs**

Run:
```bash
python3 -c "import nbformat; nb=nbformat.read('notebooks/lec01_quantum_computation_basics.ipynb',4); errs=[o for c in nb.cells if c.cell_type=='code' for o in c.get('outputs',[]) if o.get('output_type')=='error']; print('errors:', len(errs)); assert not errs"
```
Expected: `errors: 0`.

- [ ] **Step 5: Commit**

```bash
git add notebooks/README.md notebooks/lec01_quantum_computation_basics.ipynb
git commit -m "notebook: add executed UnitaryLab companion for Lecture 1 + notebooks README"
```

---

### Task 8: L2–L5 notebook outlines + final verification

**Files:**
- Create: `notebooks/lec02_channels_distances_statistics.ipynb` … `lec05_qpe_applications.ipynb` (outline-only: markdown cells listing the demos + stub code cells, NOT executed)

**Interfaces:**
- Consumes: README cheat sheet from Task 7.

- [ ] **Step 1: Create four outline notebooks**, each with a title markdown cell and a bulleted "planned demos" markdown cell, e.g.:
  - L2: sampling a Hadamard-test estimator, empirical vs Hoeffding error, trace distance of two states.
  - L3: Grover on `n=3` (reuse `unitarylab_algorithms` GroverAlgorithm), success-probability vs iteration count plot.
  - L4: build QFT via `Circuit`, run QPE on a known phase gate, precision vs ancilla count.
  - L5: ground-state energy via QPE on a small Hamiltonian; amplitude estimation query-count demo.
  Each ends with a stub code cell `# TODO(next pass): implement demo` (allowed here — these are explicitly outline-only).

- [ ] **Step 2: Final full verification**

Run:
```bash
latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode solutions.tex
grep -rn "TODO" lectures/lec0[1-5]*.tex && echo "FAIL: TODO remains" || echo "OK: no TODO in L1-L5"
```
Expected: both PDFs build; "OK: no TODO in L1-L5".

- [ ] **Step 3: Commit**

```bash
git add notebooks/lec0[2-5]_*.ipynb
git commit -m "notebook: add L2-L5 companion outlines"
```

---

## Self-Review

**Spec coverage:** L1–L5 content (Tasks 2–6) ✓; reuse & adapt `notes/` (Tasks 2,4,5) ✓; L2 & L5 fresh from PDFs (Tasks 3,6) ✓; full depth + proofs (all content tasks) ✓; separate solutions manual (Task 1 infra + per-lecture solutions) ✓; L1 notebook built & executed (Task 7) ✓; L2–L5 outlines (Task 8) ✓; notebooks README + verified API (Task 7) ✓.

**Placeholder scan:** Lecture prose is specified by source-section mapping rather than transcribed verbatim (content authoring, not code); every step names exact source files/sections. The only intentional `# TODO` markers are in the Task 8 outline notebooks, explicitly allowed. No `\todo` may remain in L1–L5 (checked in Tasks 6 & 8).

**Type/name consistency:** `solution` env, `solutions.tex`, `xr`/`\externaldocument{main}`, and exercise-label scheme `ex:lecNN-j` are defined in Task 1 and used consistently in Tasks 2–6. Notebook API names match the verified introspection (`Circuit`, `h/x/z/cx/mcx/swap/rx`, `initialize(target=)`, `execute(backend=,dtype=)`, `.state/.probabilities/.counts`).
