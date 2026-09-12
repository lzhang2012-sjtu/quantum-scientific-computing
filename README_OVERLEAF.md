# Overleaf package

This archive contains the current `paper/main_cicp.tex` manuscript, a default Overleaf entry point, the optional Chinese mini report, and all referenced figures.

## English CICP manuscript (default)

- Main document: `main.tex` (a byte-for-byte mirror of `main_cicp.tex` at packaging time)
- Compiler: **pdfLaTeX**
- TeX Live version: 2024 or newer is recommended.
- Bibliography: embedded `thebibliography`; no BibTeX or Biber run is required.
- Journal class: the bundled `cicp.cls` must remain next to `main.tex`.

Upload the ZIP as a new Overleaf project. Overleaf should select `main.tex` automatically. If it does not, choose **Menu -> Main document -> main.tex** and **Compiler -> pdfLaTeX**. Compile twice so cross-references settle.

## Chinese mini report

- Main document: `mini_report_cn.tex`
- Compiler: **XeLaTeX**

To compile it in the same Overleaf project, choose **Menu -> Main document -> mini_report_cn.tex**, change **Compiler -> XeLaTeX**, and compile twice. Switch the settings back to `main.tex` and pdfLaTeX for the English manuscript.

## Package contents

- `main_cicp.tex`: authoritative English manuscript copied from `paper/main_cicp.tex`.
- `main.tex`: identical default entry point so a fresh Overleaf upload compiles immediately.
- `mini_report_cn.tex`: current Chinese mini report source.
- `cicp.cls`: local journal class dependency.
- `figs/`: exactly the 23 raster figures referenced by the two documents.
- `reference_outputs/`: locally compiled reference PDFs for visual comparison.

No files outside this archive are required for compilation. Build logs, auxiliary files, historical drafts, source-code experiments, and unreferenced figures are intentionally excluded.
