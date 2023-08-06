#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021-2023 Hao Zhang<zh970205@mail.ustc.edu.cn>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import TAT
import tetragono as tet


def abstract_state(L1, L2, t, U, mu, side=1):
    """
    Create density matrix of Hubbard model state.

    Parameters
    ----------
    L1, L2 : int
        The lattice size.
    t, U : float
        Hubbard model parameters.
    mu : float
        The chemical potential.
    side : 1 | 2, default=1
        The Hamiltonian should apply to single side or both side of density matrix.
    """
    if side not in [1, 2]:
        raise RuntimeError("side should be either 1 or 2")
    state = tet.AbstractState(TAT.Fermi.D.Tensor, L1, L2)
    state.total_symmetry = 0
    for l1 in range(L1):
        for l2 in range(L2):
            state.physics_edges[(l1, l2, 0)] = [(0, 1), (+1, 2), (+2, 1)]
            state.physics_edges[(l1, l2, 1)] = [(0, 1), (-1, 2), (-2, 1)]
    NN = tet.common_tensor.Fermi_Hubbard.NN.to(float)
    N0 = tet.common_tensor.Fermi_Hubbard.N0.to(float)
    N1 = tet.common_tensor.Fermi_Hubbard.N1.to(float)
    CSCS = tet.common_tensor.Fermi_Hubbard.CSCS.to(float)
    single_site = U * NN - mu * (N0 + N1)
    tCC = -t * CSCS
    for layer in range(side):
        # Hamiltonian for the second layer should be transposed
        # (transpose but not conjugate, or conjugate but not transpose),
        # But the hamiltonian is real, so nothing to do here
        for l1 in range(L1):
            for l2 in range(L2):
                state.hamiltonians[(l1, l2, layer),] = single_site
                if l1 != 0:
                    state.hamiltonians[(l1 - 1, l2, layer), (l1, l2, layer)] = tCC
                if l2 != 0:
                    state.hamiltonians[(l1, l2 - 1, layer), (l1, l2, layer)] = tCC
    return state


def abstract_lattice(L1, L2, t, U, mu, side=1):
    """
    Create density matrix of Hubbard model lattice.

    Parameters
    ----------
    L1, L2 : int
        The lattice size.
    t, U : float
        Hubbard model parameters.
    mu : float
        The chemical potential.
    side : 1 | 2, default=1
        The Hamiltonian should apply to single side or both side of density matrix.
    """
    state = tet.AbstractLattice(abstract_state(L1, L2, t, U, mu, side=side))
    state.virtual_bond["R"] = state.virtual_bond["D"] = [(0, 1)]
    return state
