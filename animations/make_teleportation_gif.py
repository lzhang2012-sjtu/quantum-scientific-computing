#!/usr/bin/env python3
"""Animate the quantum teleportation protocol as a GIF:
a time-cursor sweeps across the 3-wire circuit, highlighting each gate/step,
with a running caption and the |psi> token transferred from Alice (q1) to Bob (q3)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

# wire y-positions
Y = {"q1": 3.0, "q2": 2.0, "q3": 1.0}
BLUE="#1f3a8a"; GREY="#c9ccd4"; RED="#c0392b"; GREEN="#0b603b"; GOLD="#d4a017"

# gate columns: (x, kind, payload)
#   H:(wire,label) ; CX:(ctrl,targ) ; M:(wire) ; BOX:(wire,label)
GATES = [
    (1.4, "H",  ("q2","H")),
    (2.3, "CX", ("q2","q3")),          # Bell pair prep
    (3.7, "CX", ("q1","q2")),          # Alice entangles
    (4.6, "H",  ("q1","H")),           # Alice H
    (5.6, "M",  ("q1",)),              # measure q1
    (5.6, "M",  ("q2",)),              # measure q2
    (7.4, "BOX",("q3","X^{m_2}")),     # Bob correction
    (8.4, "BOX",("q3","Z^{m_1}")),     # Bob correction
]
XL, XR = 0.2, 9.6
# stage captions keyed by cursor x-threshold
STAGES = [
    (1.3,  r"Initial: Alice holds the unknown $|\psi\rangle$ on q1; q2,q3 are a shared Bell pair."),
    (2.7,  r"Bell pair $|\Phi^+\rangle$ on q2--q3 (prepared earlier, when Alice & Bob were together)."),
    (4.1,  r"Alice applies CNOT (q1$\to$q2): she entangles her message with her Bell half."),
    (5.2,  r"Alice applies H to q1."),
    (6.6,  r"Alice measures q1,q2 $\to$ two classical bits $(m_1,m_2)$; each of 4 outcomes has prob $1/4$."),
    (7.9,  r"The 2 classical bits travel to Bob over an ordinary channel (no faster than light)."),
    (9.7,  r"Bob applies $X^{m_2}Z^{m_1}$ $\Rightarrow$ q3 becomes $|\psi\rangle$. Teleported! Source destroyed; no cloning."),
]

def caption_for(xc):
    for thr, txt in STAGES:
        if xc <= thr:
            return txt
    return STAGES[-1][1]

def draw(frame, ax, nframes):
    ax.clear()
    ax.set_xlim(-1.4, 10.2); ax.set_ylim(0.0, 4.3); ax.axis("off")
    xc = XL + (XR-XL)*frame/(nframes-1)          # cursor position
    # wires
    for w,y in Y.items():
        ax.plot([XL, XR], [y,y], color="black", lw=1.4, zorder=1)
    ax.text(-1.35, Y["q1"], r"q1  $|\psi\rangle$"+"\n(Alice)", va="center", ha="left", fontsize=9, color=BLUE)
    ax.text(-1.35, Y["q2"], "q2\n(Alice)", va="center", ha="left", fontsize=9)
    ax.text(-1.35, Y["q3"], "q3\n(Bob)",   va="center", ha="left", fontsize=9)
    # Bell-pair bracket q2-q3 at far left
    ax.annotate("", xy=(0.05,Y["q2"]), xytext=(0.05,Y["q3"]),
                arrowprops=dict(arrowstyle="-", color=GOLD, lw=2))
    ax.text(0.12, 1.5, "Bell\npair", fontsize=7.5, color=GOLD, va="center")
    # gates
    for (gx, kind, pl) in GATES:
        passed = xc >= gx
        col = BLUE if passed else GREY
        if kind == "H":
            w,lab = pl; y=Y[w]
            ax.add_patch(Rectangle((gx-0.28,y-0.28),0.56,0.56, fc="white", ec=col, lw=2, zorder=3))
            ax.text(gx,y,f"${lab}$", ha="center", va="center", fontsize=11, color=col, zorder=4)
        elif kind == "CX":
            c,t = pl; yc,yt = Y[c],Y[t]
            ax.plot([gx,gx],[yc,yt], color=col, lw=1.8, zorder=2)
            ax.add_patch(Circle((gx,yc),0.07, fc=col, ec=col, zorder=4))
            ax.add_patch(Circle((gx,yt),0.18, fc="white", ec=col, lw=2, zorder=3))
            ax.plot([gx-0.18,gx+0.18],[yt,yt], color=col, lw=1.6, zorder=4)
            ax.plot([gx,gx],[yt-0.18,yt+0.18], color=col, lw=1.6, zorder=4)
        elif kind == "M":
            w=pl[0]; y=Y[w]
            ax.add_patch(Rectangle((gx-0.28,y-0.28),0.56,0.56, fc="white", ec=col, lw=2, zorder=3))
            th=np.linspace(np.pi*0.1, np.pi*0.9, 30)
            ax.plot(gx+0.16*np.cos(th), y-0.12+0.20*np.sin(th), color=col, lw=1.3, zorder=4)
            ax.annotate("", xy=(gx+0.12,y+0.12), xytext=(gx,y-0.10),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.2), zorder=4)
        elif kind == "BOX":
            w,lab=pl; y=Y[w]
            ax.add_patch(Rectangle((gx-0.34,y-0.28),0.68,0.56, fc="white", ec=col, lw=2, zorder=3))
            ax.text(gx,y,f"${lab}$", ha="center", va="center", fontsize=10, color=col, zorder=4)
    # classical double lines from meters to Bob's corrections (appear once measured)
    if xc >= 5.6:
        for yv, off in [(Y["q1"],0.04),(Y["q2"],0.04)]:
            ax.plot([5.6,8.9],[yv+off,yv+off], color=GREEN, lw=0.9, ls=(0,(4,2)), zorder=1)
        ax.plot([8.9,8.9],[Y["q2"]+0.04,Y["q3"]+0.20], color=GREEN, lw=0.9, ls=(0,(4,2)), zorder=1)
        ax.plot([7.4,7.4],[Y["q1"]+0.04,Y["q3"]+0.20], color=GREEN, lw=0.9, ls=(0,(4,2)), zorder=1)
    # psi token: on q1 until measurement, then appears on q3 after corrections
    if xc < 5.6:
        ax.add_patch(Circle((max(XL,min(xc,5.2)) if False else 0.7, Y["q1"]),0.0))  # no moving token pre-meas (kept simple)
        ax.text(0.9, Y["q1"]+0.33, r"$|\psi\rangle$", color=RED, fontsize=11, ha="center")
    if xc >= 8.4:
        ax.text(9.4, Y["q3"]+0.33, r"$|\psi\rangle$", color=RED, fontsize=12, ha="center", fontweight="bold")
        ax.annotate("", xy=(9.4,Y["q3"]+0.18), xytext=(0.9,Y["q1"]+0.18),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.4,
                                    connectionstyle="arc3,rad=-0.25"), zorder=5)
    # time cursor
    ax.plot([xc,xc],[0.5,3.6], color=RED, lw=1.6, alpha=0.7, zorder=6)
    # title + caption
    ax.text(4.4, 4.15, "Quantum teleportation", ha="center", fontsize=14, fontweight="bold", color=BLUE)
    ax.text(-1.35, 0.28, caption_for(xc), ha="left", va="center", fontsize=9.5, wrap=True)
    return []

def main():
    fig, ax = plt.subplots(figsize=(10.5,4.4), dpi=90)
    nframes = 64
    anim = FuncAnimation(fig, draw, frames=nframes, fargs=(ax,nframes), blit=False)
    out = "animations/teleportation.gif"
    anim.save(out, writer=PillowWriter(fps=9))
    plt.close(fig)
    print("saved", out)

if __name__ == "__main__":
    main()
