import argparse
import time
from . import utils
from . import henhoe2vec_walks
from . import embeddings


def parse_args():
    """
    Parse arguments for HeNHoE-2vec.
    """
    parser = argparse.ArgumentParser(description="Run HeNHoE-2vec.")

    parser.add_argument(
        "--input",
        type=str,
        help=(
            "Path to the multilayer edge list of the network to be embedded (csv file"
            " with no index)."
        ),
    )

    parser.add_argument(
        "--sep", type=str, help=("Delimiter of the input csv edge list."), default="\t"
    )

    parser.add_argument(
        "--header",
        action="store_true",
        help=("Pass this argument if the input csv edge list has a header."),
    )

    parser.add_argument(
        "--output_name",
        type=str,
        help=(
            "Name of the output .csv file (without suffix). Default is 'embeddings'."
        ),
        default="embeddings",
    )

    parser.add_argument(
        "--is_directed",
        action="store_true",
        help="Pass this argument if the network is directed.",
    )

    parser.add_argument(
        "--edges_are_distance",
        action="store_true",
        help=(
            "Pass this argument if edge weights indicate distance between nodes"
            " (opposed to weight/similarity)."
        ),
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path of the output directory where the embedding files will be saved.",
    )

    parser.add_argument(
        "--dimensions",
        type=int,
        default=128,
        help="The dimensionality of the embeddings. Default is 128.",
    )

    parser.add_argument(
        "--walk_length",
        type=int,
        default=20,
        help="Length of each random walk. Default is 20.",
    )

    parser.add_argument(
        "--num_walks",
        type=int,
        default=10,
        help="Number of random walks to simulate for each node. Default is 10.",
    )

    parser.add_argument(
        "--p",
        type=float,
        default=1.0,
        help="Return parameter p from the node2vec algorithm. Default is 1.",
    )

    parser.add_argument(
        "--q",
        type=float,
        default=0.5,
        help="In-out parameter q from the node2vec algorithm. Default is 0.5.",
    )

    parser.add_argument(
        "--s",
        type=float,
        default=1.0,
        help=(
            "Default switching parameter for layer pairs which are not specified"
            " in the --s-dict argument. Default is 1."
        ),
    )

    parser.add_argument(
        "--s_dict",
        nargs="*",
        default=[],
        help=(
            "Switching parameters for specific layer"
            " pairs in a dict-like manner. Pass the names of layer pairs followed by"
            " their switching parameters, separated by whitespaces. E.g., if the"
            " switching parameter from layer1 to layer2 is 0.5 and the switching"
            " parameter from layer2 to layer1 is 0.7, you would pass 'layer1 layer2"
            " 0.5 layer2 layer1 0.7'. Note that layer pairs are directed. For all layer"
            " pairs which are not specified here, the default parameter --s is adopted."
        ),
    )

    parser.add_argument(
        "--window_size",
        type=int,
        default=10,
        help="Context size for the word2vec optimization. Default is 10.",
    )

    parser.add_argument(
        "--epochs", default=1, type=int, help="Number of epochs in SGD. Default is 1."
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers (threads). Default is 8.",
    )

    return parser.parse_args()


def parse_switching_param(s, s_dict):
    """
    Parse the switching arguments s and s-dict passed as script arguments.

    Parameters
    ----------
    s : float
        The default switching parameter `s`. Can be None if ALL possible layer pairs are
        specified in `s_dict`.
    s_dict : list
        List specifying the switching parameter for specific layer pairs.

    Returns
    -------
    dict
        `s` and `s_dict` parsed as a dict. The default switching parameter `s` is
        specified as the entry {"default" : s} in the returned dict.
    """
    switching_dict = {}
    # Default switching parameter
    if s:
        switching_dict["default"] = s

    while len(s_dict) > 0:
        triple = s_dict[:3]
        s_dict = s_dict[3:]
        try:
            switching_dict[(triple[0], triple[1])] = float(triple[2])
        except:
            raise ValueError(
                "[ERROR] Argument --s-dict has the wrong form. Should consist of"
                " 'layer layer s' triples, e.g., 'layer1 layer2 0.5 layer2 layer1 0.7'."
            )

    if len(switching_dict) == 0:
        raise ValueError(
            "[ERROR] Arguments --s and --s-dict cannot both be empty/None."
        )

    return switching_dict


