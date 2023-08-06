# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 10:46:40 2023

@author: Emil
"""

from collections.abc import Callable


STATE = tuple[int, ...]
SITE = int | tuple[int, ...]
OP = Callable[[STATE, SITE], None | tuple[STATE, int | float]]

def _c_dag_up_c_up(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c^dag_{i, up} c_{j, up}
    i, j = ij
    if i == j:
        return (state, 1) if (state[i] in (1, 2)) else None
    if state[i] in (1, 2) or state[j] in (0, -1):
        return
    state_out = list(state)
    state_out[i] = 1 if state[i] == 0 else 2 # 0 -> 1, -1 -> 2
    state_out[j] = 0 if state[j] == 1 else -1 # 1 -> 0, 2 -> -1
    sign = (1 if sum(state[i:j]) % 2 == 0 else -1) if j > i\
        else (1 if (sum(state[j:i]) + 1) % 2 == 0 else -1)
    return tuple(state_out), sign

def _c_up_c_dag_up(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c_{i, up} c^dag_{j, up}
    if (tmp := _c_dag_up_c_up(state, ij[::-1])) is not None:
        return tmp[0], -tmp[1]

def _c_dag_down_c_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c^dag_{i, down} c_{j, down}
    i, j = ij
    if i == j:
        return (state, 1) if (state[i] in (-1, 2)) else None
    if state[i] in (-1, 2) or state[j] in (0, 1):
        return
    state_out = list(state)
    state_out[i] = -1 if state[i] == 0 else 2
    state_out[j] = 0 if state[j] == -1 else 1
    sign = (1 if sum(state[i:j]) % 2 == 0 else -1) if j > i\
        else (1 if (sum(state[j:i]) + 1) % 2 == 0 else -1)
    if state[i] == 1:
        sign *= -1
    if state[j] == 2:
        sign *= -1
    return tuple(state_out), sign

def _c_down_c_dag_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    #  c_{i, down} c^dag_{j, down}
    if (tmp := _c_dag_down_c_down(state, ij[::-1])) is not None:
        return tmp[0], -tmp[1]

def _c_dag_up_c_dag_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c^dag_{i, up} c^dag_{j, down}
    i, j = ij
    if i == j:
        if state[i] != 0:
            return
        state_out = list(state)
        state_out[i] = 2
        return tuple(state_out), 1
    if state[i] in (1, 2) or state[j] in (-1, 2):
        return
    state_out = list(state)
    state_out[i] = 1 if state[i] == 0 else 2
    state_out[j] = -1 if state[j] == 0 else 2
    sign = (1 if sum(state[i:j]) % 2 == 0 else -1) if j > i\
        else (1 if (sum(state[j:i]) + 1) % 2 == 0 else -1)
    if state[j] == 1:
        sign *= -1
    return tuple(state_out), sign

def _c_dag_down_c_dag_up(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c^dag_{i, down} c^dag_{j, up}
    if (tmp := _c_dag_up_c_dag_down(state, ij[::-1])) is not None:
        return tmp[0], -tmp[1]

def _c_down_c_up(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c_{i, down} c_{j, up}
    i, j = ij
    if i == j:
        if state[i] != 2:
            return
        state_out = list(state)
        state_out[i] = 0
        return tuple(state_out), 1
    if state[i] in (1, 0) or state[j] in (-1, 0):
        return
    state_out = list(state)
    state_out[i] = 1 if state[i] == 2 else 0
    state_out[j] = -1 if state[j] == 2 else 0
    sign = (1 if sum(state[i:j]) % 2 == 0 else -1) if j > i\
        else (1 if (sum(state[j:i]) + 1) % 2 == 0 else -1)
    if state[i] == 2:
        sign *= -1
    return tuple(state_out), sign

def _c_up_c_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c_{i, up} c_{j, down}
    if (tmp := _c_down_c_up(state, ij[::-1])) is not None:
        return tmp[0], -tmp[1]

def _c_dag_up_c_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c^dag_{i, up} c_{j, down}
    i, j = ij
    if i == j:
        if state[i] != -1:
            return
        state_out = list(state)
        state_out[i] = 1
        return tuple(state_out), 1
    if state[i] in (1, 2) or state[j] in (1, 0):
        return
    state_out = list(state)
    state_out[i] = 1 if state[i] == 0 else 2 # 0 -> 1, -1 -> 2
    state_out[j] = 1 if state[j] == 2 else 0 # 2 -> 1, -1 -> 0
    sign = (1 if sum(state[i:j]) % 2 == 0 else -1) if j > i\
        else (1 if (sum(state[j:i]) + 1) % 2 == 0 else -1)
    if state[j] == 2:
        sign *= -1
    return tuple(state_out), sign

def _c_down_c_dag_up(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c_{i, down} c^dag_{j, up}
    if (tmp := _c_dag_up_c_down(state, ij[::-1])) is not None:
        return tmp[0], -tmp[1]

def _c_dag_down_c_up(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c^dag_{i, down} c_{j, up}
    i, j = ij
    if i == j:
        if state[i] != 1:
            return
        state_out = list(state)
        state_out[i] = -1
        return tuple(state_out), 1
    if state[i] in (-1, 2) or state[j] in (-1, 0):
        return
    state_out = list(state)
    state_out[i] = -1 if state[i] == 0 else 2 # 0 -> -1, 1 -> 2
    state_out[j] = -1 if state[j] == 2 else 0 # 2 -> -1, 1 -> 0
    sign = (1 if sum(state[i:j]) % 2 == 0 else -1) if j > i\
        else (1 if (sum(state[j:i]) + 1) % 2 == 0 else -1)
    if state[i] == 1:
        sign *= -1
    return tuple(state_out), sign

def _c_up_c_dag_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    # c_{i, up} c^dag_{j, down}    
    if (tmp := _c_dag_down_c_up(state, ij[::-1])) is not None:
        return tmp[0], -tmp[1]
    
def _n(state: STATE, i: int) -> None | tuple[STATE, int]:
    # n_{i, up} + n_{i, down}
    if state[i] == 0:
        return
    elif state[i] == 2:
        return state, 2
    else:
        return state, 1
    
def _n_up(state: STATE, i: int) -> None | tuple[STATE, int]:
    return _c_dag_up_c_up(state, i, i)

def _n_down(state: STATE, i: int) -> None | tuple[STATE, int]:
    return _c_dag_down_c_down(state, i, i)

def _n_up_n_down(state: STATE, ij: tuple[int, int]) -> None | tuple[STATE, int]:
    i, j = ij
    if i == j:
        return (state, 1) if state[i] == 2 else None
    if state[i] in (-1, 0) or state[j] in (1, 0):
        return
    return state, 1

def _c_up(state: STATE, i: int) -> None | tuple[STATE, int]:
    if state[i] in (-1, 0):
        return
    state_out = list(state)
    state_out[i] = 0 if state[i] == 1 else -1 # 1 -> 0, 2 -> -1
    sign = 1 if (sum(state[:i]) % 2 == 0) else -1
    return tuple(state_out), sign

def _c_down(state: STATE, i: int) -> None | tuple[STATE, int]:
    if state[i] in (1, 0):
        return
    state_out = list(state)
    state_out[i] = 0 if state[i] == -1 else 1 # -1 -> 0, 2 -> 1
    sign = 1 if (sum(state[:i]) % 2 == 0) else -1
    if state[i] == 2:
        sign *= -1
    return tuple(state_out), sign

def _c_dag_up(state: STATE, i: int) -> None | tuple[STATE, int]:
    if state[i] in (1, 2):
        return
    state_out = list(state)
    state_out[i] = 1 if state[i] == 0 else 2 # 0 -> 1, -1 -> 2
    sign = 1 if (sum(state[:i]) % 2 == 0) else -1
    return tuple(state_out), sign

def _c_dag_down(state: STATE, i: int) -> None | tuple[STATE, int]:
    if state[i] in (-1, 2):
        return
    state_out = list(state)
    state_out[i] = -1 if state[i] == 0 else 2 # 0 -> -1, 1 -> 2
    sign = 1 if (sum(state[:i]) % 2 == 0) else -1
    if state[i] == 1:
        sign *= -1
    return tuple(state_out), sign

def _s_z(state: STATE, i: int) -> None | tuple[STATE, float]:
    if state[i] in (0, 2):
        return None
    return (state, 0.5) if state[i] == 1 else (state, -0.5)


# str name to (func, num of args beyond *state*)
NAME_TO_OP: dict[str, tuple[OP, int]] = {"cdagup_cup": (_c_dag_up_c_up, 2),
                                         "cdagdn_cdn": (_c_dag_down_c_down, 2),
                                         "cdagup_cdagdn": (_c_dag_up_c_dag_down, 2),
                                         "cdn_cup": (_c_down_c_up, 2),
                                         "cdagup_cdn": (_c_dag_up_c_down, 2),
                                         "cdagdn_cup": (_c_dag_down_c_up, 2),
                                         "ntot": (_n, 1),
                                         "nup": (_n_up, 1),
                                         "ndn": (_n_down, 1),
                                         "nup_ndn": (_n_up_n_down, 2),
                                         "ndn_nup": (_n_up_n_down, 2),
                                         "sz": (_s_z, 1),
                                         "cup": (_c_up, 1),
                                         "cdn": (_c_down, 1),
                                         "cdagup": (_c_dag_up, 1),
                                         "cdagdn": (_c_dag_down, 1),
                                         
                                         "cup_cdagup": (_c_up_c_dag_up, 2),
                                         "cdn_cdagdn": (_c_down_c_dag_down, 2),
                                         "cdagdn_cdagup": (_c_dag_down_c_dag_up, 2),
                                         "cup_cdn": (_c_up_c_down, 2),
                                         "cdn_cdagup": (_c_down_c_dag_up, 2),
                                         "cup_cdagdn": (_c_up_c_dag_down, 2)}
# hermitian conjugate operator
HC_DICT = {"ntot": "ntot",
           "nup": "nup",
           "ndn": "ndn",
           "sz": "sz",
           "cup": "cdagup",
           "cdn": "cdagdn",
           "cdagup": "cup",
           "cdagdn": "cdn"}
