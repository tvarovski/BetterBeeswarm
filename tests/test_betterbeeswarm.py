import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import betterbeeswarm
from betterbeeswarm.betterbeeswarm import Beeswarm


class BetterBeeswarmTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_import_monkeypatches_seaborn(self):
        self.assertIs(sns.categorical.Beeswarm, betterbeeswarm.Beeswarm)
        self.assertIs(sns.swarmplot, betterbeeswarm.swarmplot)

    def test_invalid_overflow_value_raises(self):
        with self.assertRaises(ValueError):
            Beeswarm(overflow="bad-value")

    def test_add_gutters_clamps_points(self):
        beeswarm = Beeswarm(overflow="gutters", width=0.8)
        points = np.array([-1.0, 0.0, 1.0])
        beeswarm.add_gutters(points, center=0.0, trans_fwd=lambda x: x, trans_inv=lambda x: x)
        self.assertTrue(np.all(points >= -0.4))
        self.assertTrue(np.all(points <= 0.4))
        self.assertTrue(beeswarm.gutters)

    def test_random_mode_is_reproducible_with_seed(self):
        p1 = np.array([-1.0, 0.0, 1.0])
        p2 = np.array([-1.0, 0.0, 1.0])

        b1 = Beeswarm(overflow="random", width=0.8, random_state=42)
        b2 = Beeswarm(overflow="random", width=0.8, random_state=42)

        b1.add_randomly(p1, center=0.0, trans_fwd=lambda x: x, trans_inv=lambda x: x)
        b2.add_randomly(p2, center=0.0, trans_fwd=lambda x: x, trans_inv=lambda x: x)

        self.assertTrue(np.allclose(p1, p2))

    def test_swarmplot_accepts_random_state_kwarg(self):
        data = {
            "group": ["a"] * 20,
            "value": np.linspace(0, 1, 20),
        }
        ax = sns.swarmplot(data=data, x="group", y="value", overflow="random", random_state=7)
        self.assertGreater(len(ax.collections), 0)


if __name__ == "__main__":
    unittest.main()
