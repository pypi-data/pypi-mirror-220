from __future__ import annotations


from numpy import array
from torch import Tensor, einsum, bmm

from string import ascii_letters as ABC

from numpy.typing import NDArray

ABC_ARRAY: NDArray = array(list(ABC))


def _forward(
    state: Tensor, mat: Tensor, qubits: tuple, n_qubits: int
) -> Tensor:
    """
    Apply a batch execution of gates to a circuit.
    Given an tensor of states [state_0, ... state_b] and
    an tensor of gates [G_0, ... G_b] it will return the
    tensor [G_0 * state_0, ... G_b * state_b]. All gates
    are applied to the same qubit.

    Inputs:
    - state (torch.Tensor): input state of shape [2] * N_qubits + [batch_size]
    - mat (torch.Tensor): the tensor representing the gates. The last dimension
    is the batch dimension. It has to be the sam eas the last dimension of
    `state`
    - qubits (list, tuple, array): Sized iterator containing the qubits
    the gate is applied to
    - N_qubits (int): the total number of qubits of the system
    - batch_size (int): the size of the batch

    Output:
    - state (torch.Tensor): the quantum state after application of the gate.
    Same shape as `input_state`
    """
    # mat = mat.reshape([2] * len(qubits) * 2 + [batch_size])
    qubits = array(n_qubits - 1 - array(qubits))

    state_indices = ABC_ARRAY[0 : n_qubits + 1].copy()
    mat_indices = ABC_ARRAY[n_qubits + 2 : n_qubits + 2 + 2 * len(qubits) + 1].copy()
    mat_indices[len(qubits) : 2 * len(qubits)] = state_indices[qubits]
    mat_indices[-1] = state_indices[-1]

    new_state_indices = state_indices.copy()
    new_state_indices[qubits] = mat_indices[0 : len(qubits)]

    state_indices = "".join(list(state_indices))  # type: ignore
    new_state_indices = "".join(list(new_state_indices))  # type: ignore
    mat_indices = "".join(list(mat_indices))  # type: ignore

    einsum_indices = f"{mat_indices},{state_indices}->{new_state_indices}"
    # breakpoint()
    # state = einsum(einsum_indices, mat, state)


    return state.to_sparse() * mat
