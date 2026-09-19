#!/usr/bin/env python3
"""Generate a short slide deck on physical gate implementation
(Pauli, Hadamard, and a two-qubit gate) on superconducting and neutral-atom platforms."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ACCENT = RGBColor(0x1F, 0x3A, 0x8A)   # deep blue
SUB    = RGBColor(0x37, 0x4151)  if False else RGBColor(0x37, 0x41, 0x51)

prs = Presentation()
prs.slide_width  = Inches(13.333)   # 16:9
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_title(slide, text, subtitle=None):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(1.0))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; r = p.add_run(); r.text = text
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = ACCENT
    if subtitle:
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = subtitle
        r2.font.size = Pt(15); r2.font.italic = True; r2.font.color.rgb = SUB
    return slide

def add_bullets(slide, items, left, top, width, height, size=15):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for level, text, bold in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        r = p.add_run(); r.text = text
        r.font.size = Pt(size if level == 0 else size-2)
        r.font.bold = bold
        r.font.color.rgb = ACCENT if bold else RGBColor(0x11,0x11,0x11)
        p.space_after = Pt(3)
    return tb

def section_header(slide, text, left, top, width):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.4))
    p = tb.text_frame.paragraphs[0]; r = p.add_run(); r.text = text
    r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = RGBColor(0x0B,0x60,0x3B)
    return tb

# ------------------------------------------------------------------ Slide 1
s = prs.slides.add_slide(BLANK)
add_title(s, "Implementing gates on superconducting qubits (transmons)",
          "Pauli X/Y/Z, Hadamard, and a two-qubit gate (CZ / CNOT)")
section_header(s, "Single-qubit gates — resonant microwave drive (Rabi)", 0.5, 1.35, 12.3)
add_bullets(s, [
 (0,"Qubit = anharmonic LC circuit (transmon); levels |0⟩,|1⟩ set by a microwave drive at ω₀₁.",True),
 (0,"X, Y (π rotations): a shaped, resonant microwave π-pulse drives Rabi flopping; the rotation axis in the x–y plane is chosen by the drive phase (I/Q). Y is X phase-shifted by 90°.",False),
 (0,"Z (phase gate): usually a “virtual-Z” — a zero-duration software frame/phase shift of subsequent pulses; alternatively a temporary frequency detuning (flux).",False),
 (0,"Hadamard: not native; compiled from the basis {R_z, √X (SX)}, e.g. H = R_z(π/2)·SX·R_z(π/2) (equivalently a π rotation about the (x+z)/√2 axis).",False),
], 0.5, 1.75, 12.3, 2.3)
section_header(s, "Two-qubit gate — a tunable interaction imprints a conditional phase", 0.5, 4.15, 12.3)
add_bullets(s, [
 (0,"CZ: flux-tune a qubit (or a tunable coupler) to bring |11⟩ ↔ |02⟩ to an avoided crossing; the conditional π phase realizes controlled-Z.",False),
 (0,"CNOT: cross-resonance — drive the control qubit at the target's frequency to generate a ZX interaction; an echoed CR pulse plus single-qubit corrections yields CNOT (also CNOT = H·CZ·H).",False),
 (0,"Typical durations: single-qubit ~10–50 ns, two-qubit ~40–300 ns; fidelity limited by T₁/T₂ decoherence and leakage to |2⟩.",False),
], 0.5, 4.55, 12.3, 2.3)

# ------------------------------------------------------------------ Slide 2
s = prs.slides.add_slide(BLANK)
add_title(s, "Implementing gates on neutral atoms (Rydberg arrays)",
          "Qubits = two hyperfine ground states of atoms trapped in optical tweezers")
section_header(s, "Single-qubit gates — resonant Rabi rotations", 0.5, 1.35, 12.3)
add_bullets(s, [
 (0,"Drive the hyperfine qubit transition with a global microwave field, or with a two-photon optical Raman pair.",True),
 (0,"X, Y (π rotations): resonant π-pulse; axis set by the drive phase, exactly as for superconducting qubits.",False),
 (0,"Z: detuning or a laser light-shift on the target atom (can be virtual/software).",False),
 (0,"Hadamard: a π/2 rotation (composition of resonant pulses).",False),
 (0,"Site-resolved single-qubit gates use tightly focused addressing (light-shift) beams to pick out target atoms.",False),
], 0.5, 1.75, 12.3, 2.3)
section_header(s, "Two-qubit CZ — the Rydberg blockade", 0.5, 4.15, 12.3)
add_bullets(s, [
 (0,"Excite atoms from |1⟩ to a high-lying Rydberg state |r⟩ with lasers; two nearby Rydberg atoms interact strongly (van der Waals).",False),
 (0,"Within the blockade radius R_b, this interaction forbids simultaneous double excitation — the conditional shift realizes CZ (e.g. the Jaksch π–2π–π sequence, or the global two-pulse Levine–Pichler CZ). CNOT = H·CZ·H on the target.",False),
 (0,"Features: identical qubits, long coherence, reconfigurable connectivity (atoms can be moved); gate times ~ hundreds of ns; Rydberg-state decay is a key error source.",False),
], 0.5, 4.55, 12.3, 2.3)

# ------------------------------------------------------------------ Slide 3 (comparison table)
s = prs.slides.add_slide(BLANK)
add_title(s, "At a glance: same principles, different hardware knobs")
rows = [
 ("Gate", "Superconducting (transmon)", "Neutral atom (Rydberg)"),
 ("X, Y", "Resonant microwave π-pulse; axis by drive phase", "Resonant microwave/Raman π-pulse; axis by phase"),
 ("Z", "Virtual-Z (software) or flux detuning", "Detuning / light shift (can be virtual)"),
 ("Hadamard", "Compiled: R_z(π/2)·SX·R_z(π/2)", "π/2 pulse (composition of rotations)"),
 ("Two-qubit", "CZ via flux/tunable coupler; CNOT via cross-resonance", "CZ via Rydberg blockade; CNOT = H·CZ·H"),
]
tbl_shape = s.shapes.add_table(len(rows), 3, Inches(0.5), Inches(1.5), Inches(12.3), Inches(3.6))
table = tbl_shape.table
table.columns[0].width = Inches(2.2); table.columns[1].width = Inches(5.05); table.columns[2].width = Inches(5.05)
for j, cell in enumerate(table.rows[0].cells):
    cell.text = rows[0][j]
    para = cell.text_frame.paragraphs[0]; para.runs[0].font.bold = True
    para.runs[0].font.size = Pt(15); para.runs[0].font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    cell.fill.solid(); cell.fill.fore_color.rgb = ACCENT
for i in range(1, len(rows)):
    for j in range(3):
        cell = table.cell(i, j); cell.text = rows[i][j]
        r = cell.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(13); r.font.bold = (j == 0)
        if j == 0: r.font.color.rgb = ACCENT
add_bullets(s, [
 (0,"Common thread — single-qubit gates: a resonant drive produces Rabi rotations; phase sets the axis (X vs Y), detuning/frame sets Z.",True),
 (0,"Common thread — two-qubit gates: a tunable interaction (avoided crossing, cross-resonance, or Rydberg blockade) imprints a conditional phase, from which CZ/CNOT follow.",True),
], 0.5, 5.4, 12.3, 1.7, size=14)

out = "slides/gate_implementations.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides._sldIdLst))
