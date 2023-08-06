import pandas as pd
from henhoe2vec import utils
from pathlib import Path

import helpers_testing


class TestUtils:
    def test_parse_edgelist_undirected(self, tmp_path):
        # Weighted, undirected graph
        test_data = {
            "source": ["n1", "n2", "n3", "n1", "n4", "n5", "n1"],
            "source_layer": ["l1", "l1", "l2", "l2", "l2", "l1", "l1"],
            "target": ["n2", "n3", "n1", "n2", "n5", "n1", "n5"],
            "target_layer": ["l1", "l2", "l1", "l2", "l2", "l1", "l1"],
            "weight": [1, 0.5, 0.2, 1.1, 0.1, 0.3, 0.4],
        }
        df = pd.DataFrame.from_dict(test_data)

        # tab delimiter and no header
        edgelist_path = helpers_testing.save_test_edgelist(
            df, tmp_path, sep="\t", header=False
        )

        N_nx = utils.parse_multilayer_edgelist(
            edgelist_path,
            directed=False,
            edges_are_distance=False,
            sep="\t",
            header=False,
        )
        num_nodes = 8
        num_edges = 6  # Graph is undirected, so edges 6 and 7 are equal

        assert N_nx.number_of_nodes() == num_nodes
        assert N_nx.number_of_edges() == num_edges
        assert ("n1", "l1") in N_nx.nodes
        assert (("n3", "l2"), ("n1", "l1")) in N_nx.edges
        assert (("n1", "l1"), ("n3", "l2")) in N_nx.edges
        assert N_nx[("n4", "l2")][("n5", "l2")]["weight"] == 0.1
        assert N_nx.degree(("n1", "l1")) == 3

    def test_parse_edgelist_directed(self, tmp_path):
        # Weighted, directed graph
        test_data = {
            "source": ["n1", "n2", "n3", "n1", "n4", "n5", "n1"],
            "source_layer": ["l1", "l1", "l2", "l2", "l2", "l1", "l1"],
            "target": ["n2", "n3", "n1", "n2", "n5", "n1", "n5"],
            "target_layer": ["l1", "l2", "l1", "l2", "l2", "l1", "l1"],
            "weight": [1, 0.5, 0.2, 1.1, 0.1, 0.3, 0.4],
        }
        df = pd.DataFrame.from_dict(test_data)
        num_nodes = 8
        num_edges = 7

        # ',' delimiter and header
        edgelist_path = helpers_testing.save_test_edgelist(
            df, tmp_path, sep=",", header=True
        )

        # Here we set edges_are_distance=True, so all weights should be inverted
        N_nx = utils.parse_multilayer_edgelist(
            edgelist_path, directed=True, edges_are_distance=True, sep=",", header=True
        )

        assert N_nx.number_of_nodes() == num_nodes
        assert N_nx.number_of_edges() == num_edges
        assert ("n1", "l1") in N_nx.nodes
        assert (("n3", "l2"), ("n1", "l1")) in N_nx.edges
        assert (("n1", "l1"), ("n3", "l2")) not in N_nx.edges
        # Check if edge weights are inverted
        assert N_nx[("n4", "l2")][("n5", "l2")]["weight"] == 10
        assert N_nx.out_degree(("n1", "l1")) == 2
        # Sum of weights of all in-going and out-going edges
        assert (
            N_nx.degree(("n1", "l1"), weight="weight")
            == 1 + 1 / 0.2 + 1 / 0.3 + 1 / 0.4
        )

    def test_timed_invoke(self):
        result = utils.timed_invoke("test", lambda: 3 + 5)
        assert result == 8

    def test_emb_to_dataframe_tuple_nodes(self):
        """
        Test that .emb files spit out by word2vec are correctly converted to DataFrames
        and that node names which are tuples are correctly joined into a single column.
        """
        test_emb_file = Path("tests/resources/small_test_embedding_tuple_names.emb")
        NUM_ROWS = 8
        NUM_COLUMNS = 16  # 16 dims (node name doesn't count because it's the index)
        df = utils.emb_to_dataframe(test_emb_file)
        print(df)
        assert df.shape == (NUM_ROWS, NUM_COLUMNS)

    def test_emb_to_dataframe_tuple_nodes(self):
        """
        Test that .emb files spit out by word2vec are correctly converted to DataFrames
        also for embeddings with single-string node names (not tuples).
        """
        test_emb_file = Path("tests/resources/small_test_embedding_single_names.emb")
        NUM_ROWS = 8
        NUM_COLUMNS = 16  # 16 dims (node name doesn't count because it's the index)
        df = utils.emb_to_dataframe(test_emb_file)
        print(df)
        assert df.shape == (NUM_ROWS, NUM_COLUMNS)
