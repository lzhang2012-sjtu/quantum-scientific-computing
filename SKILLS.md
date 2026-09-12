# Skills Used in This Project

Conventions and workflows established while building the **Quantum Scientific
Computing** lecture notes.

## Course design

- Grounded the 20-lecture syllabus in the repo's reference PDFs: `qasc_notes.pdf`
  (Lin Lin, short notes), `live_notes_0429.pdf` (Lin Lin, expanded notes), and
  `talk_QNLA_tutorial_0411.tex` (Dong An's QNLA talk). Extracted their tables of
  contents to map lectures onto source chapters.
- Allocation agreed with the instructor: 5 foundations, 5 QNLA, 4 PDEs,
  3 tensor networks, 3 optimization & quantum machine learning.
- Tensor networks, QAOA/VQE, quantum LP/SDP, and QML are **not** in the source
  PDFs and are drafted from external references (verify citations before adding).
- The design spec lives in `docs/superpowers/specs/2026-08-27-qsc-course-notes-design.md`.

## LaTeX scaffold organization

- Master file `main.tex` (`book` class, pdfLaTeX) `\include`s one file per lecture
  from `lectures/lecNN_slug.tex`; shared macros and theorem environments live in
  `preamble.tex` (loaded via `\input{preamble}`).
- Use `\includeonly{...}` in `main.tex` to compile a single lecture quickly while
  drafting.
- Every lecture file follows one skeleton: `objectives` box → body `\section`s
  (each with a `\label{sec:lecNN-k}`) → `\exercisesection` → `\readingsection`.
  Keep this structure when filling in content.
- Unfinished content is flagged with the red `\todo{...}` macro; the scaffold must
  always compile (no dangling `\ref`/`\input` or broken environments).
- Chapter labels are `\label{ch:lecNN}`; cross-reference with `cleveref` (`\cref`).

## LaTeX / notation conventions

- All Dirac notation and math shortcuts are defined once in `preamble.tex`
  (`\ket`, `\bra`, `\braket`, `\proj`, `\tr`, `\norm`, `\bigo`, `\R`, `\C`, `\E`, …).
  Add new shared macros there, never per-lecture.
- Keep terminology consistent with the references: "block encoding",
  "qubitization", "quantum signal processing (QSP)", "quantum singular value
  transformation (QSVT)", "linear combination of unitaries (LCU)", "quantum
  linear system problem (QLSP)".
- American English spelling throughout (Schrödingerization, discretization, …).
- Teaching notes: favor motivation and worked examples over terse formalism.

## Reference verification

- Verify authors, venue, volume, and year for any reference before adding it to a
  lecture's "Further reading" list.
- For topics beyond the source PDFs, cite the canonical papers/reviews
  (e.g. Schollwöck 2011 for DMRG, Farhi et al. 2014 for QAOA, van Apeldoorn et al.
  2017 for quantum SDP solvers).

## Tooling notes

- `pdftotext`/`pdftoppm` (poppler) are **not** installed on this machine; extract
  PDF outlines with Python's `PyPDF2` (`r.outline`) instead of shell PDF tools.
- Build the notes with `latexmk -pdf main.tex` (TeX Live 2025 available locally).

## Overleaf workflow

- Clone via HTTPS with an account-level git token:
  `git clone https://git:TOKEN@git.overleaf.com/PROJECT_ID` (see `OVERLEAF.md`).
- Push only source files (`main.tex`, `preamble.tex`, `lectures/*.tex`, `figs/*`);
  do not push `main.pdf` or aux files — large PDFs cause HTTP 500 errors on Overleaf.
- Standard push workflow: commit sources, stash build artifacts, `pull --rebase`,
  resolve any conflicts, then `git push origin master`.
