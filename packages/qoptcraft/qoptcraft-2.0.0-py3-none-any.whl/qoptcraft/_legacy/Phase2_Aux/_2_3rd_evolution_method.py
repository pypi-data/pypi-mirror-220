"""Copyright 2021 Daniel Gómez Aguado

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

# ---------------------------------------------------------------------------------------------------------------------------
# 													LIBRARIES REQUIRED
# ---------------------------------------------------------------------------------------------------------------------------


# ----------TIME OF EXECUTION MEASUREMENT:----------

import time


# ----------MATHEMATICAL FUNCTIONS/MATRIX OPERATIONS:----------

# NumPy instalation: in the cmd: 'py -m pip install numpy'
import numpy as np

# SciPy instalation: in the cmd: 'py -m pip install scipy'
# from scipy.sparse import csc_matrix
# from scipy.sparse.linalg import expm
from scipy.linalg import expm

from ..mat_inner_product import *


# ----------FILE MANAGEMENT:----------

# File opening


# ----------COMBINATORY:----------

from ..recur_factorial import comb_evol


# ----------ALGORITHM 2: AUXILIAR FUNCTIONS:----------

from ._2_creation_and_destruction_operators import *

from ._2_logarithm_algorithms import *


# ---------------------------------------------------------------------------------------------------------------------------
# 										N-PHOTON OPTICAL SYSTEM EVOLUTION: THIRD METHOD
# ---------------------------------------------------------------------------------------------------------------------------


# Here, we will perform the third evolution of the system method's operations. Main function to inherit in other algorithms
def evolution_3(S, photons, vec_base, file_output=False, filename=False):
    # Initial time
    t = time.process_time_ns()

    # It is required to introduce photons_aux for 'photons_aux' and 'photons' not to "update" together
    global photons_aux
    global mult

    m = len(S)
    num_photons = int(np.sum(photons))

    # Resulting U matrix's dimensions:
    M = comb_evol(num_photons, m)
    # This value could also be obtained by measuring vec_base's length

    # Out of the three logarithm algorithms developed in the main algorithm 2b, logm_3()
    # has been the one used. It can be switched by logm_4/5(); the result will be similar
    iH_S = logm_3(S)[0]

    if file_output is True:
        # We save the vector basis
        iH_S_file = open(f"{filename}_iH_S.txt", "w")

        np.savetxt(iH_S_file, iH_S, delimiter=",")

        iH_S_file.close()

    iH_U = iH_U_operator(file_output, filename, iH_S, m, M, vec_base)

    # If the commentary of the following four lines is undone, the operator n will also be computed
    # and its conmutation with iH_U, which must exist, will be tested. It is by default omitted
    # for a faster pace

    """n_op=n_operator(m,M,vec_base)
	AperB=n_op.dot(iH_U)
	BperA=iH_U.dot(n_op)
	comparison(AperB,BperA,retrieve_name(AperB)[0],retrieve_name(BperA)[0])"""

    U = expm(iH_U)

    t_inc = time.process_time_ns() - t

    return U, t_inc


# Operator iH_U computation. It requires the use of the creation and annihilation operators.
# It can be expensive in computational terms, especially in comparison to the permament method
def iH_U_operator(file_output=False, filename=False, iH_S=False, m=False, M=False, vec_base=False):
    # iH_U initialization
    iH_U = np.zeros((M, M), dtype=complex)

    vec_base_canon = np.identity(M, dtype=complex)

    for p in range(M):
        # Array p to consider (u(m) basis)
        np.array(vec_base[p])

        # Array p to consider (u(M) basis)
        p_array_M = np.array(vec_base_canon[p])

        for q in range(M):
            # Array q to consider (u(m) basis). We must find
            # its equivalent in the u(M) basis after the operations
            np.array(vec_base[q])

            for j in range(m):
                for l in range(m):
                    # Array subject to the operators
                    q_array_aux = np.array(vec_base[q])

                    # Multiplier of (p,q)
                    mult = iH_S[j, l]

                    # We evaluate q_array_aux with the creation and annihilation
                    # operators, so we obtain a new vector, belonging to our basis
                    # (and a factor)
                    q_array_aux, mult = a(l, q_array_aux, mult)
                    q_array_aux, mult = a_dagger(j, q_array_aux, mult)

                    for k in range(M):
                        if (vec_base[k] == q_array_aux).all():
                            # We search within the vector basis u(m) in order
                            # to find the index corresponding to q_array_aux in the
                            # u(M) basis
                            index = k

                            break

                    # Array q to consider (u(M) basis)
                    q_array_M = np.array(vec_base_canon[index])

                    iH_U[p, q] += p_array_M.dot(q_array_M) * mult

    if file_output is True:
        # We save the vector basis
        iH_U_file = open(f"{filename}_iH_U.txt", "w")

        np.savetxt(iH_U_file, iH_U, delimiter=",")

        iH_U_file.close()

    return iH_U


# Operator n computation. Its use is optional. The function works similar to the iH_U operator one,
# but simpler: it only needs to search for diagonal elements and doesn't require iH_S
def n_operator(m, M, vec_base):
    n_operator = np.zeros((M, M), dtype=complex)

    vec_base_canon = np.identity(M, dtype=complex)

    for p in range(M):
        np.array(vec_base[p])

        p_array_M = np.array(vec_base_canon[p])

        for q in range(M):
            np.array(vec_base[q])

            for k in range(m):
                # Array subject to the operators
                q_array_aux = np.array(vec_base[q])

                mult = 1

                q_array_aux, mult = a(k, q_array_aux, mult)
                q_array_aux, mult = a_dagger(k, q_array_aux, mult)

                for l in range(M):
                    if (vec_base[l] == q_array_aux).all():
                        index = l

                        break

                q_array_M = np.array(vec_base_canon[index])

                n_operator[p, q] += p_array_M.dot(q_array_M) * mult

    return n_operator