def run(
    input_csv,
    output_dir,
    sep="\t",
    header=False,
    output_name="embeddings",
    is_directed=False,
    edges_are_distance=False,
    dims=128,
    walk_length=20,
    num_walks=10,
    p=1.0,
    q=0.5,
    s=1.0,
    window_size=10,
    epochs=1,
    workers=8,
    verbose=True,
):
    """
    Main method to embed the nodes of a HeNHoE (multilayer) network using the
    HeNHoE-2vec algorithm. Results are saved as .emb and .csv files.

    Parameters
    ----------
    input_csv : str
        Path to the multilayer edge list of the network to be embedded (csv file with
        no index).
    output_dir : str
        Path of the output directory where the embedding files will be saved.
    sep : str
        Delimiter of the input csv edge list. Default is "\\t".
    header : bool
        Whether the input csv edge list has a header. Default is False.
    output_name : str
        Name of the output .csv file (without suffix). Default is "embeddings".
    is_directed : bool
        Whether the network is directed. Default is False.
    edges_are_distance : bool
        Whether edge weights indicate distance between nodes (opposed to
        weight/similarity). Default is False.
    dims : int
        The dimensionality of the embeddings. Default is 128.
    walk_length : int
        Length of each random walk. Default is 20.
    num_walks : int
        Number of random walks to simulate for each node. Default is 10.
    p : float
        The return parameter `p` from the node2vec algorithm. Default is 1.
    q : float
        The in-out parameter `q` from the node2vec algorithm. Default is 0.5.
    s : float or dict
        The type-switching parameter(s) of the HeNHoE-2vec algorithm. There are two
        modes:
        Simple switching: If the probability to switch between layers should be the
        same for all pairs of layers, passing a single float suffices.
        Versus specific switching: We might want to have different probabilities for
        switching between specific layers. In this case, we can pass a dict of the
        form {("layer1","layer2") : 0.5, ("layer2","layer1") : 0.2, "default" : 1}.
        Note that the layer pairs are directed, i.e., the switching parameter from
        layer1 to layer2 may be different than the switching parameter from layer2
        to layer1. The "default" switching parameter is used for layer pairs which
        don't have an explicit entry in the dict.
        The switching modes "multiple switching" and "special node switching" are
        special cases of "versus specific switching" and are therefore not explicitly
        implemented here.
    window_size : int
        Context size for the word2vec optimization. Default is 10.
    epochs : int
        Number of epochs in SGD. Default is 1.
    workers : int
        Number of parallel workers (threads). Default is 8.
    verbose : bool
        Whether to print status messages. Default is True.
    """
    start = time.time()
    # Parse multilayer network
    if verbose:
        N_nx = utils.timed_invoke(
            "parsing edgelist",
            lambda: utils.parse_multilayer_edgelist(
                input_csv, is_directed, edges_are_distance, sep=sep, header=header
            ),
        )
    else:
        N_nx = utils.parse_multilayer_edgelist(
            input_csv, is_directed, edges_are_distance
        )

    # Create HenHoe2vec object
    hh2v = henhoe2vec_walks.HenHoe2vec(N_nx, is_directed, p, q, s)

    # Preprocess transition probabilities
    if verbose:
        utils.timed_invoke(
            "preprocessing transition probabilities",
            lambda: hh2v.preprocess_transition_probs(),
        )
    else:
        hh2v.preprocess_transition_probs()

    # Generate random walks
    if verbose:
        walks = utils.timed_invoke(
            "generating random walks",
            lambda: hh2v.simulate_walks(num_walks, walk_length),
        )
    else:
        walks = hh2v.simulate_walks(num_walks, walk_length)

    # Learn and save embeddings
    if verbose:
        utils.timed_invoke(
            "learning and saving embeddings",
            lambda: embeddings.generate_embeddings(
                walks,
                output_dir,
                output_name,
                dims,
                window_size,
                epochs,
                workers,
                verbose,
            ),
        )
    else:
        embeddings.generate_embeddings(
            walks,
            output_dir,
            output_name,
            dims,
            window_size,
            epochs,
            workers,
            verbose,
        )

    finish = time.time()
    if verbose:
        print(
            f"[STATUS] Completed multilayer network embedding in"
            f" {round((finish - start), 1)} seconds. See results in {output_dir}."
        )


def main():
    args = parse_args()
    # Parse arguments s and s-dict
    s = parse_switching_param(args.s, args.s_dict)
    run(
        input_csv=args.input,
        output_dir=args.output_dir,
        sep=args.sep,
        header=args.header,
        output_name=args.output_name,
        is_directed=args.is_directed,
        edges_are_distance=args.edges_are_distance,
        dims=args.dimensions,
        walk_length=args.walk_length,
        num_walks=args.num_walks,
        p=args.p,
        q=args.q,
        s=s,
        window_size=args.window_size,
        epochs=args.epochs,
        workers=args.workers,
        verbose=True,
    )
