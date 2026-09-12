# Overleaf Git Integration

## Repository Information

- **Project ID**: `6a90352dd7ac4f1473c9cab5`
- **Git URL**: `https://git.overleaf.com/6a90352dd7ac4f1473c9cab5`

## Authentication

- **Token**: `olp_39HjMwlv7bxJXWVRoO5ukftZDpVx6J0H7Ah4`
- **Token Type**: Overleaf Git authentication token
- Overleaf git tokens are **account-level**, so this token works across all
  projects on the same account. If it has expired, generate a new one at
  <https://www.overleaf.com/user/settings> and replace it above.

## Clone Command

```bash
git clone https://git:olp_39HjMwlv7bxJXWVRoO5ukftZDpVx6J0H7Ah4@git.overleaf.com/6a90352dd7ac4f1473c9cab5
```

## Working directory

The git repo is initialized directly in `/Users/work/Overleaf/QSC2026` (i.e., `./`).
All git commands should be run from that directory.

## Working with Changes

1. Make changes locally. The entry point is `main.tex`; lecture content lives in
   `lectures/lecNN_*.tex` and shared macros in `preamble.tex`.
2. Stage and commit source files (not build artifacts):
   ```bash
   git add main.tex preamble.tex lectures/ figs/
   git commit -m "Your commit message"
   ```
3. Stash any uncommitted build artifacts (compiled PDFs, aux files):
   ```bash
   git stash push -m "Stash build artifacts" main.pdf 2>/dev/null
   ```
4. Pull any remote changes and rebase:
   ```bash
   git pull --rebase
   ```
5. If there are merge conflicts:
   - Check conflicting files with `git status`
   - Edit the affected `.tex` file to resolve conflicts (remove `<<<<<<<`, `=======`, `>>>>>>>` markers)
   - Stage the resolved file: `git add <file>`
   - Continue rebase: `git rebase --continue`
6. Push to Overleaf:
   ```bash
   git push origin master
   ```

## Notes

- Overleaf requires tokens in the format: `https://git:TOKEN@git.overleaf.com/PROJECT_ID`
- SSH access may be blocked by firewall; HTTPS with token is recommended
- The token provides full read/write access to the project
- **Important**: Push only source files (`main.tex`, `preamble.tex`, `lectures/*.tex`,
  figures under `figs/`), not compiled PDFs or auxiliary files — large PDFs can cause
  HTTP 500 errors on Overleaf
- In the Overleaf web editor, set **Menu → Main document → main.tex** and
  **Compiler → pdfLaTeX**
- Changes pushed via git appear immediately in the Overleaf web editor, which
  recompiles the PDF automatically
