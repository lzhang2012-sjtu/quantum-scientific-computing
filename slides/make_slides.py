#!/usr/bin/env python3
"""Generate a short slide deck on physical gate implementation
(Pauli, Hadamard, and a two-qubit gate) on superconducting and neutral-atom
platforms. Schematic figures are drawn with matplotlib (no external images) and
embedded alongside the text."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ACCENT = RGBColor(0x1F, 0x3A, 0x8A)   # deep blue
SUB    = RGBColor(0x37, 0x41, 0x51)
BLUEh  = "#1f3a8a"; GOLD = "#d4a017"; GREEN = "#0b603b"; RED = "#c0392b"; GREY = "#8a90a0"

IMG = os.path.join(os.path.dirname(__file__), "img")
os.makedirs(IMG, exist_ok=True)

# =============================================================== figures
def _save(fig, name):
    p = os.path.join(IMG, name)
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p

def fig_transmon():
    """Anharmonic energy ladder + microwave (Rabi) drive of a transmon."""
    fig, ax = plt.subplots(figsize=(5.0, 2.4))
    phi = np.linspace(-2.4, 2.4, 400)
    ax.plot(phi, -np.cos(phi), color=BLUEh, lw=2, alpha=0.55)      # potential well
    levels = [(-0.70, 0.9, "0"), (-0.05, 1.25, "1"), (0.48, 1.55, "2")]
    for e, w, lab in levels:
        ax.hlines(e, -w, w, color="k", lw=1.4)
        ax.text(w + 0.12, e, rf"$|{lab}\rangle$", va="center", fontsize=11)
    ax.annotate("", xy=(0, levels[1][0]), xytext=(0, levels[0][0]),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
    ax.text(0.15, (levels[0][0] + levels[1][0]) / 2, r"$\omega_{01}$", color=RED, fontsize=11, va="center")
    xs = np.linspace(-2.25, -0.55, 120)                            # microwave drive squiggle
    ax.plot(xs, -0.70 + 0.07 * np.sin(26 * xs), color=GOLD, lw=1.3)
    ax.annotate("", xy=(-0.5, -0.70), xytext=(-0.75, -0.70),
                arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.3))
    ax.text(-2.3, -0.95, "microwave $\\pi$-pulse (Rabi)", color=GOLD, fontsize=8.5)
    ax.text(0.35, 0.95, r"$\omega_{12}\neq\omega_{01}$" + "\n(anharmonic:\nqubit isolated)",
            fontsize=8, color=BLUEh)
    ax.set_title("Transmon: anharmonic ladder driven by a resonant pulse",
                 fontsize=9.5, color=BLUEh, fontweight="bold")
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.15, 1.75); ax.axis("off")
    return _save(fig, "sc_1qubit.png")

def fig_cz():
    """CZ via a flux-tuned avoided crossing between |11> and |02>."""
    fig, ax = plt.subplots(figsize=(5.0, 2.55))
    x = np.linspace(-1, 1, 400); gap = 0.20
    d1, d2 = 0.62 * x, -0.62 * x
    avg, dif = (d1 + d2) / 2, (d1 - d2) / 2
    upper = avg + np.sqrt(dif**2 + (gap / 2)**2)
    lower = avg - np.sqrt(dif**2 + (gap / 2)**2)
    ax.plot(x, d1, "--", color=GREY, lw=1); ax.plot(x, d2, "--", color=GREY, lw=1)
    ax.plot(x, upper, color=BLUEh, lw=2.2); ax.plot(x, lower, color=GREEN, lw=2.2)
    ax.text(-0.98, 0.66, r"$|02\rangle$", color=GREY, fontsize=10)
    ax.text(-0.98, -0.72, r"$|11\rangle$", color=GREY, fontsize=10)
    ax.annotate("avoided crossing", xy=(0, gap / 2 + 0.02), xytext=(0.05, 0.62),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))
    ax.annotate("", xy=(0, gap / 2), xytext=(0, -gap / 2),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(0.04, -0.02, "conditional\nphase $\\to$ CZ", color=RED, fontsize=8.5, va="center")
    ax.set_title("Two-qubit CZ: tune $|11\\rangle\\!\\leftrightarrow\\!|02\\rangle$ to the crossing",
                 fontsize=9.5, color=BLUEh, fontweight="bold")
    ax.set_xlabel("flux / tunable-coupler bias", fontsize=8.5)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return _save(fig, "sc_2qubit.png")

def _levels(ax, x0, y0, exc=False):
    """Small hyperfine+Rydberg level stack at (x0,y0): |0>,|1>,|r>."""
    for dy, lab in [(0, "0"), (0.32, "1")]:
        ax.hlines(y0 + dy, x0 - 0.16, x0 + 0.16, color="k", lw=1.2)
        ax.text(x0 + 0.2, y0 + dy, rf"$|{lab}\rangle$", fontsize=7.5, va="center")
    ax.hlines(y0 + 0.95, x0 - 0.16, x0 + 0.16, color=RED, lw=1.2)
    ax.text(x0 + 0.2, y0 + 0.95, r"$|r\rangle$", fontsize=7.5, va="center", color=RED)
    style = dict(arrowstyle="->", color=(RED if exc else GREY), lw=1.3)
    ax.annotate("", xy=(x0, y0 + 0.93), xytext=(x0, y0 + 0.34), arrowprops=style)

def fig_tweezers():
    """Optical-tweezer array with a site-resolved addressing beam."""
    fig, ax = plt.subplots(figsize=(5.0, 2.4))
    for i in range(4):
        for j in range(2):
            x, y = i * 1.0, j * 0.9
            ax.add_patch(Circle((x, y), 0.34, color=GOLD, alpha=0.18))
            ax.plot(x, y, "o", color=BLUEh, ms=8)
    tx, ty = 1.0, 0.9                                              # addressed atom
    ax.add_patch(Polygon([[tx - 0.22, 2.05], [tx + 0.22, 2.05],
                          [tx + 0.06, ty + 0.16], [tx - 0.06, ty + 0.16]],
                         color=RED, alpha=0.35))
    ax.text(tx + 0.3, 1.75, "addressing\nbeam", color=RED, fontsize=8)
    ax.text(-0.5, -0.7, "atoms in optical tweezers; hyperfine qubit $|0\\rangle,|1\\rangle$",
            fontsize=8.5, color=BLUEh)
    ax.set_title("Neutral atoms: trapped array, focused single-qubit drive",
                 fontsize=9.5, color=BLUEh, fontweight="bold")
    ax.set_xlim(-0.6, 4.2); ax.set_ylim(-0.9, 2.2); ax.axis("off")
    return _save(fig, "na_1qubit.png")

def fig_rydberg():
    """Rydberg blockade: two atoms within R_b cannot both reach |r>."""
    fig, ax = plt.subplots(figsize=(5.0, 2.55))
    a1, a2 = (-0.75, -0.2), (0.75, -0.2)
    ax.add_patch(Circle(a1, 1.5, fill=False, ls="--", color=RED, lw=1.2))
    ax.text(a1[0] - 0.1, 1.15, r"$R_b$", color=RED, fontsize=9)
    ax.plot(*a1, "o", color=BLUEh, ms=11); ax.plot(*a2, "o", color=BLUEh, ms=11)
    ax.annotate("", xy=a2, xytext=a1, arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.text(0, -0.45, r"van der Waals $V$", ha="center", fontsize=8.5, color=GREY)
    _levels(ax, a1[0], 0.15, exc=True)
    _levels(ax, a2[0], 0.15, exc=False)
    ax.text(0, 1.75, "blockade: $|rr\\rangle$ shifted by $V$\n"
            r"$\Rightarrow$ double excitation forbidden $\Rightarrow$ CZ",
            ha="center", fontsize=8.2, color=RED)
    ax.set_title("Two-qubit CZ: the Rydberg blockade",
                 fontsize=9.5, color=BLUEh, fontweight="bold")
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-0.75, 2.15); ax.axis("off")
    return _save(fig, "na_2qubit.png")

FIGS = {"sc1": fig_transmon(), "sc2": fig_cz(), "na1": fig_tweezers(), "na2": fig_rydberg()}

# =============================================================== slides
prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
LW = 7.2   # left text-column width

def add_title(slide, text, subtitle=None):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(12.3), Inches(1.0))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; r = p.add_run(); r.text = text
    r.font.size = Pt(28); r.font.bold = True; r.font.color.rgb = ACCENT
    if subtitle:
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = subtitle
        r2.font.size = Pt(14); r2.font.italic = True; r2.font.color.rgb = SUB

def add_bullets(slide, items, left, top, width, height, size=13):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for level, text, bold in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        r = p.add_run(); r.text = text
        r.font.size = Pt(size if level == 0 else size - 1)
        r.font.bold = bold
        r.font.color.rgb = ACCENT if bold else RGBColor(0x11, 0x11, 0x11)
        p.space_after = Pt(3)

def section_header(slide, text, left, top, width):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.4))
    p = tb.text_frame.paragraphs[0]; r = p.add_run(); r.text = text
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = RGBColor(0x0B, 0x60, 0x3B)

def pic(slide, path, top):
    slide.shapes.add_picture(path, Inches(7.9), Inches(top), width=Inches(5.0))

def add_notes(slide, text):
    """Attach Chinese speaker notes (备注) explaining the slide."""
    slide.notes_slide.notes_text_frame.text = text

# ------------------------------------------------------------ Slide 1
s = prs.slides.add_slide(BLANK)
add_title(s, "Implementing gates on superconducting qubits (transmons)",
          "Pauli X/Y/Z, Hadamard, and a two-qubit gate (CZ / CNOT)")
section_header(s, "Single-qubit gates — resonant microwave drive (Rabi)", 0.5, 1.35, LW)
add_bullets(s, [
 (0, "Qubit = anharmonic LC circuit (transmon); a microwave drive at ω₀₁ addresses |0⟩↔|1⟩.", True),
 (0, "X, Y: a resonant π-pulse drives Rabi flopping; the rotation axis is set by the drive phase (I/Q). Y is X phase-shifted 90°.", False),
 (0, "Z: virtual-Z — a zero-duration software phase shift of later pulses (or a brief flux detuning).", False),
 (0, "Hadamard: compiled from {R_z, √X}, e.g. H = R_z(π/2)·SX·R_z(π/2).", False),
], 0.5, 1.78, LW, 2.2)
section_header(s, "Two-qubit gate — a tunable interaction gives a conditional phase", 0.5, 4.15, LW)
add_bullets(s, [
 (0, "CZ: flux-tune |11⟩↔|02⟩ to an avoided crossing; the conditional π phase realizes controlled-Z.", False),
 (0, "CNOT: cross-resonance (drive control at target's frequency) → ZX interaction; also CNOT = H·CZ·H.", False),
 (0, "Times ~10–50 ns (1q), ~40–300 ns (2q); limited by T₁/T₂ and leakage to |2⟩.", False),
], 0.5, 4.55, LW, 2.4)
pic(s, FIGS["sc1"], 1.5)
pic(s, FIGS["sc2"], 4.15)
add_notes(s, """【超导量子比特（transmon 传输子）】
· 量子比特是一个非谐振荡器：电容与约瑟夫森结并联。用频率 ω01 的微波脉冲驱动 |0⟩↔|1⟩。因为能级不等间距（ω12 ≠ ω01），可只驱动 |0⟩-|1⟩ 而不泄漏到 |2⟩。
· 单比特门 X、Y：共振 π 脉冲产生拉比（Rabi）振荡；旋转轴由驱动相位（I/Q）决定，Y 即 X 相移 90°。
· Z 门：常用“虚拟 Z”——对后续脉冲做零时长的软件相位平移；或用磁通短暂失谐。
· Hadamard 非原生门，由 {R_z, √X} 编译，例如 H = R_z(π/2)·SX·R_z(π/2)。
· 两比特 CZ：调节磁通/可调耦合器，使 |11⟩ 与 |02⟩ 到达“避免交叉”，得到的条件 π 相位即受控 Z；CNOT 可用交叉共振，或 H·CZ·H。
· 典型门时间：单比特约 10–50 ns，两比特约 40–300 ns；主要受 T1/T2 退相干与向 |2⟩ 泄漏限制。
· 左图：非谐势阱中的能级与微波驱动。右图：CZ 的避免交叉。""")

# ------------------------------------------------------------ Slide 2
s = prs.slides.add_slide(BLANK)
add_title(s, "Implementing gates on neutral atoms (Rydberg arrays)",
          "Qubits = two hyperfine ground states of atoms in optical tweezers")
section_header(s, "Single-qubit gates — resonant Rabi rotations", 0.5, 1.35, LW)
add_bullets(s, [
 (0, "Drive the hyperfine qubit with a global microwave field or a two-photon optical Raman pair.", True),
 (0, "X, Y: resonant π-pulse, axis set by the drive phase (as for transmons); Z by detuning / light shift.", False),
 (0, "Hadamard: a π/2 rotation (composition of resonant pulses).", False),
 (0, "Site-resolved gates use tightly focused addressing (light-shift) beams.", False),
], 0.5, 1.78, LW, 2.2)
section_header(s, "Two-qubit CZ — the Rydberg blockade", 0.5, 4.15, LW)
add_bullets(s, [
 (0, "Excite |1⟩→|r⟩ (high-lying Rydberg); nearby Rydberg atoms interact strongly (van der Waals).", False),
 (0, "Within blockade radius R_b, double excitation is forbidden — the conditional shift gives CZ (Jaksch π–2π–π, or global Levine–Pichler). CNOT = H·CZ·H.", False),
 (0, "Identical qubits, long coherence, movable/reconfigurable connectivity; ~hundreds of ns; Rydberg decay is a key error.", False),
], 0.5, 4.55, LW, 2.4)
pic(s, FIGS["na1"], 1.5)
pic(s, FIGS["na2"], 4.15)
add_notes(s, """【中性原子（里德堡阵列）】
· 量子比特 = 光镊（optical tweezers）中原子的两个超精细基态 |0⟩、|1⟩。
· 单比特门：用全局微波场或双光子拉曼（Raman）对驱动比特跃迁。X、Y 为共振 π 脉冲，轴由驱动相位决定（与超导相同）；Z 用失谐或光频移（可做成虚拟 Z）。
· 位点选址：用紧聚焦的寻址（光频移）光束单独作用于目标原子，实现单比特寻址门。
· 两比特 CZ：里德堡阻塞（Rydberg blockade）。用激光把 |1⟩ 激发到高里德堡态 |r⟩；阻塞半径 R_b 内两原子的范德瓦尔斯相互作用很强，禁止同时双激发（|rr⟩ 被移出共振），由此条件相移得到 CZ（如 Jaksch π–2π–π，或全局的 Levine–Pichler 方案）；CNOT = H·CZ·H。
· 特点：比特全同、相干时间长、连接可重构（原子可移动）；门时间约数百 ns；里德堡态衰变是主要误差源。
· 左图：光镊阵列与寻址光束。右图：里德堡阻塞。""")

# ------------------------------------------------------------ Slide 3 (comparison table)
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
    para.runs[0].font.size = Pt(15); para.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cell.fill.solid(); cell.fill.fore_color.rgb = ACCENT
for i in range(1, len(rows)):
    for j in range(3):
        cell = table.cell(i, j); cell.text = rows[i][j]
        r = cell.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(13); r.font.bold = (j == 0)
        if j == 0:
            r.font.color.rgb = ACCENT
add_bullets(s, [
 (0, "Common thread — single-qubit: a resonant drive gives Rabi rotations; phase sets the axis (X vs Y), detuning/frame sets Z.", True),
 (0, "Common thread — two-qubit: a tunable interaction (avoided crossing, cross-resonance, or Rydberg blockade) imprints a conditional phase → CZ/CNOT.", True),
], 0.5, 5.4, 12.3, 1.7, size=14)
add_notes(s, """【小结：同一原理，不同硬件“旋钮”】
· 单比特门的共同点：一个共振驱动产生拉比旋转；相位设定旋转轴（X 对 Y），失谐/参考系设定 Z。
· 两比特门的共同点：一个可调相互作用（避免交叉、交叉共振、或里德堡阻塞）施加条件相位，由此得到 CZ/CNOT。
· 区别只在实现的“旋钮”不同：超导用磁通/可调耦合器/交叉共振；中性原子用里德堡阻塞。
· 表格逐行对照 X/Y、Z、Hadamard、两比特门在两个平台上的实现方式。""")

out = os.path.join(os.path.dirname(__file__), "gate_implementations.pptx")
prs.save(out)
print("saved", out, "slides:", len(prs.slides._sldIdLst), "figures:", list(FIGS.values()))
