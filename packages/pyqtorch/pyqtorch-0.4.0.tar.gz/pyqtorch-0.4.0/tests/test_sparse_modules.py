# from __future__ import annotations

# from typing import Callable

# import pytest
# import torch

# import pyqtorch.core as func_pyq
# import pyqtorch.modules as pyq
# from pyqtorch.modules.abstract import AbstractGate

# state_000 = pyq.zero_state(3, device="cpu", dtype=torch.cdouble)
# state_001 = pyq.X(qubits=[2], n_qubits=3)(state_000)
# state_100 = pyq.X(qubits=[0], n_qubits=3)(state_000)
# state_101 = pyq.X(qubits=[2], n_qubits=3)(pyq.X(qubits=[0], n_qubits=3)(state_000))
# state_110 = pyq.X(qubits=[1], n_qubits=3)(pyq.X(qubits=[0], n_qubits=3)(state_000))


# @pytest.mark.parametrize("batch_size", [1, 2, 4, 6])
# def test_circuit(batch_size: int) -> None:
#     n_qubits = 2
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     dtype = torch.cdouble

#     ops = [
#         pyq.X([0], n_qubits),
#         pyq.Y([1], n_qubits),
#         pyq.RX([1], n_qubits),
#         pyq.RY([0], n_qubits),
#         pyq.RZ([1], n_qubits),
#     ]
#     circ = pyq.QuantumCircuit(n_qubits, ops).to(device=device, dtype=dtype)

#     state = circ.init_state(batch_size)
#     phi = torch.rand(batch_size, device=device, dtype=dtype, requires_grad=True)
#     assert circ(state, phi).size() == (2, 2, batch_size)

#     state = pyq.zero_state(n_qubits, batch_size=batch_size, device=device, dtype=dtype)

#     res = circ(state, phi)
#     assert not torch.any(torch.isnan(res))
#     dres_theta = torch.autograd.grad(res, phi, torch.ones_like(res), create_graph=True)[0]
#     assert not torch.any(torch.isnan(dres_theta))
