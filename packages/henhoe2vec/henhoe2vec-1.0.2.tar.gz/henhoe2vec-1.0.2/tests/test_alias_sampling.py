import numpy as np
import pytest
from henhoe2vec import alias_sampling


class TestAliasSampling:
    def test_alias_setup_known_outcome(self):
        probs = [0.25, 0.3, 0.05, 0.4]
        target_J = np.array([0, 0, 3, 1])
        target_q = np.array([1.0, 1.0, 0.2, 0.8])

        J, q = alias_sampling.alias_setup(probs)

        assert np.array_equal(J, target_J)
        assert np.array_equal(q, target_q)

    def test_alias_setup_uniform_distribution(self):
        probs = [0.2, 0.2, 0.2, 0.2, 0.2]
        target_J = np.array([0, 0, 0, 0, 0])
        target_q = np.array([1, 1, 1, 1, 1])

        J, q = alias_sampling.alias_setup(probs)

        assert np.array_equal(J, target_J)
        assert np.array_equal(q, target_q)

    def test_alias_draw(self):
        probs = [0, 0, 1, 0]

        J, q = alias_sampling.alias_setup(probs)
        sample = alias_sampling.alias_draw(J, q)

        assert sample == 2

    def test_negative_prob_exception(self):
        probs = [0.2, 0.4, -0.2]

        with pytest.raises(ValueError):
            J, q = alias_sampling.alias_setup(probs)
