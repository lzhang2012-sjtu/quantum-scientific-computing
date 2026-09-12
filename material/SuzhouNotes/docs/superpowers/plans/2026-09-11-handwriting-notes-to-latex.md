# Quantum Computing for PDEs — Handwriting-to-LaTeX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the 59-page handwritten notebook `Zhang_Quantum Computing for PDEs.pdf` into a clean, standalone, always-compiling LaTeX project, piloting the first section before doing the rest.

**Architecture:** A `book`-class master (`main.tex`) `\include`s per-section files under `sections/`. A `preamble.tex` reuses the QSC2026 quantum macros plus circuit/plot packages. Content is transcribed by reading high-resolution renders of each page (vision transcription — no automated handwriting OCR); figures are redrawn as vector art (quantikz / pgfplots / tikz).

**Tech Stack:** pdfLaTeX (TeX Live 2025), latexmk, quantikz, pgfplots, tikz, braket, cleveref, hyperref; ghostscript (`gs`) for rendering source pages.

## Global Constraints

- Fidelity: **cleaned-up notes** — faithful content and section order, polished typesetting. Do **not** reproduce original colors, highlights, or page breaks.
- Figures: **redraw as vector art** (quantikz circuits, pgfplots charts, tikz schematics). Never `\includegraphics` a crop of the source.
- Spelling: **American English** (Schrödingerization, discretization, neighborhood, etc.).
- Macros: reuse QSC2026 notation (`\ket \bra \braket \proj \tr \Tr \norm \abs \bigo \id \dg`, `\R \C \N \Z \E \Prob \Hilb`, `\ii \dd \ee`). Add new shared macros to `preamble.tex`, never per-section.
- The document **must always compile** (`latexmk -pdf main.tex` exits 0). Use `\todo{...}` only for genuinely illegible source symbols.
- Build artifacts (`build/`, `*.aux`, `*.log`, compiled `main.pdf`) are gitignored / not committed. The source PDF is kept.
- Working directory for all paths below: `/Users/work/Overleaf/QSC2026/SuzhouNotes/`.

---

## File Structure

- `main.tex` — book-class master; loads preamble, sets up front matter, `\include`s section files.
- `preamble.tex` — packages, quantum macros, theorem environments, `\todo`.
- `sections/00-frontmatter.tex` — title + Feynman epigraph (source p.1).
- `sections/NN-<slug>.tex` — one file per major section; slugs fixed by the outline pass (Task 3).
- `build/` — latexmk aux output + `build/pages/pNN.png` renders. Gitignored.
- `.gitignore` — excludes build artifacts.
- `docs/superpowers/OUTLINE.md` — the section→page-range→figures map produced in Task 3.

Verification cadence for every task: `latexmk -pdf -output-directory=build main.tex` returns exit 0, then render the affected page(s) of `build/main.pdf` and eyeball against the source render.

---

### Task 1: Project scaffold that compiles empty

**Files:**
- Create: `preamble.tex`
- Create: `main.tex`
- Create: `.gitignore`

**Interfaces:**
- Produces: `preamble.tex` (input by `main.tex`); a `book`-class `main.tex` whose body is empty except a `\todo` marker; `objectives`-free — this project doesn't use the course's lecture skeleton.

- [ ] **Step 1: Write `.gitignore`**

```gitignore
build/
*.aux
*.log
*.out
*.toc
*.fls
*.fdb_latexmk
*.synctex.gz
main.pdf
```

- [ ] **Step 2: Write `preamble.tex`**

