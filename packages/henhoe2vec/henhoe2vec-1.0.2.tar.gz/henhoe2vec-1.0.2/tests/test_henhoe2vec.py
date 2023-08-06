import pytest
import pandas as pd
from henhoe2vec import henhoe2vec

import helpers_testing


class TestHenHoe2vec:
    def test_parse_switching_param(self):
        s = 1.1
        s_dict = ["l1", "l2", "0.53", "l2", "l1", "1.2"]
        s = henhoe2vec.parse_switching_param(s, s_dict)

        assert s["default"] == 1.1
        assert s[("l1", "l2")] == float(0.53)

    def test_parse_switching_param_sdict_too_long(self):
        s = 1.0
        # Improper s_dict argument
        s_dict = ["l1", "l2", "0.53", "l2", "l1", "1.2", "l2"]

        with pytest.raises(ValueError):
            s = henhoe2vec.parse_switching_param(s, s_dict)

    def test_parse_switching_param_s_emtpy(self):
        s = None
        s_dict = []

        with pytest.raises(ValueError):
            s = henhoe2vec.parse_switching_param(s, s_dict)

    def test_henhoe2vec(self, tmp_path):
        # Weighted, undirected graph
        test_data = {
            "source": ["n1", "n2", "n3", "n1", "n4", "n5", "n1"],
            "source_layer": ["l1", "l1", "l2", "l2", "l2", "l1", "l1"],
            "target": ["n2", "n3", "n1", "n2", "n5", "n1", "n5"],
            "target_layer": ["l1", "l2", "l1", "l2", "l2", "l1", "l1"],
            "weight": [1, 0.5, 0.2, 1.1, 0.1, 0.3, 0.4],
        }
        NUM_NODES = 8
        DIMS = 16
        df = pd.DataFrame.from_dict(test_data)

        edgelist_path = helpers_testing.save_test_edgelist(
            df, tmp_path, sep="\t", header=False
        )
        output_path = tmp_path.joinpath("output/")

        # Run HeNHoE-2vec
        henhoe2vec.run(
            edgelist_path,
            output_path,
            is_directed=False,
            dims=DIMS,
            walk_length=10,
            num_walks=5,
        )

        # Assert that a .csv file was produced
        assert len(list(output_path.glob("*.csv"))) == 1
        # Assert that output .csv file has correct shape
        for output_csv in output_path.glob("*.csv"):
            df = pd.read_csv(output_csv, sep="\t", index_col=None, header=None)
            print(df)
            # NUM_NODES rows and DIMS+1 columns
            assert df.shape == (NUM_NODES, DIMS + 1)
