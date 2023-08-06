# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:54:41 2023

@author: Emil
"""

import numpy as np
from numpy.typing import ArrayLike
from numbers import Number
from collections.abc import Sequence, Iterable

from operator_sum import OpSum


HAM_PAR = Number | ArrayLike

def build_ham_op_sum_S_D(epsilon_d: HAM_PAR,
                         U: HAM_PAR,
                         Gamma: HAM_PAR,
                         Delta: HAM_PAR,
                         gamma: Sequence[float],
                         xi: Sequence[float]):
    h_op = OpSum()
    add_dot_to_ham_op_sum(h_op, epsilon_d, U, site_dot=0)
    add_sc_to_ham_op_sum(h_op, Gamma, Delta, gamma, xi,
                         sites_sc=range(1, len(xi) + 1), site_dot=0)
    return h_op

def build_ham_op_sum_SN_D(epsilon_d: HAM_PAR,
                          U: HAM_PAR,
                          Gammas: Sequence[HAM_PAR],
                          Deltas: Sequence[HAM_PAR],
                          gamma: Sequence[float],
                          xi: Sequence[float]):
    h_op = OpSum()
    add_dot_to_ham_op_sum(h_op, epsilon_d, U, site_dot=0)
    
    if len(Gammas) != len(Deltas):
        raise ValueError("'Gammas' and 'Deltas' must have the same length "
                         "(equal to the number of superconductors).")
    L = len(xi)
    for i, (Gamma, Delta) in enumerate(zip(Gammas, Deltas)):
        add_sc_to_ham_op_sum(h_op, Gamma, Delta, gamma, xi,
                             sites_sc=range(1 + i * L, 1 + (i + 1) * L),
                             site_dot=0)
    return h_op

def add_dot_to_ham_op_sum(h_op: OpSum, epsilon_d: HAM_PAR, U: HAM_PAR,
                          site_dot: int) -> OpSum:
    h_op += (epsilon_d, "ntot", site_dot)
    h_op += (U, "nup_ndn", (site_dot, site_dot))
    return h_op
    
def add_sc_to_ham_op_sum(h_op: OpSum, Gamma: HAM_PAR, Delta: HAM_PAR,
                         gamma: Sequence[float], xi: Sequence[float],
                         sites_sc: Iterable[int], site_dot: int) -> OpSum:
    if len(gamma) != len(xi):
        raise ValueError("There must be the same number of parameters for the "
                         "superconductor, i.e. 'gamma' and 'xi' must have the "
                         "same length (equal to the number of desired levels "
                         "in the superconductor).")
        
    for site_sc, xi_l, gamma_l in zip(sites_sc, xi, gamma):
        h_op += (-Delta, "cdagup_cdagdn", (site_sc, site_sc))
        h_op += (-Delta.conjugate(), "cdn_cup", (site_sc, site_sc))
        
        h_op += (xi_l, "ntot", site_sc)
        
        t = np.sqrt(gamma_l * Gamma)
        h_op += (t, "cdagup_cup", (site_sc, site_dot))
        h_op += (t, "cdagdn_cdn", (site_sc, site_dot))
        h_op += (t, "cdagup_cup", (site_dot, site_sc))
        h_op += (t, "cdagdn_cdn", (site_dot, site_sc))
    
    return h_op