```latex
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{braket}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc,decorations.pathreplacing}
\usepackage{quantikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{xcolor}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue]{hyperref}
\usepackage{cleveref}

% ---- draft markers ----
\newcommand{\todo}[1]{\textcolor{red}{\textbf{[TODO: #1]}}}
\newcommand{\note}[1]{{\small\textcolor{violet}{#1}}}

% ---- Dirac / linear algebra (from QSC2026) ----
\newcommand{\proj}[1]{\ket{#1}\!\bra{#1}}
\DeclareMathOperator{\tr}{tr}
\DeclareMathOperator{\Tr}{Tr}
\DeclareMathOperator{\Var}{Var}
\DeclareMathOperator{\Cov}{Cov}
\DeclareMathOperator{\rank}{rank}
\DeclareMathOperator{\diag}{diag}
\DeclareMathOperator{\poly}{poly}
\DeclareMathOperator{\polylog}{polylog}
\newcommand{\norm}[1]{\left\lVert #1 \right\rVert}
\newcommand{\abs}[1]{\left\lvert #1 \right\rvert}
\newcommand{\bigo}{\mathcal{O}}
\newcommand{\id}{\mathbb{1}}
\newcommand{\dg}{^{\dagger}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\E}{\mathbb{E}}
\newcommand{\Prob}{\mathbb{P}}
\newcommand{\Hilb}{\mathcal{H}}
\newcommand{\ii}{\mathrm{i}}
\newcommand{\dd}{\mathrm{d}}
\newcommand{\ee}{\mathrm{e}}

% ---- theorem environments, numbered per chapter ----
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{exercise}{Exercise}[chapter]
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
```

Note: `\ket`, `\bra`, `\braket` come from the `braket` package — do not redefine.

- [ ] **Step 3: Write `main.tex`**

```latex
\documentclass[11pt]{book}
\input{preamble}

\title{Quantum Computing for PDEs}
\author{Lei Zhang \\ XJTLU}
\date{August 2024}

\begin{document}
\todo{content pending}
\end{document}
```

- [ ] **Step 4: Compile and verify exit 0**

Run: `latexmk -pdf -output-directory=build main.tex`
Expected: exit 0; `build/main.pdf` exists with the red TODO marker.

- [ ] **Step 5: Commit**

(Only if the enclosing directory is a git repo; otherwise skip commit and note it.)
```bash
git add .gitignore preamble.tex main.tex
git commit -m "scaffold: standalone LaTeX project for QC-for-PDEs notes"
```

---

### Task 2: Render source pages and build the outline

**Files:**
- Create: `build/pages/p01.png` … `p59.png` (generated)
- Create: `docs/superpowers/OUTLINE.md`

**Interfaces:**
- Consumes: source `Zhang_Quantum Computing for PDEs.pdf`.
- Produces: `docs/superpowers/OUTLINE.md` — an ordered list of major sections, each with: proposed file slug, source page range, and a list of figures (with page number + one-line description of what to redraw). Later section tasks consume this map.

- [ ] **Step 1: Render all pages to PNG at 200 dpi**

```bash
mkdir -p build/pages
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r200 \
   -sOutputFile=build/pages/p%02d.png \
   "Zhang_Quantum Computing for PDEs.pdf"
```
Expected: 59 files `build/pages/p01.png` … `p59.png`.

- [ ] **Step 2: Skim every page and record the outline**

Read each render in order. In `docs/superpowers/OUTLINE.md`, write one entry per major section using this exact shape:

```markdown
## Outline

- **00-frontmatter** — pp.1 — title + Feynman epigraph. Figures: none.
- **01-<slug>** — pp.2–N — <section title>. Figures:
  - p.X: <what to redraw, e.g. "Deutsch balanced-circuit quantikz diagram">
- **02-<slug>** — pp.N–M — <section title>. Figures: none.
...
```

Rules: use the author's own section headings (the underlined/boxed titles) to set boundaries; slugs are lowercase-hyphenated; every figure across all 59 pages appears under exactly one section.

- [ ] **Step 3: Sanity-check coverage**

Confirm the page ranges are contiguous and cover pp.1–59 with no gaps or overlaps. Fix the outline if not.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/OUTLINE.md
git commit -m "docs: section/figure outline of source notebook"
```
(`build/pages/` is gitignored.)

---

### Task 3: Front matter (title + epigraph)

**Files:**
- Create: `sections/00-frontmatter.tex`
- Modify: `main.tex` (replace the `\todo` body)

**Interfaces:**
- Consumes: preamble macros.
- Produces: `sections/00-frontmatter.tex` (included first in the body).

- [ ] **Step 1: Write `sections/00-frontmatter.tex`**

```latex
\begin{titlepage}
  \centering
  \vspace*{3cm}
  {\Huge Quantum Computing for PDEs\par}
  \vspace{2cm}
  \begin{minipage}{0.8\textwidth}\itshape
    Nature isn't classical, dammit, and if you want to make a simulation of
    Nature, you'd better make it quantum mechanical. And by golly it's a
    wonderful problem, because it doesn't look so easy.
  \end{minipage}
  \par\vspace{0.5cm}
  \raggedleft --- Richard Feynman\par
  \vspace{2cm}
  \raggedleft {\large Lei Zhang}\\ XJTLU\\ August 2024\par
