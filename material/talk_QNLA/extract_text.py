#!/usr/bin/env python3
"""Extract text and structure from PDF"""
import fitz
import sys

pdf_path = "../material/talk_QNLA_tutorial_0411.pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}\n")
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text().strip()
    imgs = page.get_images(full=True)
    if text or imgs:
        print(f"=== Page {page_num+1} ===")
        if imgs:
            print(f"  [HAS {len(imgs)} IMAGE(S)]")
        print(text[:500] if text else "(no text)")
        print()

doc.close()
