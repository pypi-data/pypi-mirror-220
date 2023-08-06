import networkx as nx
import numpy as np
from henhoe2vec import henhoe2vec_walks, alias_sampling


def prepare_test_network():
    """
    Prepare a small test network and return it as a NetworkX graph.
    """
    N = nx.Graph()
    nodes_l1 = [("n1", "l1"), ("n2", "l1")]
    nodes_l2 = [("n3", "l2"), ("n4", "l2")]
    N.add_nodes_from(nodes_l1, layer="l1")
    N.add_nodes_from(nodes_l2, layer="l2")
    N.add_edge(("n1", "l1"), ("n2", "l1"), weight=0.5)
    N.add_edge(("n2", "l1"), ("n3", "l2"), weight=0.2)
    N.add_edge(("n1", "l1"), ("n3", "l2"), weight=0.5)
    N.add_edge(("n3", "l2"), ("n4", "l2"), weight=0.4)

    return N


class TestHenHoe2vecWalks:
    def test_preprocess_transition_probabilities(self):
        # Test network
        N = prepare_test_network()
        # Set HeNHoE-2vec parameters
        p = 1
        q = 0.5
        s = {("l1", "l2"): 0.5, ("l2", "l1"): 1}
        # Construct HenHoe2vec object
        hh2v = henhoe2vec_walks.HenHoe2vec(N, is_directed=False, p=p, q=q, s=s)
        # Preprocess transition probabilities
        hh2v.preprocess_transition_probs()

        # Target node/edge transition probabilities (pre-computed by hand)
        target_node_trans_probs = {
            ("n1", "l1"): [1 / 3, 2 / 3],
            ("n2", "l1"): [5 / 9, 4 / 9],
            ("n3", "l2"): [5 / 11, 2 / 11, 4 / 11],
            ("n4", "l2"): [1],
        }
        target_edge_trans_probs = {
            (("n1", "l1"), ("n2", "l1")): [5 / 9, 4 / 9],
            (("n2", "l1"), ("n1", "l1")): [1 / 3, 2 / 3],
            (("n1", "l1"), ("n3", "l2")): [5 / 15, 2 / 15, 8 / 15],
            (("n3", "l2"), ("n1", "l1")): [1 / 3, 2 / 3],
            (("n2", "l1"), ("n3", "l2")): [5 / 15, 2 / 15, 8 / 15],
            (("n3", "l2"), ("n2", "l1")): [5 / 9, 4 / 9],
            (("n3", "l2"), ("n4", "l2")): [1],
            (("n4", "l2"), ("n3", "l2")): [5 / 9, 2 / 9, 2 / 9],
        }

        # Get alias and probability tables
        target_node_trans_alias = {}
        for node, probs in target_node_trans_probs.items():
            target_node_trans_alias[node] = alias_sampling.alias_setup(probs)
        target_edge_trans_alias = {}
        for edge, probs in target_edge_trans_probs.items():
            target_edge_trans_alias[edge] = alias_sampling.alias_setup(probs)

        # Assetions
        assert target_node_trans_alias.keys() == hh2v.transition_probs_nodes.keys()
        assert target_edge_trans_alias.keys() == hh2v.transition_probs_edges.keys()

        # Assert that alias and probability tables are correct
        for key in target_node_trans_alias.keys():
            J_target, q_target = target_node_trans_alias[key]
            J, q = hh2v.transition_probs_nodes[key]
            assert np.array_equal(J, J_target)
            # Round to 5 decimal places in order to avoid failure due to rounding errors
            assert np.array_equal(np.round(q, 5), np.round(q_target, 5))

        for key in target_edge_trans_alias.keys():
            J_target, q_target = target_edge_trans_alias[key]
            J, q = hh2v.transition_probs_edges[key]
            assert np.array_equal(J, J_target)
            # Round to 5 decimal places in order to avoid failure due to rounding errors
            assert np.array_equal(np.round(q, 5), np.round(q_target, 5))

    def test_walk_generation(self):
        # Test network
        N = prepare_test_network()
        # Set HeNHoE-2vec parameters
        p = 1
        q = 0.5
        s = {("l1", "l2"): 0.5, ("l2", "l1"): 1}
        # Construct HenHoe2vec object
        hh2v = henhoe2vec_walks.HenHoe2vec(N, is_directed=False, p=p, q=q, s=s)
        # Preprocess transition probabilities
        hh2v.preprocess_transition_probs()

        # Simulate walks
        walks = hh2v.simulate_walks(num_walks=5, walk_length=10)

        assert len(walks) == 5 * N.number_of_nodes()
        assert len(walks[0]) == 10
