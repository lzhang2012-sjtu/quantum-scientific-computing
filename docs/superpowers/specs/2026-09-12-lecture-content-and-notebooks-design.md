# Design: Writing Lecture Content + UnitaryLab Companion Notebooks

**Date:** 2026-09-12
**Depends on:** `2026-08-27-qsc-course-notes-design.md` (the 20-lecture syllabus and
LaTeX scaffold). This spec covers *filling in content* for the first 5 lectures
and adding companion Python notebooks — it does not change the syllabus.

## Goal

Turn the `\todo`-body scaffold of lectures L1–L5 into full, worked lecture notes,
drawing on the repo's reference materials; add a separate instructor solutions
manual; and add UnitaryLab companion notebooks (Lecture 1 built and executed,
the rest outlined).

## Decisions (locked with instructor)

1. **Syllabus order unchanged.** Write the spec's existing Part I: L1 Quantum
   Computation Basics, L2 Quantum Channels/Distances/Statistics, L3 Grover &
   Amplitude Amplification, L4 QFT & Phase Estimation, L5 Applications of Phase
   Estimation.
2. **Reuse & adapt `material/notes/`.** The six existing worked lectures are the
   instructor's own material; rewrap them to the course `preamble.tex` and merge/
   split into the proper lecture slots (mapping below).
3. **Full depth.** Definitions, theorems *with proofs*, worked examples, and
   exercises — matching the depth of `material/notes/lecture1.tex`.
4. **Solutions in a separate document (option A).** Lecture files contain only the
   exercises; a standalone solutions manual (`solutions.tex` → `solutions/solNN_*.tex`)
   holds the worked solutions, so students get a problems-only build.
5. **Notebooks = narrative teaching companions** using `unitarylab` v1.1.4.
   Lecture-1 notebook is built and executed; L2–L5 notebooks are outlined this pass.
6. **This pass produces:** `lectures/lec01–05` content, `solutions/sol01–05`,
   `notebooks/lec01_*.ipynb` (run), and outlines/README for the rest.

## Reference → lecture content map (Part I)

| Lecture | Primary source | Supporting source |
|---|---|---|
| **L1 Quantum Computation Basics** | `notes/lec1` (states, Hilbert space, Dirac, Bloch, tensor products, entanglement) + `notes/lec2` (unitaries as gates, single/multi-qubit gates, circuits, Bell state, universal sets & compilation, no-cloning) | Density operators / mixed states and complexity notions from Lin Lin *qasc* Ch.1, *live* Ch.2 |
| **L2 Quantum Channels, Distances & Statistical Estimates** | Lin Lin *live_notes* Ch.3 (probability, quantum channels/CPTP, trace distance, fidelity, diamond norm) | *live_notes* Ch.8 (concentration inequalities, statistical amplification, parameter estimation, Cramér–Rao). *No `notes/` source — written fresh from the PDFs.* |
| **L3 Grover & Amplitude Amplification** | `notes/lec3` (query/oracle model, phase kickback, Hadamard transform, Deutsch, Deutsch–Jozsa, Bernstein–Vazirani as warm-up) + `notes/lec4` (unstructured search, two reflections, invariant plane/rotation, optimal iteration count, multiple solutions & amplitude amplification, Ω(√N) lower bound) | Lin Lin *qasc* Ch.2; Childs notes |
| **L4 QFT & Phase Estimation** | `notes/lec5` (QFT: definition, unitarity, tensor/product form, circuit, gate count, applications) + `notes/lec6` (phase-estimation problem, Hadamard test, single-qubit PE, Kitaev bit-by-bit, controlled powers/phase register, standard QPE, precision analysis, eigenstate preparation) | Lin Lin *qasc* Ch.3; *live* Ch.16 |
| **L5 Applications of Phase Estimation** | Lin Lin *qasc* Ch.4 (ground-state energy estimation, amplitude estimation, HHL preview, Poisson) | *live* Ch.16 (amplitude estimation, Heisenberg limit), Ch.18 (eigenvalue problems, near-optimal ground-state prep). *Written fresh from the PDFs.* |

