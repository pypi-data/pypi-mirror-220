# from __future__ import annotations

# import pytest
# import torch

# import pyqtorch.modules as pyq


# def test_circuit_matrices() -> None:
#     n_qubits = 2
#     batch_size = 1
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     dtype = torch.cdouble

#     ops = [
#         pyq.RY([0], n_qubits),
#         pyq.RZ([1], n_qubits),
#         pyq.RX([0], n_qubits),
#     ]
#     circ = pyq.QuantumCircuit(n_qubits, ops).to(device=device, dtype=dtype)

#     state = circ.init_state(batch_size)
#     phi = torch.rand(batch_size, device=device, dtype=dtype, requires_grad=True)
#     matrices = circ.matrices(phi)
#     # breakpoint()
#     assert circ(state, phi).size() == (2, 2, batch_size)

#     state = pyq.zero_state(n_qubits, batch_size=batch_size, device=device, dtype=dtype)

#     res = circ(state, phi)
#     assert not torch.all(torch.isnan(res))

#     # g = torch.autograd.grad(circ, thetas)
#     dres_theta = torch.autograd.grad(res, phi, torch.ones_like(res), create_graph=True)[0]
#     assert not torch.all(torch.isnan(dres_theta))