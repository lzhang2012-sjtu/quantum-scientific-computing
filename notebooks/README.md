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
One notebook per lecture: `lecNN_slug.ipynb`. Lecture 1 is executed; L2–L5 are outlines.
