# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>

import unittest
from unittest import TestCase

import jax.numpy as jnp
import numpy as np

from pyhgf import load_data
from pyhgf.model import HGF
from pyhgf.response import total_gaussian_surprise


class Testmodel(TestCase):
    def test_HGF(self):
        """Test the model class"""

        ##############
        # Continuous #
        ##############
        timeserie = load_data("continuous")

        # two-level
        # ---------
        two_level_continuous_hgf = HGF(
            n_levels=2,
            model_type="continuous",
            initial_mu={"1": timeserie[0], "2": 0.0},
            initial_pi={"1": 1e4, "2": 1e1},
            omega={"1": -3.0, "2": -3.0},
            rho={"1": 0.0, "2": 0.0},
            kappas={"1": 1.0},
        )

        two_level_continuous_hgf.input_data(input_data=timeserie)

        surprise = (
            two_level_continuous_hgf.surprise()
        )  # Sum the surprise for this model
        assert jnp.isclose(surprise, -676.51306)
        assert len(two_level_continuous_hgf.node_trajectories[1]["mu"]) == 614

        # three-level
        # -----------
        three_level_continuous_hgf = HGF(
            n_levels=3,
            model_type="continuous",
            initial_mu={"1": 1.04, "2": 1.0, "3": 1.0},
            initial_pi={"1": 1e4, "2": 1e1, "3": 1e1},
            omega={"1": -13.0, "2": -2.0, "3": -2.0},
            rho={"1": 0.0, "2": 0.0, "3": 0.0},
            kappas={"1": 1.0, "2": 1.0},
        )
        three_level_continuous_hgf.input_data(input_data=timeserie)
        surprise = three_level_continuous_hgf.surprise()
        assert jnp.isclose(surprise, -394.20514)

        # test an alternative response function
        sp = total_gaussian_surprise(three_level_continuous_hgf)
        assert jnp.isclose(sp, 1646.3826)

        ##########
        # Binary #
        ##########
        timeseries = load_data("binary")

        # two-level
        # ---------
        two_level_binary_hgf = HGF(
            n_levels=2,
            model_type="binary",
            initial_mu={"1": 0.0, "2": 0.5},
            initial_pi={"1": 0.0, "2": 1e4},
            omega={"1": None, "2": -6.0},
            rho={"1": None, "2": 0.0},
            kappas={"1": None},
            eta0=0.0,
            eta1=1.0,
            pihat=jnp.inf,
        )

        # Provide new observations
        two_level_binary_hgf = two_level_binary_hgf.input_data(timeseries)
        surprise = two_level_binary_hgf.surprise()
        assert jnp.isclose(surprise, 215.58821)

        # three-level
        # -----------
        three_level_binary_hgf = HGF(
            n_levels=3,
            model_type="binary",
            initial_mu={"1": 0.0, "2": 0.5, "3": 0.0},
            initial_pi={"1": 0.0, "2": 1e4, "3": 1e1},
            omega={"1": None, "2": -6.0, "3": -2.0},
            rho={"1": None, "2": 0.0, "3": 0.0},
            kappas={"1": None, "2": 1.0},
            eta0=0.0,
            eta1=1.0,
            pihat=jnp.inf,
        )
        three_level_binary_hgf.input_data(input_data=timeseries)
        surprise = three_level_binary_hgf.surprise()
        assert jnp.isclose(surprise, 215.59067)

        ############################
        # dynamic update sequences #
        ############################

        three_level_binary_hgf = HGF(
            n_levels=3,
            model_type="binary",
            initial_mu={"1": 0.0, "2": 0.5, "3": 0.0},
            initial_pi={"1": 0.0, "2": 1e4, "3": 1e1},
            omega={"1": None, "2": -6.0, "3": -2.0},
            rho={"1": None, "2": 0.0, "3": 0.0},
            kappas={"1": None, "2": 1.0},
            eta0=0.0,
            eta1=1.0,
            pihat=jnp.inf,
        )

        # create a custom update series
        update_sequence1 = three_level_binary_hgf.get_update_sequence()
        update_sequence2 = update_sequence1[:2]
        update_branches = (update_sequence1, update_sequence2)
        branches_idx = np.random.binomial(n=1, p=0.5, size=len(timeseries))

        three_level_binary_hgf.input_custom_sequence(
            update_branches=update_branches,
            branches_idx=branches_idx,
            input_data=timeseries,
        )


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
