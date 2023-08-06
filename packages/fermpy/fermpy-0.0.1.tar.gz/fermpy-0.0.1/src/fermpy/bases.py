# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 12:09:55 2023

@author: Emil
"""

import numpy as np
import scipy.sparse as sp
from itertools import product
from collections.abc import Callable


STATE = tuple[int, ...]
STATE_COMP = dict[tuple[int, ...], float]
OP = Callable[[STATE, int | tuple[int, ...]], None | tuple[STATE, int]]
OP_FIXED = Callable[[STATE], None | tuple[STATE, int]]

def s_minus(state: STATE) -> list[STATE]:
    states_out = []
    for idx, sp_state in enumerate(state):
        if sp_state == 1:
            states_out.append(state[:idx] + (-1, ) + state[idx + 1:])
    assert len(states_out) == len(set(states_out)), states_out
    return states_out

def s_minus_composite(state_com: np.ndarray,
                      basis_states: list[STATE],
                      state_to_idx_minus: dict[STATE, int]) -> np.ndarray:
    state_com_out = np.zeros(len(state_to_idx_minus), dtype=np.float64)
    for state, val in zip(basis_states, state_com):
        states_minus = s_minus(state)
        for state_minus in states_minus:
            state_com_out[state_to_idx_minus[state_minus]] += val
    state_com_out /= np.sqrt((state_com_out**2).sum())
    return state_com_out

def inner_comp(state_comp_left: STATE_COMP, state_comp_right: STATE_COMP) -> float:
    common_states = set(state_comp_left).intersection(state_comp_right)
    ip = 0
    for state in common_states:
        ip += state_comp_left[state] * state_comp_right[state]
    return ip

def apply_operator_to_state_comp(operator: OP | OP_FIXED, state_comp: STATE_COMP,
                                 *args, **kwargs) -> STATE_COMP:
    out: STATE_COMP = {}
    for state, coeff in state_comp.items():
        if (state_to := operator(state, *args, **kwargs)) is not None:
            out[state_to[0]] = state_to[1] * coeff
    return out

def build_mat_rep_of_operator_dense(basis: list[STATE],
                                    state_to_idx: dict[STATE, int],
                                    operator: OP | OP_FIXED,
                                    *args, **kwargs) -> np.ndarray:
    N = len(basis)
    op_mat = np.zeros((N, N), dtype=np.float64)
    for j_mat, state_from in enumerate(basis):
        if (op_state := operator(state_from, *args, **kwargs)) is not None:
            i_mat = state_to_idx[op_state[0]]
            op_mat[i_mat, j_mat] = op_state[1]
    return op_mat

def build_mat_rep_of_operator_sparse(basis: list[STATE],
                                     state_to_idx: dict[STATE, int],
                                     operator: OP | OP_FIXED,
                                     *args, **kwargs) -> sp.csc_array:
    # TODO: consider the impact of .append instead of constructing the list to begin with and indexing...
    N = len(basis)
    data = []
    row_inds = []
    col_inds = []
    for j_mat, state_from in enumerate(basis):
        if (op_state := operator(state_from, *args, **kwargs)) is not None:
            i_mat = state_to_idx[op_state[0]]
            data.append(op_state[1])
            row_inds.append(i_mat)
            col_inds.append(j_mat)
    return sp.csc_array((data, (row_inds, col_inds)), shape=(N, N), dtype=np.float64)

def build_mat_rep_of_operator_comp_dense(basis: list[STATE_COMP],
                                         state_to_idxs: dict[STATE, set[int]],
                                         operator: OP | OP_FIXED,
                                         *args, **kwargs) -> np.ndarray:
    N = len(basis)
    op_mat = np.zeros((N, N), dtype=np.float64)
    for j_mat, state_comp_from in enumerate(basis):
        op_state_comp = apply_operator_to_state_comp(operator, state_comp_from,
                                                     *args, **kwargs)
        
        # Indices of states that will potentially have non-zero overlap
        is_mat = set()
        is_mat.update(*[state_to_idxs[op_state] for op_state in op_state_comp])
        for i_mat in is_mat:
            state_comp_to = basis[i_mat]
            op_mat[i_mat, j_mat] = inner_comp(state_comp_to, op_state_comp)
    return op_mat

def build_mat_rep_of_operator_comp_sparse(basis: list[STATE_COMP],
                                          state_to_idxs: dict[STATE, set[int]],
                                          operator: OP | OP_FIXED,
                                          *args, **kwargs) -> sp.csc_array:
    N = len(basis)
    data = []
    indptr = (N + 1) * [0]
    row_indices = []
    for j_mat, state_comp_from in enumerate(basis):
        op_state_comp = apply_operator_to_state_comp(operator, state_comp_from,
                                                     *args, **kwargs)
        
        # Indices of states that will potentially have non-zero overlap
        is_mat = set()
        is_mat.update(*[state_to_idxs[op_state] for op_state in op_state_comp])
        
        nums_in_col = 0
        for i_mat in is_mat:
            state_comp_to = basis[i_mat]
            ip = inner_comp(state_comp_to, op_state_comp)
            if abs(ip) > 1e-15: # Don't include very small numbers (round-off errors)
                data.append(ip)
                row_indices.append(i_mat)
                nums_in_col += 1
        indptr[j_mat + 1] = indptr[j_mat] + nums_in_col
    return sp.csc_array((data, row_indices, indptr), shape=(N, N), dtype=np.float64)


class Basis:
    
    def __eq__(self, other):
        if isinstance(other, Basis):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
    
    def _get_func_build_mat_rep_of_operator_single_QN(self, sparse)\
        -> Callable[[OP | OP_FIXED, int, ...], np.ndarray | sp.csc_array]:
        if sparse:
            return self.build_mat_rep_of_operator_single_QN_sparse
        return self.build_mat_rep_of_operator_single_QN_dense


class BasisNoSym(Basis):
    def __init__(self, N: int):
        assert N > 0, N
        self.N = N
        self.states_block: list[STATE]
        self.state_to_idx: dict[STATE, int]
        self.states_block, self.state_to_idx = self.generate_basis()
        self.qns: set[int] = {0}
        self.dims: dict[int, int] = {0: len(self.states_block)}
        self.id = ("no_sym", N)
        self.prefer_sparse: bool = (True if N > 5 else False)
    
    def generate_basis(self) -> tuple[list[STATE],
                                      dict[STATE, int]]:
        if self.N < 1:
            return
        
        states_block: list[STATE] = list(product((0, 1, -1, 2), repeat=self.N))
        state_to_idx: dict[STATE, int] = {state: idx for idx, state in enumerate(states_block)}
        
        assert len(states_block) == 4**self.N

        return states_block, state_to_idx
    
    @staticmethod
    def inner(state_left: STATE, state_right: STATE) -> int:
        return 1 if state_left == state_right else 0
    
    @staticmethod
    def apply_operator_to_state(operator: OP | OP_FIXED, state: STATE,
                                *args, **kwargs) -> None | tuple[STATE, int]:
        return operator(state, *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_dense(self,
                                                  operator: OP | OP_FIXED,
                                                  qn: int,
                                                  *args, **kwargs) -> np.ndarray:
        return build_mat_rep_of_operator_dense(self.states_block,
                                               self.state_to_idx,
                                               operator,
                                               *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_sparse(self,
                                                   operator: OP | OP_FIXED,
                                                   qn: int,
                                                   *args, **kwargs) -> sp.csc_array:
        return build_mat_rep_of_operator_sparse(self.states_block,
                                                self.state_to_idx,
                                                operator,
                                                *args, **kwargs)


class BasisParity(Basis):
    def __init__(self, N: int):
        assert N > 0, N
        self.N = N
        self.states_block: dict[int, list[STATE]]
        self.state_to_idx: dict[int, dict[STATE, int]]
        self.states_block, self.state_to_idx = self.generate_basis()
        self.qns: set[int] = {-1, 1}
        self.dims: dict[int, int] = {-1: len(self.states_block[-1]),
                                     1: len(self.states_block[1])}
        self.id = ("parity", N)
    
    def generate_basis(self) -> tuple[dict[int, list[STATE]],
                                      dict[int, dict[STATE, int]]]:
        if self.N < 1:
            return
        
        states_block: dict[int, list[STATE]] = {parity: [] for parity in (-1, 1)}
        state_to_idx: dict[int, dict[STATE, int]] = {parity: {} for parity in (-1, 1)}
            
        for state in product((0, 1, -1, 2), repeat=self.N):
            parity = -2 * (sum(state) % 2) + 1 # even or odd number of electrons
            state_to_idx[parity][state] = len(states_block[parity])
            states_block[parity].append(state)
            
        return states_block, state_to_idx
    
    @staticmethod
    def inner(state_left: STATE, state_right: STATE) -> int:
        return 1 if state_left == state_right else 0
    
    @staticmethod
    def apply_operator_to_state(operator: OP | OP_FIXED, state: STATE,
                                *args, **kwargs) -> None | tuple[STATE, int]:
        return operator(state, *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_dense(self,
                                                  operator: OP | OP_FIXED,
                                                  qn: int,
                                                  *args, **kwargs) -> np.ndarray:
        return build_mat_rep_of_operator_dense(self.states_block[qn],
                                               self.state_to_idx[qn],
                                               operator,
                                               *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_sparse(self,
                                                   operator: OP | OP_FIXED,
                                                   qn: int,
                                                   *args, **kwargs) -> sp.csc_array:
        return build_mat_rep_of_operator_sparse(self.states_block[qn],
                                                self.state_to_idx[qn],
                                                operator,
                                                *args, **kwargs)


class BasisSZ(Basis):
    def __init__(self, N: int):
        assert N > 0, N
        self.N = N
        self.states_block: dict[int, list[STATE]]
        self.state_to_idx: dict[int, dict[STATE, int]]
        self.states_block, self.state_to_idx = self.generate_basis()
        self.qns: set[int] = set(self.states_block)
        self.dims: dict[int, int] = {qn: len(state_block)
                                     for qn, state_block in self.states_block.items()}
        self.id = ("sz", N)
    
    def generate_basis(self) -> tuple[dict[int, list[STATE]],
                                      dict[int, dict[STATE, int]]]:
        if self.N < 1:
            return
        
        states_block: dict[int, list[STATE]]\
            = {sz: [] for sz in range(-self.N, self.N + 1)}
        state_to_idx: dict[int, dict[STATE, int]]\
            = {sz: {} for sz in range(-self.N, self.N + 1)}
            
        for state in product((0, 1, -1, 2), repeat=self.N):
            sz = sum(state) - 2 * state.count(2)
            state_to_idx[sz][state] = len(states_block[sz])
            states_block[sz].append(state)
            
        return states_block, state_to_idx
    
    @staticmethod
    def inner(state_left: STATE, state_right: STATE) -> int:
        return 1 if state_left == state_right else 0
    
    @staticmethod
    def apply_operator_to_state(operator: OP | OP_FIXED, state: STATE,
                                *args, **kwargs) -> None | tuple[STATE, int]:
        return operator(state, *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_dense(self,
                                                  operator: OP | OP_FIXED,
                                                  qn: int,
                                                  *args, **kwargs) -> np.ndarray:
        return build_mat_rep_of_operator_dense(self.states_block[qn],
                                               self.state_to_idx[qn],
                                               operator,
                                               *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_sparse(self,
                                                   operator: OP | OP_FIXED,
                                                   qn: int,
                                                   *args, **kwargs) -> sp.csc_array:
        return build_mat_rep_of_operator_sparse(self.states_block[qn],
                                                self.state_to_idx[qn],
                                                operator,
                                                *args, **kwargs)


class BasisS2(Basis):
    def __init__(self, N: int):
        assert N > 0, N
        self.N = N
        self.states_block: dict[int, list[STATE_COMP]]
        self.state_to_idx: dict[int, dict[STATE, set[int]]]
        self.states_block, self.state_to_idx = self.generate_basis()
        self.qns: set[int] = set(self.states_block)
        self.dims: dict[int, int] = {qn: len(state_block)
                                     for qn, state_block in self.states_block.items()}
        self.id = ("s2", N)
    
    def _generate_spin_basis_sz(self, n: int) -> tuple[dict[int, list[STATE]],
                                                       dict[int, dict[STATE, int]]]:
        if n < 1:
            return
        basis_z: dict[int, list[STATE]] = {sz: [] for sz in range(n, -1, -2)}
        state_to_idx: dict[int, dict[STATE, int]] = {sz: {} for sz in range(n, -1, -2)}
        for state in product((1, -1), repeat=n):
            if (sz := sum(state)) >= 0:
                state_to_idx[sz][state] = len(basis_z[sz])
                basis_z[sz].append(state)
        return basis_z, state_to_idx
    
    def _generate_spin_basis_s2(self, n: int):
        if n < 1:
            return
        # s -> orthonormal basis with equal s_z, s^2 quantum numbers.
        basis_total: dict[int, np.ndarray] = {n: np.array([[1.]])}
        basis_minimal: dict[int, np.ndarray] = {n: np.array([[1.]])}
        basis_states_z, basis_state_to_idx = self._generate_spin_basis_sz(n)
        
        for s in range(n - 2, -1, -2):
            # Apply S_- to previously found states.
            # Find orthonormal basis for each s.
            basis_prev_minus = np.transpose([s_minus_composite(state_com,
                                                               basis_states_z[s + 2],
                                                               basis_state_to_idx[s])
                                             for state_com in basis_total[s + 2].T])
            
            states_to_orthogonalize = np.concatenate((basis_prev_minus,
                                                      np.eye(len(basis_states_z[s]))),
                                                     axis=1)
            orthonormal_basis = np.linalg.qr(states_to_orthogonalize)[0]
            orthonormal_basis *= np.sign(orthonormal_basis[0, 0])
            basis_total[s] = orthonormal_basis
            
            basis_minimal[s] = orthonormal_basis[:, len(basis_total[s + 2]):]
            
        return basis_total, basis_minimal, basis_states_z, basis_state_to_idx
        
    def generate_basis(self) -> tuple[dict[int, list[dict[tuple[int, ...], float]]],
                                                         dict[int, dict[tuple[int, ...], set[int]]]]:
        # How to decompose i spin 1/2 particles into eigenstates of total spin S^2
        s2_basis_info = {i: self._generate_spin_basis_s2(i) for i in range(2, self.N + 1)}
        # The output: s -> list of basis states: {s_z Fock representation: amplitude}
        #             s -> dict: S_Z basis state -> set with indices of S^2 basis states where it's used.
        states_block: dict[int, list[STATE_COMP]] = {s: [] for s in range(self.N + 1)}
        state_to_idx: dict[int, dict[STATE, set[int]]] = {s: {} for s in range(self.N + 1)}
        
        # Loop over all possible states with 0, 1, 2 electrons.
        for prod_state in product((0, 1, 2), repeat=self.N):
            # Single-paricle states with 1 electron are decomposed into eigenstates of S^2.
            if (num_doublets := prod_state.count(1)) > 1:
                doublet_idxs = tuple(idx for idx, sp_state in enumerate(prod_state) if sp_state == 1)
                s2_basis_coeffs, s2_basis_states = s2_basis_info[num_doublets][1:3]
                
                for s in range(num_doublets, -1, -2):
                    basis_coeffs = s2_basis_coeffs[s]
                    basis_states = s2_basis_states[s]
                    prod_basis_states = len(basis_states) * [list(prod_state)]
                    
                    # Replace the 1's in *prod_state* with appropriate linear
                    # combinations of spin up (+1) and spin down (-1) to form
                    # eigenstates of S^2.
                    for state_idx, basis_state in enumerate(basis_states):
                        for s2_idx, prod_state_to_replace_idx in enumerate(doublet_idxs):
                            prod_basis_states[state_idx][prod_state_to_replace_idx] = basis_state[s2_idx]
                        prod_basis_states[state_idx] = tuple(prod_basis_states[state_idx])
                        
                        # Add the indices of the S^2 states to the 'state-to-idxs' set.
                        num_previous_states = len(states_block[s])
                        num_states_to_add = basis_coeffs.shape[1]
                        state_to_idx[s].setdefault(prod_basis_states[state_idx], set()).update(
                            range(num_previous_states,
                                  num_previous_states + num_states_to_add
                                  )
                            )
                    for vec in basis_coeffs.T:
                        states_block[s].append({state: coeff for state, coeff in zip(prod_basis_states, vec)
                                                if abs(coeff) > 1e-15})
                        
            else: # already an eigenstate of S^2 when there's only 1 doublet in the product state.
                s = num_doublets # s = 0 or s = 1
                state_to_idx[s][prod_state] = {len(states_block[s])}
                states_block[s].append({prod_state: 1.})
                
        return states_block, state_to_idx
    
    @staticmethod
    def inner(state_left: STATE_COMP, state_right: STATE_COMP) -> float:
        return inner_comp(state_left, state_right)
    
    @staticmethod
    def apply_operator_to_state(operator: OP | OP_FIXED, state_comp: STATE_COMP,
                                *args, **kwargs) -> STATE_COMP:
        return apply_operator_to_state_comp(operator, state_comp, *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_dense(self,
                                                  operator: OP | OP_FIXED,
                                                  qn: int,
                                                  *args, **kwargs) -> np.ndarray:
        return build_mat_rep_of_operator_comp_dense(self.states_block[qn],
                                                    self.state_to_idx[qn],
                                                    operator,
                                                    *args, **kwargs)
    
    def build_mat_rep_of_operator_single_QN_sparse(self,
                                                   operator: OP | OP_FIXED,
                                                   qn: int,
                                                   *args, **kwargs) -> sp.csc_array:
        return build_mat_rep_of_operator_comp_sparse(self.states_block[qn],
                                                     self.state_to_idx[qn],
                                                     operator,
                                                     *args, **kwargs)
