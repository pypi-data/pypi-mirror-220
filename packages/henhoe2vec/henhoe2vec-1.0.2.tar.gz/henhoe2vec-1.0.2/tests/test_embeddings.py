import pandas as pd
from henhoe2vec import embeddings


def test_generate_embeddings(tmp_path):
    # Define random walks (with 10 different nodes)
    walks = [
        [2, 4, 5, 6, 7],
        [5, 6, 2, 4, 5],
        [1, 9, 8, 5, 3],
        [6, 4, 3, 6, 5],
        [1, 3, 5, 6, 7],
    ]
    NUM_NODES = 9
    DIMS = 16

    # Generate embeddings
    embeddings.generate_embeddings(walks, tmp_path, dimensions=DIMS, window_size=3)

    # Assert that a .csv file was produced
    assert len(list(tmp_path.glob("*.csv"))) == 1

    for output_csv in tmp_path.glob("*.csv"):
        df = pd.read_csv(output_csv, sep="\t", index_col=None, header=None)
        print(df)
        # NUM_NODES rows and DIMS+1 columns
        assert df.shape == (NUM_NODES, DIMS + 1)