Content-organization notes:
- L1 absorbs two `notes/` chapters; keep it coherent by ordering
  states → gates/circuits → measurement → no-cloning → density operators →
  complexity. It is the longest lecture.
- Deutsch/Deutsch–Jozsa/Bernstein–Vazirani (from `notes/lec3`) serve as the
  oracle-model warm-up *inside L3* before Grover, matching the spec's L3
  ("query complexity" is already a listed objective).

## File structure (added/changed)

```
lectures/lec01_..05_*.tex     # \todo bodies replaced with full content; exercises kept, NO inline solutions
solutions.tex                 # NEW master: instructor solutions manual (book class, reuses preamble)
solutions/sol01_..05_*.tex    # NEW: one solutions chapter per lecture
notebooks/lec01_quantum_computation_basics.ipynb   # NEW: built + executed
notebooks/README.md           # NEW: UnitaryLab install + verified API cheatsheet + how to run
notebooks/lec02..05 outlines  # cell-outline stubs (markdown plan inside each .ipynb or in README)
```

### Solutions-manual mechanism
- Each exercise in a lecture gets a stable label, e.g. `\label{ex:lec01-3}`.
- `solutions.tex` uses the `xr` package: `\externaldocument{main}` so solution
  entries reference the same exercise numbers as the compiled lecture notes.
- `solutions/solNN_*.tex` mirrors the lecture's chapter title and lists
  `solution` environments (reusing the `solution` env style from `notes/preamble`).
- Result: `main.tex` → student notes (problems only); `solutions.tex` → instructor key.
- `preamble.tex` gains a `solution` environment (unnumbered, italic "Solution." lead-in).

## UnitaryLab notebook conventions

Verified locally against `unitarylab` **1.1.4**:

```python
from unitarylab.core import Circuit         # (Register also available)
qc = Circuit(n, name="...")                 # n qubits
qc.h(0); qc.x(1); qc.cx(0, 1); qc.rx(theta, 0); qc.mcx([0,1], 2)   # Qiskit-like gates
qc.initialize(state_vector, target=[...])   # load an explicit amplitude vector
qc.append(subcircuit, target=[...]); qc.dagger()
res = qc.execute(backend="numpy", device="cpu", dtype=np.complex128)  # 'torch' also works
res.state            # complex statevector (np array)
res.probabilities    # {bitstring: prob}
res.counts           # sampled counts (uses shots=...)
qc.draw(filename=...); qc.to_qasm()          # visualize / export
```

**Lecture-1 notebook content** (each concept = markdown + runnable cell, executed):
1. Building a qubit state; amplitudes and normalization.
2. Computational basis, `|+>/|->`, and measurement probabilities via `res.probabilities`.
3. Single-qubit gates (X, Z, H) acting on states; verify against hand computation.
4. Two-qubit systems: tensor products, the CNOT, and building the Bell state
   `|B+> = (|00>+|11>)/√2`; show entanglement via correlated measurement statistics.
5. Bloch-sphere angles (θ, φ) for a state; short numeric check.
6. A "your turn" cell linking back to the L1 exercises.

Notebooks assume `pip install unitarylab unitarylab-algorithms`; the L1 notebook
is executed here so its outputs are real. L2–L5 notebooks are outlined only.

## Out of scope (this pass)
- Lectures L6–L20 content (later passes; SuzhouNotes feeds Part III/QNLA).
- Running L2–L5 notebooks.
- Pushing to Overleaf.

## Success criteria
- `main.tex` compiles with L1–L5 full content, no `\todo` left in L1–L5, no
  undefined references.
- `solutions.tex` compiles and its solution numbering matches the lecture exercises.
- `notebooks/lec01_*.ipynb` executes top-to-bottom without error and reproduces the
  expected states/probabilities (e.g., Bell state → {'00':0.5,'11':0.5}).
