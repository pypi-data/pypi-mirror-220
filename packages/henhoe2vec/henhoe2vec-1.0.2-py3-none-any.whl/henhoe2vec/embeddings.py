from gensim.models import word2vec as w2v
from pathlib import Path
from . import utils


def generate_embeddings(
    walks,
    output_dir,
    output_name="embeddings",
    dimensions=128,
    window_size=10,
    epochs=1,
    workers=8,
    verbose=True,
):
    """
    Learn the embeddings of the nodes by optimizing the Skip-Gram objective using SGD.
    Save embeddings to `output_dir` in word2vec and csv format.

    Parameters
    ----------
    walks : list of list of 2-tuples of strs
        The list of random walks generated over the HeNHoE network.
    output_dir : str
        Path of the output directory where the embedding files shall be saved, e.g.,
        "project/output/".
    output_name : str
        Name of the output .csv embedding file (without suffix). Default is
        "embeddings".
    dimensions : int
        The dimensionality of the embeddings. Default is 128.
    window_size : int
        Context size for optimization. Default is 10.
    epochs : int
        Number of epochs in SGD. Default is 1.
    workers : int
        Number of parallel workers (threads). Default is 8.
    verbose : bool
        Whether to print status messages. Default is True.
    """
    # Generate embeddings
    walks = [list(map(str, walk)) for walk in walks]
    w2v_model = w2v.Word2Vec(
        walks,
        vector_size=dimensions,
        window=window_size,
        epochs=epochs,
        min_count=0,
        sg=1,
        workers=workers,
    )

    # Remove redundant suffix
    if ".csv" in output_name:
        output_name = output_name.split(".csv")[0]

    # Save embeddings
    output_dir = utils.clean_output_directory(output_dir)
    output_emb = output_dir.joinpath(f"{output_name}.emb")
    w2v_model.wv.save_word2vec_format(output_emb, total_vec=dimensions)

    output_csv = output_dir.joinpath(f"{output_name}.csv")
    embedding_df = utils.emb_to_dataframe(output_emb)
    embedding_df.to_csv(output_csv, sep="\t", header=False)
    if verbose:
        print(f"[STATUS] Saved embeddings to {output_csv}")

    # Remove temporary .emb file
    output_emb.unlink()
