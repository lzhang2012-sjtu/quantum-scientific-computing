# Companion notebooks (UnitaryLab)

Install:
```bash
pip install unitarylab unitarylab-algorithms
```
Verified against `unitarylab` 1.1.4.

## API cheat sheet
```python
from unitarylab.core import Circuit          # Register also available
qc = Circuit(n, name="...")                   # n qubits
qc.h(0); qc.x(1); qc.z(0); qc.cx(0,1); qc.rx(theta,0); qc.mcx([0,1],2); qc.swap(0,1)
qc.initialize(vec, target=[...])              # load explicit amplitudes
qc.append(sub, target=[...]); qc.dagger()
res = qc.execute(backend="numpy", device="cpu", dtype=np.complex128)  # 'torch' also works
res.state            # complex statevector
res.probabilities    # {bitstring: prob}
res.counts           # sampled counts (pass shots=...)
qc.draw(); qc.to_qasm()
```

Note on qubit ordering: qubit 0 is the least-significant bit, so a 3-qubit
statevector reshapes as `[q2, q1, q0]` and probability keys read `q_{n-1}…q_0`.

UnitaryLab has no Bloch-sphere plotter and qiskit is unavailable here, so the
Lecture 1 notebook defines its own matplotlib helpers: `bloch_vector(state)`
returns $(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)$ for a single-qubit
statevector, and `plot_bloch(vec, title)` renders a translucent unit sphere with
the state as an arrow (headless via `matplotlib.use("Agg")`).

One notebook per lecture: `lecNN_slug.ipynb`. Lecture 1 is executed; L2–L5 are outlines.
