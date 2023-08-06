# FermPy
A Python package for exactly solving low-dimensional fermionic Hamiltonians. It was developed with the intention of constructing and diagonalizing matrix representations of low-dimensional, interacting fermionic Hamiltonians, in particular effective (surrogate) models that describe the low-energy (sub-gap) physics of the superconducting Anderson impurity model (see the [arXiv preprint](https://arxiv.org/)).

FermPy is based on [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/). Small systems use *dense* NumPy arrays as operator representations while large systems employ *sparse* Scipy arrays.

Functionality of this package includes:
- Construction of matrix representations of operators (*H*, *S<sub>z</sub>*, etc.) from a basis (chosen from symmetry considerations)
- Diagonalization (*numpy.linalg.eigh*, *scipy.sparse.linalg.eigh*) of operators
- Calculating expectation values and thermal averages of operators