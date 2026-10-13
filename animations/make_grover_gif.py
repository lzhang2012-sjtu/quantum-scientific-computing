#!/usr/bin/env python3
"""Animate Grover's search for N=16 with the single marked item |0101>=|5> (Example 3.24):
a signed-amplitude bar chart with the inversion-about-the-mean line, a 2-D rotation
diagram, and the success probability, stepping Start -> Oracle -> Diffuse through FIVE
iterations with smooth morphs between stages. The optimum is k=3; iterations 4 and 5
deliberately over-rotate, so the marked bar grows to its peak at k=3 and then shrinks."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

BLUE="#1f3a8a"; GOLD="#d4a017"; GREEN="#0b603b"; RED="#c0392b"; GREY="#9aa0ac"
N=16; MARKED=5; s0=1/np.sqrt(N)

def mean(v): return v.sum()/N
def oracle(v): o=v.copy(); o[MARKED]=-o[MARKED]; return o
def diffuse(v): m=mean(v); return 2*m-v

# discrete stages: Start, then (Oracle k, Diffuse k) for k=1..5
ops=["Start"]
for k in range(1,6): ops += [f"Oracle {k}", f"Diffuse {k}"]
states=[np.full(N,s0)]
cur=states[0].copy()
for name in ops[1:]:
    cur = oracle(cur) if name.startswith("Oracle") else diffuse(cur)
    states.append(cur.copy())
# success-probability label per stage (|marked|^2); oracle leaves it unchanged
show_mean=[s.startswith("Oracle") for s in ops]  # dashed mean drawn right after a sign flip

# build frames: hold each stage, then morph to the next
HOLD, MORPH = 6, 9
frames=[]   # each: (amp array, stage index s for labels, is_transition)
for i in range(len(states)):
    for _ in range(HOLD): frames.append((states[i], i, False))
    if i < len(states)-1:
        for m in range(1, MORPH):
            t=m/MORPH
            frames.append(((1-t)*states[i]+t*states[i+1], i, True))

labels=[format(k,"04b") for k in range(N)]

def draw(fi, ax1, ax2):
    amp, si, trans = frames[fi]
    ax1.clear(); ax2.clear()
    # ----- bar chart -----
    xs=np.arange(N)
    cols=[GOLD if k==MARKED else BLUE for k in range(N)]
    ax1.bar(xs, amp, width=0.74, color=cols, alpha=0.9)
    ax1.axhline(0, color="#333", lw=1)
    if show_mean[si] and not trans:
        m=mean(amp)
        ax1.axhline(m, color=GREEN, lw=1.6, ls="--")
        ax1.text(N-0.4, m+0.02, f"mean {m:.3f}", color=GREEN, fontsize=8, ha="right")
    # value label on the marked bar only (16 bars are too dense to label them all)
    ax1.text(MARKED, amp[MARKED]+(0.03 if amp[MARKED]>=0 else -0.03), f"{amp[MARKED]:.3f}",
             ha="center", va="bottom" if amp[MARKED]>=0 else "top", fontsize=8.5, color=GOLD)
    ax1.set_xticks(xs); ax1.set_xticklabels([f"{b}" for b in labels], fontsize=6.3, rotation=90)
    ax1.get_xticklabels()[MARKED].set_color(GOLD)
    ax1.set_ylim(-0.38, 1.08); ax1.set_yticks([])
    ax1.set_title("Amplitudes  (marked |0101⟩ in gold, mean dashed)", fontsize=10.5, color=BLUE)
    for sp in ["top","right","left"]: ax1.spines[sp].set_visible(False)

    # ----- rotation diagram -----
    a=amp[0]; g=amp[MARKED]                       # amp[0] is a representative unmarked amplitude
    vx, vy = np.sqrt(N-1)*a, g
    nrm=np.hypot(vx,vy) or 1.0; ux,uy=vx/nrm, vy/nrm
    th=np.linspace(0,2*np.pi,200)
    ax2.plot(np.cos(th), np.sin(th), color="#dfe3ea", lw=1.3)
    ax2.plot([-1.15,1.15],[0,0], color=GREY, lw=0.9)
    ax2.plot([0,0],[-1.15,1.15], color=GREY, lw=0.9)
    t2=np.arcsin(s0)
    ax2.plot([0,np.cos(t2)],[0,np.sin(t2)], color="#c9ccd4", lw=1.3, ls="--")
    ax2.annotate("", xy=(ux,uy), xytext=(0,0),
                 arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
    ax2.text(1.02,-0.12,r"$|\psi_0^\perp\rangle$", fontsize=9, color="#6b7280")
    ax2.text(0.04,1.04,r"$|x_0\rangle=|0101\rangle$", fontsize=9, color=GOLD)
    ax2.text(ux*1.12, uy*1.12, r"$|\psi\rangle$", color=RED, fontsize=10, ha="center")
    ax2.set_xlim(-1.25,1.25); ax2.set_ylim(-1.25,1.25); ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title("Rotation picture", fontsize=11, color=BLUE)

    name = ops[si] if not trans else f"{ops[si]} → {ops[si+1]}"
    tag = "  (optimum)" if ops[si]=="Diffuse 3" and not trans else \
          ("  (over-rotation)" if ops[si] in ("Diffuse 4","Diffuse 5") and not trans else "")
    p=g*g
    fig.suptitle(f"Grover's search, $N=16$, marked $|0101\\rangle=|5\\rangle$   —   {name}{tag}"
                 f"      P(|0101⟩) = {p:.3f}",
                 fontsize=12.5, color=BLUE, y=0.98)
    return []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.4), dpi=92,
                               gridspec_kw={"width_ratios":[1.9,1]})
fig.subplots_adjust(left=0.04, right=0.97, top=0.86, bottom=0.17, wspace=0.16)
anim=FuncAnimation(fig, draw, frames=len(frames), fargs=(ax1,ax2), blit=False)
out="animations/grover.gif"
anim.save(out, writer=PillowWriter(fps=8))
plt.close(fig)
print("saved", out, "frames:", len(frames), "stages:", len(states))
