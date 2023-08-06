import networkx as nx
import time
import pandas as pd
from pathlib import Path


# --------------------------------------------------------------------------------------
# PARSING AND CONVERSION FOR MULTILAYER NETWORKS
# --------------------------------------------------------------------------------------
def parse_multilayer_edgelist(
    multiedgelist, directed, edges_are_distance=False, sep="\t", header=False
):
    """
    Convert a multilayer edge list into a NetworkX Graph.

    Parameters
    ----------
    multiedgelist : str
        Path to the multilayer edge list (csv file , no index) to be converted. Consists
        of the columns 'source', 'source_layer', 'target', 'target_layer', 'weight'.
    directed : bool
        Whether the network is directed or not.
    edges_are_distance : bool
        Whether edge weights indicate distance between nodes (opposed to
        weight/similarity). If network is unweighted, set to False. Default is False.
    sep : str
        Delimiter used in the multilayer edge list .csv file. Default is '\\t'.
    header : bool
        Whether the multilayer edge list .csv file has a header row. Default is False.

    Returns
    -------
    NetworkX (Di)Graph
        Multilayer network parsed from the passed in edge list. Nodes are tuples of the
        form ('n','l') where 'n' is the name of the node and 'l' is the layer it belongs
        to. Every node additionally has an attribute 'layer' which denotes its layer.
        Edges have an attribute 'weight'. If the edge attribute of the input graph is
        'distance', distances are converted to 'weights' through distance/1.
    """
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    with open(multiedgelist) as IN:
        for i, line in enumerate(IN):
            # Skip header row
            if header and i == 0:
                continue

            parts = line.strip().split(sep=sep)
            if len(parts) == 5:
                source, source_layer, target, target_layer, weight = parts
            elif len(parts) == 4:
                source, source_layer, target, target_layer = parts
                weight = 1
            else:
                raise ValueError(
                    f"[ERROR] mutliedgelist has too many columns: {len(parts)}. The"
                    f" columns should be 'source', 'source_layer', 'target',"
                    f" 'target_layer', 'weight'. Check that the multilayer edge list"
                    f" does not have an index column."
                )

            if edges_are_distance:
                weight = 1 / float(weight)
            else:
                weight = float(weight)

            G.add_node((source, source_layer), layer=source_layer)
            G.add_node((target, target_layer), layer=target_layer)
            G.add_edge((source, source_layer), (target, target_layer), weight=weight)

    return G


# --------------------------------------------------------------------------------------
# OUTPUT
# --------------------------------------------------------------------------------------
def timed_invoke(action_desc, method):
    """
    Invoke a method with timing.

    Parameters
    ----------
    action_desc : str
        The string describing the method action.
    method : function
        The method to invoke.

    Returns
    -------
    object
        The return object of the method.
    """
    print(f"[STATUS] Started {action_desc}...")
    start = time.time()
    try:
        output = method()
        print(
            f"[STATUS] Finished {action_desc} in {round((time.time() - start), 1)}"
            f" seconds"
        )
        return output
    except Exception:
        print(
            f"[ERROR] Exception while {action_desc} after"
            f" {round((time.time() - start), 1)} seconds"
        )
        raise


def emb_to_dataframe(emb_file):
    """
    Convert an embedding file, as output from a trained word2vec model, to a pandas
    DataFrame.

    Parameters
    ----------
    emb_file : str
        Absolute path of the word2vec embedding file.

    Returns
    -------
    pandas DataFrame
        word2vec embedding as a dataframe.
    """
    embedding = pd.read_csv(
        emb_file, delim_whitespace=True, skiprows=1, header=None, index_col=False
    )

    # The node names are split up across the first two columns because they are tuples.
    # We therefore join the first two columns.
    if isinstance(embedding[1].iloc[0], str):
        node_column = embedding[0] + embedding[1]
        embedding[0] = node_column
        embedding.drop(columns=1, inplace=True)

    # Set first column (node names) as index column
    embedding.set_index(0, inplace=True)
    embedding.sort_index(inplace=True)

    return embedding


def clean_output_directory(dir_path):
    """
    Check if output directory exists, otherwise created it.

    Parameters
    ----------
    dir_path : str or pathlib.Path
        Path of the output directory.

    Returns
    -------
    pathlib.Path object
        Absolute path of the output directory.
    """
    directory = Path(dir_path)
    if directory.is_dir():
        return directory
    else:
        directory.mkdir()
        print(f"Created output directory {directory}.")
        return directory
