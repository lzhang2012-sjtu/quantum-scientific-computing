# Source Outline — "Quantum Computing for PDEs" (Lei Zhang, XJTLU, Aug 2024)

59-page handwritten notebook. PDF page numbers below; the author's own
page tags (Q1, 230, …) are noted in parentheses. Section files live in
`sections/`. The **pilot** is Chapter I (`01-preliminaries`).

## Chapter map

- **00-frontmatter** — p.1 — title + Feynman epigraph. Figures: none.

- **01-preliminaries** — pp.2–12 (Q1–Q11) — *Preliminary for Quantum Computation*.
  Covers: the 4 postulates of QM (state space, quantum operator/gates, quantum
  measurement, tensor product); Dirac notation; Pauli/Hadamard/phase/T gates;
  Clifford vs. non-Clifford; Schrödinger equation; observables & expectation;
  Bell/EPR state; CNOT; multiqubit Pauli; universal gate sets & Solovay–Kitaev;
  quantum circuit language; Toffoli; register; no-cloning & no-deleting.
  Figures (redraw in quantikz):
  - p.3 (Q2): Bloch-sphere parametrization — only a formula in the source; optional TikZ Bloch sphere schematic.
  - p.10 (Q9): single-qubit gate action diagrams; X/Z/H examples; state-transition square; CNOT; SWAP; multi-qubit gate compact form.
  - p.11 (Q10): Toffoli (CCNOT) circuit; multi-controlled "quantum if" circuit.

- **02-basic-algorithms** — pp.13–30 (Q12–Q28) — *Basic Algorithms (Quantum Primitives)*.
  Deutsch & Deutsch–Jozsa; Grover & amplitude amplification; QFT; QPE; Hadamard
  test; SWAP test.
  Figures:
  - p.13 (Q12): hand-drawn "Box 0 / Box 1" sketch (fruit-checker motivation).
  - p.14 (Q13): Deutsch's algorithm circuit.
  - p.15 (Q14): Qiskit screenshots — constant/balanced circuits, Deutsch balanced circuit, simulator vs. IBMQ probability bar charts (redraw circuits in quantikz, charts in pgfplots).
  - p.18 (Q17): Grover geometry diagram (rotation of state vectors, angles θ/2, 3θ/2).
  - p.19 (Q18): 3-qubit R_{x0} circuit (without ancilla).
  - p.22 (Q21): (real) Hadamard-test circuit.
  - p.23 (Q22): imaginary Hadamard-test circuit; SWAP-test circuit.
  - p.24 (Q23): Qiskit phase-estimation screenshots (circuits + convergence plot).
  - p.27 (Q25): controlled-rotation circuit; QFT for n=2.
  - p.28 (Q26): QFT circuit (2-qubit and general n).
  - p.30 (Q28): standard QPE-using-QFT circuit.

- **03-applications** — p.31 (Q29) — *Chapter III: Applications* (divider page; lists
  Ground State Energy Estimation, Amplitude Estimation, HHL, Poisson & Heat
  equation). Figures: none.

- **04-trotter-hamiltonian-simulation** — pp.32–34 (230–232) — *Chapter IV:
  Trotter-based Hamiltonian Simulation*. Trotter/Suzuki splitting; first/second/
  higher-order error bounds; commutator-type error bound; TFIM and
  particle-in-a-potential examples. Figures: none (all inline math).

- **05-schrodingerization** — pp.35–43 (233–241) — *Chapter V: Quantum Simulation of
  PDEs: Schrödingerization*. Warped-phase transform; heat equation; numerical
  implementation (Fourier spectral method); full discretization; heat equation
  with source term; general linear ODEs; sparse-access oracle definitions;
  Berry–Childs–Kothari simulation lemma; gate-complexity theorem.
  Figures:
  - p.36 (234): hand-drawn embedding circuit (QFT / P projection).
  - p.37 (235): hand-drawn spectral-method sketch (Gaussian bumps on [L, R]).

- **06-schrodingerisation-circuits** — pp.44–51 (Q42–Q50) — *Chapter VI: Quantum
  Circuits of Schrödingerisation*. Finite-difference & shift operators; periodic
  and Dirichlet BC; operator-decomposition lemma; heat-equation Hamiltonian;
  explicit circuit construction.
  Figures:
  - p.50 (Q48): Figures 1–4 (typeset) — circuits for W_j(γτ,λ), V_0(τ), Ṽ_0(τ), V_heat(τ).
  - p.51 (Q50): Figure 5 (typeset) — full Schrödingerisation circuit.

- **07-quantum-preconditioning** — pp.52–59 (Q51–Q58) — *Chapter VII: Quantum
  Preconditioning*. Variational form; block encoding, normalization &
  subnormalization; C_π NOT gate definitions; block-encoding propositions;
  quantum linear system problem (QLSP) definition; HHL complexity; optimal
  multilevel (BPX) preconditioning; implementation; block-encoding theorems.
  Figures:
  - p.56 (Q55): hand-drawn grid sketch (ℓ=2 mesh).
  - p.59 (Q58): Figure 6.1 (typeset) — block-encoding circuit for m²N⁻¹r.

## Coverage check

Pages 1–59 covered contiguously: 1 | 2–12 | 13–30 | 31 | 32–34 | 35–43 | 44–51 | 52–59. No gaps, no overlaps.

## Notes for transcription

- The author's page tags switch between "Q<n>" (chapters I–III, VI–VII) and a
  running "2xx" numbering (chapters IV–V); ignore for typesetting.
- Several pages paste in **typeset** excerpts (lemmas/theorems in a serif font,
  pp.9, 20, 21, 43, 50–51, 54, 55, 57–59) alongside handwriting — transcribe both
  as normal LaTeX; the typeset boxes become theorem/lemma environments.
- Color coding in the source (red keywords, blue headers, highlights) is **not**
  reproduced per the design (cleaned-up fidelity).
