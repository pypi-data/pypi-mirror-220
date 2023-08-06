# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 10:51:49 2023

@author: Emil
"""

import numpy as np
from numpy.typing import ArrayLike
from typing import Callable
from collections.abc import MutableSequence
from numbers import Number

from operators import NAME_TO_OP, HC_DICT


STATE = tuple[int, ...]
SITE = int | tuple[int, ...]
OP = Callable[[STATE, SITE], None | tuple[STATE, int | float]]
OP_FIXED = Callable[[STATE], None | tuple[STATE, int | float]]
HAM_PAR = Number | ArrayLike
HAM_TERM = (tuple[HAM_PAR, str, SITE] | tuple[str, SITE] | 
            tuple[HAM_PAR, str, SITE, str, SITE, ...] | tuple[str, SITE, str, SITE, ...])
TERM_ID = tuple[str, tuple[int, ...]]


class Term:
    def __init__(self, ham_term: HAM_TERM):
        self.coeff: HAM_PAR
        self.op_str: str
        self.sites: SITE
        self.op_func: OP_FIXED
        self.coeff, self.op_str, self.sites, self.op_func\
            = self._parse_ham_term(ham_term)
            
        self.id: TERM_ID = (self.op_str, self.sites)
        self.hc_id: TERM_ID = self._get_hc_id()
        
        self.shape: tuple[int, ...] = np.shape(self.coeff)
        self.is_complex: bool = np.iscomplexobj(self.coeff)
        self.is_zero: bool = np.allclose(self.coeff, 0, atol=1e-15)
        self.is_arr: bool = isinstance(self.coeff, np.ndarray)
        
    def __str__(self):
        coeff_str = "arr" if np.size(self.coeff) > 1 else str(self.coeff)
        return f"Term(coeff={coeff_str}, op_str={self.op_str}, sites={self.sites})"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def _parse_ham_term(ham_term: HAM_TERM):
        if isinstance(ham_term, Term):
            return ham_term.coeff, ham_term.op_str, ham_term.sites, ham_term.op_func
        ham_term = tuple(ham_term)
        if isinstance(ham_term[0], str):
            assert len(ham_term) % 2 == 0, ham_term
            coefficient = 1.
            names = ham_term[::2]
            sites = ham_term[1::2]
        else:
            assert len(ham_term) % 2 == 1, ham_term
            coefficient = ham_term[0]
            names = ham_term[1::2]
            sites = ham_term[2::2]
            
        if np.size(coefficient) > 1:
            coefficient = np.asarray(coefficient)
        else:
            coefficient = np.squeeze(coefficient).item()
            assert isinstance(coefficient, Number), coefficient
            
        # if not isinstance(coefficient, HAM_PAR):
        #     raise TypeError("Element 0 of the added term must be either "
        #                     f"a 'str' or '{HAM_PAR}'. Instead, '{ham_term[0]}' "
        #                     "was passed.")
        names = tuple(name.lower() for name in names)
        combined_name = '_'.join(names)
        combined_sites = flatten(sites)
        
        # Look for the full operator in the defined operator functions.
        # Otherwise, apply the operators consecutively as written in *ham_term*.
        try:
            op, num_sites = NAME_TO_OP[combined_name]
            assert len(combined_sites) == num_sites, (combined_name, combined_sites,
                                                      sites, num_sites)
            op_func = _fix_sites_in_op(op, combined_sites)
        except KeyError:
            ops, nums_sites = zip(*[NAME_TO_OP[name] for name in names])
            for sites_, num_sites in zip(sites, nums_sites):
                if num_sites > 1:
                    assert len(sites_) == num_sites, (sites_, num_sites)
            op_func = _apply_operators_consecutively(operators=ops, sites=sites)
        return coefficient, combined_name, combined_sites, op_func
    
    @staticmethod
    def _hermitian_conjugate_term_name(name: str) -> str:
        if name == "nup_ndn":
            return name
        components = name.split('_')
        return "_".join(HC_DICT[component] for component in components[::-1])

    def _get_hc_id(self) -> TERM_ID:
        return (self._hermitian_conjugate_term_name(self.id[0]), self.id[1][::-1])


def _fix_sites_in_op(operator: OP, sites) -> OP_FIXED:
    if len(sites) == 1:
        return lambda state: operator(state, sites[0])
    return lambda state: operator(state, sites)

def _apply_operators_consecutively(operators: tuple[OP, ...],
                                   sites: tuple[SITE, ...]) -> OP_FIXED:
    assert len(operators) == len(sites), (operators, sites)
    def combined_operator(state: STATE) -> None | tuple[STATE, int]:
        sign_out = 1
        for operator_intmd, site in zip(operators[::-1], sites[::-1]):
            tmp = operator_intmd(state, site)
            if tmp is None:
                return
            state, sign = tmp
            sign_out *= sign
        return state, sign_out
    return combined_operator

def flatten(data):
    if isinstance(data, (tuple, list)):
        if len(data) == 0:
            return ()
        else:
            return flatten(data[0]) + flatten(data[1:])
    else:
        return (data, )

def _is_complex_par(ham_par: HAM_PAR):
    return np.iscomplexobj(ham_par)

class OpSum(list):
    def __init__(self, terms: list[HAM_TERM | Term] | None = None):
        parsed_terms: list[Term] = [] if terms is None else [Term(term) for term in terms]
        self.has_complex_term = True if np.any([term.is_complex for term in parsed_terms]) else False
        self.parameter_shape: tuple[int, ...]\
            = np.broadcast_shapes(*(term.shape for term in parsed_terms))
        self.factored_terms: list[list[Term]] = self._factor_terms(parsed_terms)
        super().__init__(parsed_terms)

    def __setitem__(self, idx: int, term: HAM_TERM | Term):
        list.__setitem__(self, idx, self._before_insert(term))
    
    def __iadd__(self, term: HAM_TERM | Term):
        list.append(self, self._before_insert(term))
        return self
    
    def insert(self, idx: int, term: HAM_TERM | Term):
        list.insert(self, idx, self._before_insert(term))
    
    def append(self, other):
        self.__iadd__(other)

    def _before_insert(self, term: HAM_TERM | Term):
        parsed_term = Term(term)
        if parsed_term.is_complex == True:
            self.has_complex_term = True
        self.parameter_shape = np.broadcast_shapes(self.parameter_shape,
                                                   parsed_term.shape)
        self._factor_term(parsed_term, self.factored_terms)
        return parsed_term
    
    def _factor_terms(self, terms: list[Term]) -> list[list[Term]]:
        # Collect terms with the same coefficient. It is more efficient to add
        # the operators before they are multiplied by a coefficient.
        # e.g. c * A + c * B = c * (A + B) where c is a coeffcient and A, B are
        # matrix representations of some operators.
        factored_terms: list[list[Term]] = []
        for term in terms:
            self._factor_term(term, factored_terms)
        return factored_terms
    
    @staticmethod
    def _factor_term(term: Term, factored_terms: list[list[Term]]):
        # Look for the coefficient of 'term' in 'factored_terms' and append
        # 'term' to 'factored_terms'.
        for prev_terms in factored_terms:
            if term.shape == prev_terms[0].shape and np.all(term.coeff == prev_terms[0].coeff):
                prev_terms.append(term)
                break
        else:
            factored_terms.append([term])
        