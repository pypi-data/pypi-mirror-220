# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 10:50:07 2023

@author: Emil
"""

import numpy as np
import scipy.sparse as sp
import warnings
from numpy.typing import ArrayLike
from numbers import Number

from operator_sum import OpSum, Term
from bases import Basis


OP_TERM_ID = tuple[str, tuple[int, ...]] # (*str_name*, *sites*)
OPR_TERM_ID = tuple[str, int, int, str, tuple[int, ...]] # (*basis.id*, *qn*, *str_name*, *sites*)


class OpRep:
    # Class responsible for writing the matrix representation of an operator
    # (given as an instance of *OpSum*) in a certain basis (given by an
    # instance of *Basis*).
    
    # Matrix representation of single operators in the given *basis* indexed by an ID.
    # This is accessible to all instances of this class as a quick look-up table.
    # These saved matrices are of type scipy.sparse.csc_array if sparse=True,
    # otherwise they are of type numpy.ndarray.
    _op_reps: dict[OPR_TERM_ID, np.ndarray | sp.csc_array] = {}
    
    def __init__(self, opsum: OpSum, basis: Basis,
                 qns_to_consider: list[int] | None = None,
                 sparse: bool | None = None):
        self.opsum = opsum
        self.basis = basis
        
        self.qns_to_consider: set[int] = self.basis.qns\
            if qns_to_consider is None else set(qns_to_consider)
        assert self.qns_to_consider.issubset(self.basis.qns), (
            "The given quantum numbers are not present in the given basis. "
            f"The quantum numbers of the basis are {self.basis.qns}, "
            f"while the given quantum numbers are {self.qns_to_consider}."
            )
        
        self.is_sparse = (True if self.basis.N > 5 else False) if sparse is None else bool(sparse)
        self._build_mat_rep_op\
            = self.basis.build_mat_rep_of_operator_single_QN_sparse if self.is_sparse\
                else self.basis.build_mat_rep_of_operator_single_QN_dense
        
        # matrix representation of *op* in the given *basis*, indexed by a quantum number.
        self.mat_rep = self._build_mat_rep_sparse() if self.is_sparse else self._build_mat_rep_dense()
    
    def _build_mat_rep_dense(self) -> dict[int, np.ndarray]:
        dtype = np.complex128 if self.opsum.has_complex_term else np.float64
        mat_rep: dict[int, np.ndarray] = {}
        for qn in self.qns_to_consider:
            mat_rep_qn = np.zeros(self.opsum.parameter_shape
                                  + 2 * (self.basis.dims[qn], ), dtype=dtype)
            for factored_term in self.opsum.factored_terms:
                if factored_term[0].is_zero:
                    continue
                mat_rep_qn_fac = np.zeros(2 * (self.basis.dims[qn], ), dtype=dtype)
                for term in factored_term:
                    mat_rep_qn_fac += self._get_mat_rep_of_operator_from_term_single_QN(term, qn)
                coeff = term.coeff[..., None, None] if term.is_arr else term.coeff
                mat_rep_qn += coeff * mat_rep_qn_fac
            mat_rep[qn] = mat_rep_qn
        return mat_rep
    
    def _build_mat_rep_sparse(self) -> dict[int, sp.csc_array]:
        mat_rep: dict[int, sp.csc_array] = {}
        dtype = np.complex128 if self.opsum.has_complex_term else np.float64
        for qn in self.qns_to_consider:
            # All coefficients of all terms are scalars.
            if not self.opsum.parameter_shape:
                mat_rep_qn = sp.csc_array(2 * (self.basis.dims[qn], ), dtype=dtype)
                for i, factored_term in enumerate(self.opsum.factored_terms):
                    print('factorized term: ', i, f'/ {len(self.opsum.factored_terms)}')
                    if factored_term[0].is_zero:
                        continue
                    mat_rep_qn_fac = sp.csc_array(2 * (self.basis.dims[qn], ), dtype=dtype)
                    for term in factored_term:
                        mat_rep_qn_fac += self._get_mat_rep_of_operator_from_term_single_QN(term, qn)
                    mat_rep_qn += term.coeff * mat_rep_qn_fac
            
            # Some coefficients are numpy arrays; do broadcasting.
            else:
                # Wrap scipy sparse arrays in numpy arrays to take care of broadcasting.
                mat_rep_qn = np.full(shape=self.opsum.parameter_shape,
                                      fill_value=sp.csc_array(2 * (self.basis.dims[qn], ), dtype=dtype),
                                      dtype=object)
                for factored_term in self.opsum.factored_terms:
                    if factored_term[0].is_zero:
                        continue
                    mat_rep_qn_fac = sp.csc_array(2 * (self.basis.dims[qn], ), dtype=dtype)
                    for term in factored_term:
                        mat_rep_qn_fac += self._get_mat_rep_of_operator_from_term_single_QN(term, qn)
                    if term.shape:
                        mat_rep_qn += term.coeff * np.full(shape=term.shape,
                                                           fill_value=mat_rep_qn_fac,
                                                           dtype=object)
                    else:
                        mat_rep_qn += np.array(term.coeff * mat_rep_qn_fac,
                                               dtype=object)

            mat_rep[qn] = mat_rep_qn
        return mat_rep
    
    def _get_mat_rep_of_operator_from_term_single_QN(self, term: Term, qn: int) -> np.ndarray:
        saved_op_reps = self.__class__._op_reps
        opr_term_id = self._get_opr_term_id(term, qn)
        if opr_term_id in saved_op_reps:
            return saved_op_reps[opr_term_id]
        opr_conj_term_id = self._get_opr_hc_term_id(term, qn)
        if opr_conj_term_id in saved_op_reps:
            if self.is_sparse:
                # Transposed sparse array will be of format "CSR". Convert to
                # "CSC" format and save it for later use.
                op_rep_trans = saved_op_reps[opr_conj_term_id].T.tocsc()
                saved_op_reps[opr_term_id] = op_rep_trans
                return op_rep_trans
            return saved_op_reps[opr_conj_term_id].T
        op_rep = self._build_mat_rep_op(term.op_func, qn)
        saved_op_reps[opr_term_id] = op_rep
        return op_rep
    
    def _get_mat_rep_of_operator_from_term_all_QNs(self, term: Term) -> dict[int, np.ndarray]:
        return {qn: self._get_mat_rep_of_operator_from_term_single_QN(term, qn)
                for qn in self.basis.qns}
    
    def _get_opr_term_id(self, term: Term, qn: int):
        return (*self.basis.id, qn, self.is_sparse, *term.id)
    
    def _get_opr_hc_term_id(self, term: Term, qn: int):
        return (*self.basis.id, qn, self.is_sparse, *term.hc_id)
    
    def clear_saved_matrix_elements(self):
        self.__class__._op_reps.clear()
        
    def diagonalize_single_qn(self,
                              qn: int,
                              k: int = 6,
                              return_eigenvectors: bool = False,
                              which: str = 'SA',
                              tol: float = 0,
                              **kwargs) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
        assert qn in self.mat_rep
        if self.is_sparse:
            if self.opsum.parameter_shape:
                energies = np.empty(shape=self.opsum.parameter_shape + (k, ),
                                    dtype=np.float64)
                eigenvectors = np.empty(shape=self.opsum.parameter_shape + (self.basis.dims[qn], k),
                                        dtype=np.complex128 if self.opsum.has_complex_term else np.float64)
                v0 = None if "v0" not in kwargs else kwargs.pop("v0")
                for idx, mat_rep in np.ndenumerate(self.mat_rep[qn]):
                    tmp = sp.linalg.eigsh(mat_rep,
                                          k=k,
                                          return_eigenvectors=True,
                                          which=which,
                                          v0=v0,
                                          tol=tol,
                                          **kwargs)
                    if return_eigenvectors:
                        energies[idx], eigenvectors[idx] = tmp
                    else:
                        energies[idx] = tmp[0]
                    v0 = tmp[1][:, 0]
                return (energies, eigenvectors) if return_eigenvectors else energies
            
            return sp.linalg.eigsh(self.mat_rep[qn],
                                   k=k,
                                   return_eigenvectors=return_eigenvectors,
                                   which=which,
                                   tol=tol,
                                   **kwargs)
        
        return np.linalg.eigh(self.mat_rep[qn]) if return_eigenvectors else np.linalg.eigvalsh(self.mat_rep[qn])
    
    def diagonalize_all_qns(self,
                            k: int | dict[int, int] = 6,
                            return_eigenvectors: bool = False,
                            which: str | dict[int, str] = 'SA',
                            tol: float | dict[int, float] = 0,
                            **kwargs)\
        -> dict[int, np.ndarray] | tuple[dict[int, np.ndarray], dict[int, np.ndarray]]:
        if return_eigenvectors:
            energies = {}
            eigenvectors = {}
            for qn in self.mat_rep:
                e, v = self.diagonalize_single_qn(qn=qn,
                                                  k=k,
                                                  return_eigenvectors=True,
                                                  which=which,
                                                  tol=tol,
                                                  **kwargs)
                energies[qn] = e
                eigenvectors[qn] = v
            return energies, eigenvectors
        return {qn: self.diagonalize_single_qn(qn=qn,
                                               k=k,
                                               return_eigenvectors=False,
                                               which=which,
                                               tol=tol,
                                               **kwargs)
                for qn in self.mat_rep}
    
def _parse_and_set_arg(kwargs_qns: dict[int, dict[str, ...]], arg, kw: str):
    if isinstance(arg, dict):
        kwargs_qns[kw] = arg
    else:
        pass
    
def operator_exp_val(op_rep: np.ndarray | sp.spmatrix | dict[int, np.ndarray | sp.spmatrix],
                     state_rep: np.ndarray | dict[int, np.ndarray],
                     axis: int | None = None,
                     prepend_dim_op_rep: bool = False,
                     append_dim_op_rep: bool = False,
                     op_rep_is_sparse: bool | None = None,
                     dtype: np.dtype | None = None,
                     weights: None | Number | ArrayLike = None)\
    -> float | complex | dict[int, np.ndarray | sp.spmatrix] | np.ndarray:
    # If 'op_rep' is in a sparse formulation, either it is a sparse array
    # with shape (N, N) or sparse arrays (shape (N, N)) wrapped in a numpy
    # array with arbitrary shape (m1, m2, ...) and 'object' dtype.
    #
    # If 'op_rep' is in a dense formulation, 'op_rep' is a numpy array with
    # shape (m1, m2, ..., N, N), i.e. "matrix axes" in the last two axes.
    # The dtype is not 'object' and usually np.complex128 or np.float64.
    
    # 'state_rep' is always a numpy array which must be broadcastable with
    # 'op_rep' after 'axis' has been removed from the shape of 'state_rep'
    # and the last two dimension of 'op_rep' has been removed.
    # The length of 'state_rep' in the 'axis' dimension must match 'op_rep'
    # in the last two dimensions, i.e. the length must be N.
    # If 'op_rep' has shape (N, N), the only requirement is that the shape 
    # of 'state_rep' matches 'op_rep' in the summation axis 'axis' (length N).
    # The output will have the same shape as the broadcasted shape of
    # 'op_rep' and 'state_rep' with the summation axis removed (m1, m2, ..., m_j).
    
    # Example: op_rep.shape=(m1, m2, ..., N, N) and
    #          state_rep.shape=(m1, m2, ..., N) with axis=-1 is valid.
    #          out.shape=(m1, m2, ...)
    
    # Example: op_rep.shape=(m1, m2, ..., mj, N, N) and
    #          state_rep.shape=(m1, m2, ..., m_{j-1}, N, m_j) with axis=-2 is valid.
    #          out.shape=(m1, m2, ..., m_j)
    
    # Example: op_rep.shape=(N, N) and
    #          state_rep.shape=(m1, m2, ..., m_{j-1}, N, m_j) with axis=-2 is valid.
    #          out.shape=(m1, m2, ..., m_j)
    
    # Example: op_rep.shape=(m1, m2, ..., N, N) and
    #          state_rep.shape=(N, ) with axis=0 or axis=-1 or axis=None is valid.
    #          out.shape=(m1, m2, ...)
    if isinstance(op_rep, dict) or isinstance(state_rep, dict):
        assert isinstance(op_rep, dict) and isinstance(state_rep, dict)
        common_keys = set(op_rep).intersection(state_rep)
        return {qn: operator_exp_val(op_rep[qn], state_rep[qn], axis, 
                                     prepend_dim_op_rep, append_dim_op_rep,
                                     op_rep_is_sparse, dtype, weights)
                for qn in common_keys}
    
    if state_rep.ndim > 1:
        if axis is None:
            raise ValueError("Please specify the summation axis 'axis' when "
                             "there is more than one dimension in 'state_rep'.")
    else:
        assert state_rep.ndim == 1, ("0d arrays are not allowed for 'state_rep'.")
        axis = 0
    axis = axis + state_rep.ndim if axis < 0 else axis
    assert 0 <= axis < state_rep.ndim, (axis, state_rep.ndim)
    
    dtype = state_rep.dtype if dtype is None else np.dtype(dtype)
        
    state_right = state_rep if weights is None else weights * state_rep
    
    if sp.issparse(op_rep):
        assert op_rep.shape[0] == op_rep.shape[1], op_rep.shape
        assert op_rep.shape[0] == state_rep.shape[axis], (op_rep.shape, state_rep.shape)
        if state_rep.ndim <= 2:
            # Slightly faster than using np.apply_along_axis since scipy
            # can handle matrix multiplication with 1D and 2D vectors
            state_to: np.ndarray = _apply_sparse_op(op_rep, state_right, axis)
            assert state_to.shape == state_rep.shape
        else:
            state_to = np.apply_along_axis(lambda state_rep: _apply_sparse_op(op_rep, state_rep, axis=0),
                                           axis=axis, arr=state_right)
        return np.einsum(_get_einsum_subscripts(state_to, axis),
                         state_rep.conj(), state_to)
    
    if op_rep_is_sparse is None:
        # Use the dtype of 'op_rep' to determine if its a sparse array
        # wrapped in a numpy array or simply a regular, dense numpy array if
        # not specified explicitly.
        op_rep_is_sparse = True if op_rep.dtype == np.dtype(object) else False
    
    if op_rep_is_sparse:
        if append_dim_op_rep:
            op_rep = op_rep[..., None]
        if prepend_dim_op_rep:
            op_rep = op_rep[None, ...]
            
        brc_shape = np.broadcast_shapes(op_rep.shape,
                                        state_rep.shape[:axis]
                                        + state_rep.shape[axis + 1:])
        # Put axis to sum at the end.
        out_shape = brc_shape + (state_rep.shape[axis], )
        assert op_rep.flat[0].shape[0] == op_rep.flat[0].shape[1]
        assert op_rep.flat[0].shape[0] == state_rep.shape[axis]
        state_to = np.empty(shape=out_shape, dtype=dtype)
        
        # op_rep_br, state_right_br = np.broadcast_arrays(op_rep, state_right)
        op_rep_brc = np.broadcast_to(op_rep, brc_shape)
        state_right_brc = np.broadcast_to(state_right,
                                          brc_shape[:axis]
                                          + state_rep.shape[axis:axis + 1]
                                          + brc_shape[axis:])
        state_right_brc = np.moveaxis(state_right_brc, axis, -1)
        for idx, op_rep_ in np.ndenumerate(op_rep_brc):
            # Do multiplication of 2D matrix and 1D vector in scipy.sparse
            state_to[idx] = op_rep_ @ state_right_brc[idx]
            
        str_left = _get_index_str(state_rep, axis)
        str_out = str_left.replace("n", "")
        str_right = str_out + "n"
        return np.einsum(f"{str_left}, {str_right} -> {str_out}",
                         state_rep.conj(), state_to)
    else:
        assert op_rep.ndim >= 2
        if append_dim_op_rep and op_rep.ndim > 2:
            op_rep = op_rep[..., None]
        if prepend_dim_op_rep and op_rep.ndim > 2:
            op_rep = op_rep[None, ...]
            
        # assert shapes of 'op_rep' and 'state_rep' match
        np.broadcast_shapes(op_rep.shape[:-2],
                            state_rep.shape[:axis] + state_rep.shape[axis + 1:])
        str_left = _get_index_str(state_rep, axis)
        str_right = str_left.replace("n", "m")
        str_out = str_left.replace("n", "")
        str_op = str_out + "nm" if op_rep.ndim > 2 else "nm"
        return np.einsum(f"{str_left}, {str_op}, {str_right} -> {str_out}",
                         state_rep.conj(), op_rep, state_right,
                         optimize='greedy')

def _apply_sparse_op(op_rep: sp.spmatrix,
                     state_rep: np.ndarray,
                     axis: int | None = None) -> np.ndarray:
    # op_rep @ state_rep.
    # sparse arrays handle matrix-vector multiplications when the vector
    # is 1-D or 2-D (summing over axis 0).
    assert sp.issparse(op_rep), type(op_rep)
    assert np.ndim(state_rep) in (1, 2), np.shape(state_rep)
    if state_rep.ndim == 1:
        return op_rep @ state_rep
    
    # state_rep.ndim == 2
    assert axis is not None
    if axis in (0, -2):
        return op_rep @ state_rep
    elif axis in (1, -1):
        return (op_rep @ state_rep.T).T
    raise ValueError("'axis' should be an int with value -2, -1, 0, or 1. "
                     f"Got {type(axis) = } with value {axis = }.")
    
def _thermal_avg_of_op_arr(op_rep: np.ndarray | sp.spmatrix | dict[int, np.ndarray | sp.spmatrix],
                           eig_rep: np.ndarray | dict[int, np.ndarray],
                           energies: np.ndarray | dict[int, np.ndarray],
                           temp: float | np.ndarray,
                           axis_mat: int,
                           axis_eig: int,
                           energy_zero: float | np.ndarray | None = None,
                           prepend_dim_op_rep: bool = False,
                           append_dim_op_rep: bool = False,
                           op_rep_is_sparse: bool | None = None,
                           dtype: np.dtype | None = None,
                           weights: np.ndarray | None = None) -> float | complex | np.ndarray:
    axis_mat = _pos_axis(axis_mat, eig_rep.ndim)
    axis_eig = _pos_axis(axis_eig, eig_rep.ndim)
    
    assert axis_mat != axis_eig
    axis_eig = axis_eig -1 if axis_mat < axis_eig else axis_eig
    
    op_rep_exp_val = operator_exp_val(op_rep, eig_rep, axis=axis_mat,
                                      prepend_dim_op_rep=prepend_dim_op_rep,
                                      append_dim_op_rep=append_dim_op_rep,
                                      op_rep_is_sparse=op_rep_is_sparse,
                                      dtype=dtype,
                                      weights=None)
    if weights is None:
        if energy_zero is None:
            energy_zero = np.mean(energies, axis=axis_eig, keepdims=True)
        weights = np.exp(-(energies - energy_zero) / temp)
        weights /= weights.sum(axis=axis_eig, keepdims=True)
    
    op_rep_exp_val_brc, weights_brc = np.broadcast_arrays(op_rep_exp_val, weights)
    
    str_exp = _get_index_str(op_rep_exp_val_brc, axis=axis_eig)
    str_w = str_exp
    str_out = str_exp.replace("n", "")
    return np.einsum(f"{str_w}, {str_exp} -> {str_out}",
                     weights_brc, op_rep_exp_val_brc)


def thermal_avg_of_op(op_rep: dict[int, np.ndarray | sp.spmatrix],
                      eig_rep: dict[int, np.ndarray],
                      energies: dict[int, np.ndarray],
                      temp: float | np.ndarray,
                      degeneracies: dict[int, int],
                      axis_mat: int,
                      axis_eig: int,
                      energy_zero: float | np.ndarray | None = None,
                      prepend_dim_op_rep: bool = False,
                      append_dim_op_rep: bool = False,
                      op_rep_is_sparse: bool | None = None,
                      dtype: np.dtype | None = None) -> float | complex | np.ndarray:
    assert (isinstance(op_rep, dict) and
            isinstance(eig_rep, dict) and
            isinstance(energies, dict) and
            isinstance(degeneracies, dict)), (type(op_rep), type(eig_rep), type(energies), type(degeneracies))
    common_keys = set(op_rep).intersection(eig_rep, energies, degeneracies)
    
    if (len(common_keys) != len(op_rep) or
        len(common_keys) != len(eig_rep) or
        len(common_keys) != len(energies) or
        len(common_keys) != len(degeneracies)):
        warnings.warn("The keys (usually quantum numbers) of 'op_rep', "
                      "'gs_rep', 'energies', and 'degeneracies' do not match; "
                      "the thermal average only considers the shared keys: "
                      f"{common_keys}.")
            
    axis_mat = _pos_axis(axis_mat, eig_rep[0].ndim)
    axis_eig = _pos_axis(axis_eig, eig_rep[0].ndim)
    assert axis_mat != axis_eig
    axis_eig_energies = axis_eig - 1 if axis_mat < axis_eig else axis_eig
    
    # Use the mean of all energies across different quantum numbers and eigenvalue idx.
    energy_zero = np.mean([np.mean(e,
                                   axis=axis_eig_energies,
                                   keepdims=True)
                           for e in energies.values()], axis=0)\
        if energy_zero is None else energy_zero
            
    # Boltzmann factors
    weights = {qn: degeneracies[qn] * np.exp(-(energies[qn] - energy_zero) / temp)
               for qn in common_keys}
    
    z = np.sum([w.sum(axis=axis_eig_energies, keepdims=True)
                for w in weights.values()],
               axis=0)
    
    for w in weights.values():
        w /= z
        
    return np.sum([_thermal_avg_of_op_arr(op_rep[qn], eig_rep[qn], energies[qn],
                                          temp, axis_mat, axis_eig,
                                          energy_zero, prepend_dim_op_rep,
                                          append_dim_op_rep,
                                          op_rep_is_sparse, dtype, weights[qn])
                   for qn in common_keys],
                  axis=0)
    
    

def _get_index_str(state_rep: np.ndarray, axis: int) -> str:
    indices = "abcdefghijkl"
    axis = axis + state_rep.ndim if axis < 0 else axis
    assert 0 <= axis < state_rep.ndim, (axis, state_rep.ndim)
    state_str = indices[:axis] + "n" + indices[axis + 1: state_rep.ndim]
    return state_str


def _get_einsum_subscripts(state_rep: np.ndarray, axis: int):
    state_str = _get_index_str(state_rep, axis)
    return f"{state_str}, {state_str} -> {state_str.replace('n', '')}"

def _broadcast_and_sum(arrays: list[np.ndarray], sum_axis: int, **kwargs):
    arrays_brc = np.broadcast_arrays(*arrays)
    arr_indices = _get_index_str(arrays_brc[0], sum_axis)
    lhs = ', '.join(len(arrays) * [arr_indices])
    rhs = arr_indices.replace('n', '')
    return np.einsum(f'{lhs} -> {rhs}', *arrays_brc, **kwargs)
    

def _pos_axis(axis: int, ndim: int):
    axis_pos = axis + ndim if axis < 0 else axis
    assert 0 <= axis < ndim, (axis, ndim)
    return axis_pos


# TODO: write function which extracts the ground state across different quantum numbers
# def extract_gs(energies: dict[int, np.ndarray],
#                eigs: dict[int, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
#     E_gs_candidates = [E[..., 0] for E in energies.values()]
#     qn_gs = np.take(list(energies.keys()), np.argmin(E_gs_candidates, axis=0))
#     E_gs = np.min(E_gs_candidates, axis=0)
#     gs = np.array([eigs[qn][i, :, 0] for i, qn in enumerate(qn_gs)], dtype=object)
#     return E_gs, gs, qn_gs
