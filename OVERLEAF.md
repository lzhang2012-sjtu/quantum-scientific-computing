# Overleaf Git Integration

## Repository Information

- **Project ID**: `6aab5685ebed48e6b21c58df`  (course lecture materials; uploaded 2026-09-17)
- **Git URL**: `https://git.overleaf.com/6aab5685ebed48e6b21c58df`
- **Default branch**: `main`
- A git remote named `overleaf` is already configured in this working copy
  (`git remote -v`). Current remote head: the clean LaTeX-only upload commit.
- Previous project ID (superseded): `6a90352dd7ac4f1473c9cab5`.

## Authentication

- **Token**: `olp_39HjMwlv7bxJXWVRoO5ukftZDpVx6J0H7Ah4`
- **Token Type**: Overleaf Git authentication token
- Overleaf git tokens are **account-level**, so this token works across all
  projects on the same account. If it has expired, generate a new one at
  <https://www.overleaf.com/user/settings> and replace it above.

## Clone Command

```bash
git clone https://git:olp_39HjMwlv7bxJXWVRoO5ukftZDpVx6J0H7Ah4@git.overleaf.com/6aab5685ebed48e6b21c58df
```

## Working directory

The git repo is initialized directly in `/Users/work/Overleaf/QSC2026` (i.e., `./`).
All git commands should be run from that directory. The local default branch is
`lectures-l1-l5`; the Overleaf branch is `main`.

## What is (and isn't) uploaded

The Overleaf project holds a **clean LaTeX-only subset** (45 files): `main.tex`,
`preamble.tex`, `lectures/`, `solutions.tex` + `solutions/`, `teaching/` (teacher's
notes + `teacher_preamble.tex`), `syllabus/syllabus.tex`, `figs/`, `README.md`,
`.gitignore`. It deliberately **excludes** the large reference PDFs under `material/`,
the Jupyter `notebooks/`, `docs/`, and the `.docx` forms — because **large PDFs cause
HTTP 500 errors on Overleaf push** (see Notes), and those files are not needed to
compile the documents. All figures are TikZ/quantikz, so there are no external images.

## Compiling on Overleaf

- Lecture notes: **Menu → Main document → `main.tex`**, **Compiler → pdfLaTeX**.
- Solutions manual: compile `main.tex` first (the manual reads `main.aux` via `xr`),
  then set main document to `solutions.tex`.
- Teacher's notes (`teaching/*.tex`): pdfLaTeX.
- Syllabus (`syllabus/syllabus.tex`): switch **Compiler → XeLaTeX** (uses `ctex`).

## Pushing updates

Overleaf **prohibits force-push** and requires new commits to sit on top of its
current `main`. Because the local `lectures-l1-l5` history is unrelated to Overleaf's
`main` (and contains the large PDFs), push updates as a clean commit stacked on the
remote head — for example:

```bash
git fetch overleaf main                 # get the current Overleaf head into FETCH_HEAD
# rebuild a clean tree (LaTeX-only), commit it with FETCH_HEAD as parent, e.g. via a
# subset branch/orphan, then:
git commit-tree <clean-tree> -p FETCH_HEAD -m "Update course notes"   # -> NEWSHA
git branch -f overleaf-final <NEWSHA>
git push overleaf overleaf-final:main
```

Never `git add -A` when building the upload tree — that re-adds the `material/` PDFs
and triggers the HTTP 500 error. Add only the LaTeX source paths explicitly.

## Notes

- Overleaf requires tokens in the format: `https://git:TOKEN@git.overleaf.com/PROJECT_ID`
- SSH access may be blocked by firewall; HTTPS with token is recommended
- The token provides full read/write access to the project
- **Important**: push only source files, not compiled PDFs or reference PDFs — large
  binaries cause **HTTP 500** errors on Overleaf push (confirmed on this project)
- Overleaf forbids `git push --force`; stack changes on top of the current head instead
- Changes pushed via git appear immediately in the Overleaf web editor, which
  recompiles the PDF automatically