\end{titlepage}
```

- [ ] **Step 2: Wire it into `main.tex`**

Replace the `\todo{content pending}` line with:
```latex
\frontmatter
\input{sections/00-frontmatter}
\mainmatter
```

- [ ] **Step 3: Compile and verify**

Run: `latexmk -pdf -output-directory=build main.tex`
Expected: exit 0; title page shows title, epigraph, attribution. Compare to `build/pages/p01.png`.

- [ ] **Step 4: Commit**

```bash
git add sections/00-frontmatter.tex main.tex
git commit -m "feat: front matter (title + Feynman epigraph)"
```

---

### Task 4: PILOT — transcribe the first section (prose + math)

**Files:**
- Create: `sections/01-<slug>.tex` (slug from OUTLINE.md)
- Modify: `main.tex` (add `\include`)

**Interfaces:**
- Consumes: OUTLINE.md (page range for section 01), preamble macros.
- Produces: `sections/01-<slug>.tex` with a `\chapter{...}`, `\section{...}`s, all prose and math for the section's pages, and `% FIGURE: <desc>` placeholder comments where figures belong.

- [ ] **Step 1: Create the section file with chapter/section skeleton**

Open the section's page range from OUTLINE.md. Create `sections/01-<slug>.tex` starting with `\chapter{<author's section title>}` and the `\section{...}` headings the author uses. Add a `\label{ch:sec01}`.

- [ ] **Step 2: Transcribe prose and math, page by page**

For each page in range, read `build/pages/pNN.png` and write the content into the section file: prose as clean sentences, all mathematics using the preamble macros (`\ket`, `\bra`, matrices via `bmatrix`/`pmatrix`, tensor products `\otimes`, etc.). Keep the author's logical order. Where a figure appears, insert a line:
```latex
% FIGURE: <one-line description of what Task 5 will redraw>
```
Use `\todo{illegible: ...}` only for symbols you genuinely cannot read.

- [ ] **Step 3: Wire into `main.tex`**

Add after the front matter include:
```latex
\input{sections/01-<slug>}
```

- [ ] **Step 4: Compile and verify math renders**

Run: `latexmk -pdf -output-directory=build main.tex`
Expected: exit 0. Render the new pages of `build/main.pdf` and check each equation against the source render. Fix transcription errors.

- [ ] **Step 5: Commit**

```bash
git add sections/01-<slug>.tex main.tex
git commit -m "feat: pilot section prose + math"
```

---

### Task 5: PILOT — redraw the first section's figures in TikZ

**Files:**
- Modify: `sections/01-<slug>.tex` (replace `% FIGURE:` placeholders)

**Interfaces:**
- Consumes: the `% FIGURE:` placeholders from Task 4 and the source page renders.
- Produces: `figure` environments with `\label{fig:...}`, referenced via `\cref`.

- [ ] **Step 1: Redraw each figure**

For each `% FIGURE:` placeholder, replace it with a `figure` environment containing vector art:
- Quantum circuit → `quantikz` (`\begin{quantikz} ... \end{quantikz}`).
- Bar/line chart → `pgfplots` `axis`, reproducing the visible numeric values; add `% estimated` after any value read approximately from the image.
- Schematic → `tikz`.

Example skeleton (circuit):
```latex
\begin{figure}[t]
  \centering
  \begin{quantikz}
    \lstick{$q_0$} & \gate{H} & \ctrl{1} & \gate{H} & \meter{} \\
    \lstick{$q_1$} & \gate{X} & \targ{}  & \qw       & \qw
  \end{quantikz}
  \caption{<caption from source>}
  \label{fig:sec01-<name>}
\end{figure}
```

- [ ] **Step 2: Add cross-references**

Where the prose refers to a figure, reference it with `\cref{fig:sec01-<name>}`.

- [ ] **Step 3: Compile and verify against source**

Run: `latexmk -pdf -output-directory=build main.tex`
Expected: exit 0. Compare each redrawn figure side-by-side with its source render; adjust gate order, labels, bar heights, and captions until faithful.

- [ ] **Step 4: Commit**

```bash
git add sections/01-<slug>.tex
git commit -m "feat: pilot section figures redrawn in TikZ"
```

---

### Task 6: PILOT review gate

**Files:** none (review only)

- [ ] **Step 1: Full clean build**

Run: `latexmk -C -output-directory=build && latexmk -pdf -output-directory=build main.tex`
Expected: exit 0, no LaTeX errors, no undefined references.

- [ ] **Step 2: Stray-marker check**

Run: `grep -rn "\\\\todo" sections/01-*.tex`
Expected: only genuinely-illegible spots remain (ideally none). Resolve any others.

- [ ] **Step 3: Present the pilot PDF to the user**

Show the rendered pilot section and get sign-off before proceeding. Ask specifically about: math fidelity, figure fidelity, heading/prose style. Record any style corrections to apply to all remaining sections.

- [ ] **Step 4: STOP for user approval.** Do not start Task 7 until the user approves the pilot.

---

### Task 7+: Remaining sections (repeat per OUTLINE entry)

After pilot sign-off, instantiate one task per remaining section in OUTLINE.md, each following the **same two-phase pattern as Tasks 4–5**, applying any style corrections from the pilot review:

**Files (per section NN):**
- Create: `sections/NN-<slug>.tex`
- Modify: `main.tex` (add `\include`)

- [ ] **Step 1: Skeleton** — `\chapter{...}` + `\section{...}` + `\label{ch:secNN}` from the author's headings.
- [ ] **Step 2: Transcribe prose + math** for the section's page range from OUTLINE.md, macros per Global Constraints, `% FIGURE:` placeholders inserted.
- [ ] **Step 3: Wire `\input{sections/NN-<slug>}` into `main.tex`.**
- [ ] **Step 4: Redraw figures** (quantikz / pgfplots / tikz), captions + `\label` + `\cref`.
- [ ] **Step 5: Compile** — `latexmk -pdf -output-directory=build main.tex` exits 0; compare rendered pages to `build/pages/pNN.png`; fix errors.
- [ ] **Step 6: Stray-marker check** — `grep -rn "\\\\todo" sections/NN-*.tex`; resolve.
- [ ] **Step 7: Commit** — `git commit -m "feat: section NN <slug>"`.

Repeat until every OUTLINE section is done.

---

### Task FINAL: Whole-document verification

**Files:** none (verification), possible small fixes to `main.tex`.

- [ ] **Step 1: Clean rebuild twice** (settle ToC/cross-refs)

Run: `latexmk -C -output-directory=build && latexmk -pdf -output-directory=build main.tex && latexmk -pdf -output-directory=build main.tex`
Expected: exit 0, no "undefined references" or "multiply defined labels" warnings.

- [ ] **Step 2: Page-coverage check**

Confirm every source section from OUTLINE.md has a corresponding `\include` in `main.tex` and appears in the ToC.

- [ ] **Step 3: Global stray-marker check**

Run: `grep -rn "\\\\todo" sections/`
Expected: empty (or only genuinely-illegible source symbols, listed for the user).

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: full-document build clean, all sections included"
```

---

## Self-Review

**Spec coverage:**
- Cleaned-up fidelity → Global Constraints + Tasks 4/7 (prose polishing, author order). ✓
- Redraw figures in TikZ → Task 5, Task 7 step 4. ✓
- Standalone split-file project reusing QSC2026 macros → Tasks 1–3, `sections/` split. ✓
- Vision transcription page-by-page → Task 2 renders, Tasks 4/7 transcribe. ✓
- Pilot first, then continue → Task 6 gate before Task 7. ✓
- Build/verification (`latexmk`, gitignore, no committed PDF) → Task 1 `.gitignore`, Task FINAL. ✓
- American English, `\todo` only for illegible → Global Constraints, enforced in stray-marker checks. ✓

**Placeholder scan:** Section slugs and exact page ranges are intentionally deferred to the OUTLINE.md produced in Task 2 (the spec defines these as implementation-time outputs), not left as vague "TBD" in code steps. All code steps contain real content.

**Type/name consistency:** `preamble.tex` input by `main.tex`; `\todo` defined in Task 1 and used in checks; figure/chapter label conventions (`fig:secNN-*`, `ch:secNN`) consistent across Tasks 4/5/7; `-output-directory=build` used in every compile step.
