# Design: Convert "Quantum Computing for PDEs" handwritten notes to LaTeX

**Date:** 2026-09-11
**Source:** `SuzhouNotes/Zhang_Quantum Computing for PDEs.pdf` — 59-page digital handwritten notebook by Lei Zhang (XJTLU, Aug 2024).

## Goal

Convert the full 59-page handwritten notebook into a clean, standalone LaTeX
project: **cleaned-up lecture notes** — faithful to the author's content and
section order, but tidied into publication-quality typesetting (consistent
headings, smoothed phrasing, fixed obvious slips). Every formula and every
figure is reproduced. Figures are **redrawn as vector art** (not cropped
images).

## Decisions (from brainstorming)

| Question | Decision |
|---|---|
| Fidelity | Cleaned-up notes (faithful content, polished typesetting). Do not preserve original color coding or page breaks. |
| Figures | Redraw everything in TikZ: circuits in `quantikz`, charts in `pgfplots`, schematics in `tikz`. |
| Structure | Standalone project inside `SuzhouNotes/`, split into per-section files. Reuse quantum macros from the QSC2026 preamble. |
| Rollout | Pilot the first section end-to-end, get sign-off, then continue. |
| Transcription mechanism | Vision transcription by Claude, page-by-page, from high-res renders. No automated handwriting-math OCR. |

## Project layout

```
SuzhouNotes/
  main.tex               % book class, pdfLaTeX; \includes section files
  preamble.tex           % packages + quantum macros (adapted from QSC2026/preamble.tex)
  sections/
    00-frontmatter.tex   % title + Feynman epigraph (page 1)
    01-<slug>.tex        % one file per major section (slugs decided from the outline)
    02-<slug>.tex
    ...
  build/                 % latexmk aux + rendered page PNGs (gitignored)
  .gitignore
  Zhang_Quantum Computing for PDEs.pdf   % source, kept in place
  docs/superpowers/specs/                % this spec + the plan
```

## Preamble & macros

- Class: `book` (title page + multi-section, ~59 pp).
- Reuse QSC2026 macros: `\ket \bra \braket \proj \tr \Tr \norm \abs \bigo \id \dg`,
  blackboard sets `\R \C \N \Z \E \Prob \Hilb`, upright `\ii \dd \ee`, and the
  theorem environments (`theorem`, `lemma`, `proposition`, `corollary`,
  `definition`, `example`, `remark`, `exercise`), numbered per section/chapter.
- Add packages this document needs: `amsmath`, `amssymb`, `braket`, `quantikz`,
  `tikz` (+ libraries), `pgfplots`, `xcolor`, `cleveref`, `hyperref`, `geometry`.
- American-English spelling throughout (Schrödingerization, discretization, etc.).

## Transcription workflow

1. **Render** all 59 pages to PNG at `-r200` into `build/pages/` via
   `gs -sDEVICE=png16m`.
2. **Outline pass:** skim every page and record, in an outline note, the major
   section titles, their page ranges, and the location of every figure. This
   fixes the `sections/*.tex` split and the file slugs.
3. **Transcribe section by section:** read each page render and write clean
   LaTeX (prose + math). Use `\todo{...}` *only* where a symbol is genuinely
   illegible. Mark each figure inline with a `% FIGURE:` note describing what to
   redraw.
4. **Redraw figures** in that section (see below), replacing the `% FIGURE:`
   notes with real `figure` environments.
5. **Compile** after each section; the document must always compile.

## Figures (redraw in TikZ)

- Quantum circuits → `quantikz`.
- Bar/line charts (e.g., the Qiskit simulator vs. IBMQ probability plots) →
  `pgfplots`, reproducing the visible numeric values (e.g., 0.027 / 0.973). Any
  value estimated from the image is flagged in a comment.
- Hand-drawn schematics / diagrams → `tikz`.
- Each figure: `figure` environment, caption, `\label{fig:...}`, referenced with
  `\cref`.

## Build & verification

- Build: `latexmk -pdf main.tex` (pdfLaTeX), aux output in `build/`.
- `.gitignore` excludes `build/`, `*.aux`, `*.log`, `*.pdf` build artifacts (the
  source PDF is kept; the compiled `main.pdf` is not committed).
- **Pilot done =** first section compiles cleanly, math renders correctly,
  figures are redrawn as TikZ, and there are no stray `\todo` markers beyond
  genuinely-illegible spots. User reviews the pilot PDF before the rest proceeds.

## Pilot scope

The first major section: the title/epigraph page (frontmatter) through the
"Preliminary for Quantum Computation / State-space postulate" material — the
opening pages. Exact page range confirmed after the outline pass.

## Out of scope

- Preserving original colors, highlights, or page layout.
- Committing the compiled PDF.
- Any content not present in the source notebook (no added exercises, no
  expanded derivations beyond what the author wrote).

## Open items resolved at implementation time

- Exact number of sections and their slugs (from the outline pass).
- Whether any figure's chart data cannot be recovered from the render (flagged
  in-line if so).
