#!/usr/bin/env python3
"""Animate Grover's search for N=8 with the single marked item |011> (Example 3.24):
a signed-amplitude bar chart with the inversion-about-the-mean line, a 2-D rotation
diagram, and the success probability, stepping Start -> Oracle -> Diffuse -> Oracle ->
Diffuse with smooth morphs between stages."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

BLUE="#1f3a8a"; GOLD="#d4a017"; GREEN="#0b603b"; RED="#c0392b"; GREY="#9aa0ac"
N=8; MARKED=3; s0=1/np.sqrt(8)

def mean(v): return v.sum()/N
def oracle(v): o=v.copy(); o[MARKED]=-o[MARKED]; return o
def diffuse(v): m=mean(v); return 2*m-v

# discrete stages
ops=["Start","Oracle 1","Diffuse 1","Oracle 2","Diffuse 2"]
states=[np.full(N,s0)]
cur=states[0].copy()
for name in ops[1:]:
    cur = oracle(cur) if name.startswith("Oracle") else diffuse(cur)
    states.append(cur.copy())
pfrac=["1/8","1/8","25/32","25/32","121/128"]
show_mean=[False,True,False,True,False]

# build frames: hold each stage, then morph to the next
HOLD, MORPH = 7, 10
frames=[]   # each: (amp array, stage index s for labels, is_transition)
for i in range(len(states)):
    for _ in range(HOLD): frames.append((states[i], i, False))
    if i < len(states)-1:
        for m in range(1, MORPH):
            t=m/MORPH
            frames.append(((1-t)*states[i]+t*states[i+1], i, True))

labels=[("00"+format(k,"b"))[-3:] for k in range(N)]

def draw(fi, ax1, ax2):
    amp, si, trans = frames[fi]
    ax1.clear(); ax2.clear()
    # ----- bar chart -----
    xs=np.arange(N)
    cols=[GOLD if k==MARKED else BLUE for k in range(N)]
    ax1.bar(xs, amp, width=0.66, color=cols, alpha=0.9)
    ax1.axhline(0, color="#333", lw=1)
    if show_mean[si] and not trans:
        m=mean(amp)
        ax1.axhline(m, color=GREEN, lw=1.6, ls="--")
        ax1.text(N-0.4, m+0.02, f"mean {m:.3f}", color=GREEN, fontsize=8, ha="right")
    for k in range(N):
        ax1.text(k, amp[k]+(0.03 if amp[k]>=0 else -0.03), f"{amp[k]:.2f}",
                 ha="center", va="bottom" if amp[k]>=0 else "top", fontsize=7.5,
                 color=cols[k])
    ax1.set_xticks(xs); ax1.set_xticklabels([f"|{b}⟩" for b in labels], fontsize=8)
    ax1.get_xticklabels()[MARKED].set_color(GOLD)
    ax1.set_ylim(-0.45, 1.08); ax1.set_yticks([]); ax1.set_title("Amplitudes", fontsize=11, color=BLUE)
    for sp in ["top","right","left"]: ax1.spines[sp].set_visible(False)

    # ----- rotation diagram -----
    a=amp[0]; g=amp[MARKED]
    vx, vy = np.sqrt(7)*a, g
    nrm=np.hypot(vx,vy) or 1.0; ux,uy=vx/nrm, vy/nrm   # display on the unit circle
    th=np.linspace(0,2*np.pi,200)
    ax2.plot(np.cos(th), np.sin(th), color="#dfe3ea", lw=1.3)
    ax2.plot([-1.15,1.15],[0,0], color=GREY, lw=0.9)
    ax2.plot([0,0],[-1.15,1.15], color=GREY, lw=0.9)
    t2=np.arcsin(s0)
    ax2.plot([0,np.cos(t2)],[0,np.sin(t2)], color="#c9ccd4", lw=1.3, ls="--")
    ax2.annotate("", xy=(ux,uy), xytext=(0,0),
                 arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
    ax2.text(1.02,-0.12,r"$|\psi_0^\perp\rangle$", fontsize=9, color="#6b7280")
    ax2.text(0.04,1.04,r"$|x_0\rangle=|011\rangle$", fontsize=9, color=GOLD)
    ax2.text(ux*1.12, uy*1.12, r"$|\psi\rangle$", color=RED, fontsize=10, ha="center")
    ax2.set_xlim(-1.25,1.25); ax2.set_ylim(-1.25,1.25); ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title("Rotation picture", fontsize=11, color=BLUE)

    name = ops[si] if not trans else f"{ops[si]} → {ops[si+1]}"
    p=g*g
    fig.suptitle(f"Grover's search, $N=8$, marked $|011\\rangle$   —   {name}"
                 f"      P(|011⟩) = {p:.3f}" + (f" = {pfrac[si]}" if not trans else ""),
                 fontsize=12.5, color=BLUE, y=0.98)
    return []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.3), dpi=92,
                               gridspec_kw={"width_ratios":[1.7,1]})
fig.subplots_adjust(left=0.05, right=0.97, top=0.86, bottom=0.12, wspace=0.18)
anim=FuncAnimation(fig, draw, frames=len(frames), fargs=(ax1,ax2), blit=False)
out="animations/grover.gif"
anim.save(out, writer=PillowWriter(fps=8))
plt.close(fig)
print("saved", out, "frames:", len(frames))
