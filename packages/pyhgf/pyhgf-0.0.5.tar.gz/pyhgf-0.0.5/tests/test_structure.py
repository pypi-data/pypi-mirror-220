# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>

import unittest
from unittest import TestCase

import jax.numpy as jnp

from pyhgf.continuous import continuous_input_update, continuous_node_update
from pyhgf.structure import beliefs_propagation, list_branches, trim_sequence
from pyhgf.typing import Indexes


class TestStructure(TestCase):
    def test_beliefs_propagation(self):
        """Test the loop_inputs function"""

        ###############################################
        # one value parent with one volatility parent #
        ###############################################
        input_node_parameters = {
            "omega": 1.0,
            "kappas": None,
            "psis": None,
            "surprise": 0.0,
            "time_step": 0.0,
            "value": 0.0,
        }
        node_parameters = {
            "pihat": 1.0,
            "pi": 1.0,
            "muhat": 1.0,
            "kappas": (1.0,),
            "mu": 1.0,
            "nu": 1.0,
            "psis": (1.0,),
            "omega": 1.0,
            "rho": 1.0,
        }

        node_structure = (
            Indexes((1,), None, None, None),
            Indexes(None, (2,), (0,), None),
            Indexes(None, None, None, (1,)),
        )
        parameters_structure = (
            input_node_parameters,
            node_parameters,
            node_parameters,
        )

        # create update sequence
        sequence1 = 0, continuous_input_update
        sequence2 = 1, continuous_node_update
        update_sequence = (sequence1, sequence2)

        # one batch of new observations with time step
        data = jnp.array([0.2, 1.0])

        # apply sequence
        new_parameters_structure, _ = beliefs_propagation(
            parameters_structure=parameters_structure,
            data=data,
            update_sequence=update_sequence,
            node_structure=node_structure,
        )

        assert new_parameters_structure[1]["mu"] == 0.6405112
        assert new_parameters_structure[2]["pi"] == 0.50698835

    def test_find_branch(self):
        """Test the find_branch function"""
        node_structure = (
            Indexes((1,), None, None, None),
            Indexes(None, (2,), (0,), None),
            Indexes(None, None, None, (1,)),
            Indexes((4,), None, None, None),
            Indexes(None, None, (3,), None),
        )
        branch_list = list_branches([0], node_structure, branch_list=[])
        assert branch_list == [0, 1, 2]

    def test_trim_sequence(self):
        """Test the trim_sequence function"""
        node_structure = (
            Indexes((1,), None, None, None),
            Indexes(None, (2,), (0,), None),
            Indexes(None, None, None, (1,)),
            Indexes((4,), None, None, None),
            Indexes(None, None, (3,), None),
        )
        update_sequence = (
            (0, continuous_input_update),
            (1, continuous_node_update),
            (2, continuous_node_update),
            (3, continuous_node_update),
            (4, continuous_node_update),
        )
        new_sequence = trim_sequence(
            exclude_node_idxs=[0],
            update_sequence=update_sequence,
            node_structure=node_structure,
        )
        assert len(new_sequence) == 2
        assert new_sequence[0][0] == 3
        assert new_sequence[1][0] == 4


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
