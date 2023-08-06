import random

# from alias_sampling import alias_setup, alias_draw
from .alias_sampling import alias_setup, alias_draw


class HenHoe2vec:
    """
    A class to generate HeNHoE-2vec random walks over a heterogeneous-node
    homogeneous-edge network.

    Attributes
    ----------
    henhoe_network : NetworkX Graph
        Heterogeneous-node homogeneous-edge network.
    is_directed : bool
        Whether the network is directed or not.
    p : float
        The return parameter `p` from the node2vec algorithm.
    q : float
        The in-out parameter `q` from the node2vec algorithm.
    s : dict
        The type-switching parameter(s) of the HeNHoE-2vec algorithm.
    transition_probs_nodes : dict
        Transition probability distribution to neighbors of each node based only on edge
        weights and switching parameters.
    transition_probs_edges : dict
        Transition probability distribution to neighbors of each node based on edge
        weights, p, q, and switching parameters.
    """

    def __init__(self, henhoe_network, is_directed, p, q, s):
        """
        Constructor for the HenHoe2vec class.

        Parameters
        ----------
        henhoe_network : NetworkX Graph
            Heterogeneous-node homogeneous-edge network.
        is_directed : bool
            Whether the network is directed or not.
        p : float
            The return parameter `p` from the node2vec algorithm.
        q : float
            The in-out parameter `q` from the node2vec algorithm.
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
            special cases of "versus specific switching" and are therefore not
            explicitly implemented here.

        Returns
        -------
        HenHoe2vec
            Constructed HenHoe2vec object.
        """
        self.N = henhoe_network
        self.is_directed = is_directed
        self.p = p  # Return parameter
        self.q = q  # In-out parameter

        # Transition probability distribution to neighbors of each node based only on
        # edge weights and switching parameters. Only used for first step of each walk
        # where there is no previous node.
        # Form: {node : (J, q)}
        self.transition_probs_nodes = {}
        # Transition probability distribution to neighbors of each node based on edge
        # weights, p, q, and switching parameters. Used for all other steps of the walk.
        # Form: {(node1, node2) : (J, q)}
        self.transition_probs_edges = {}

        if type(s) in [float, int]:
            self.s = {"default": s}
        elif type(s) == dict:
            self.s = s
        else:
            raise TypeError(
                f"[ERROR] Invalid type for argument s. Should be float or dict but"
                f" is {type(s)}."
            )

    # ----------------------------------------------------------------------------------
    # RANDOM WALKS
    # ----------------------------------------------------------------------------------
    def henhoe2vec_walk(self, walk_length, start_node):
        """
        Simulate a random walk of length `walk_length` starting from `start_node`.

        Parameters
        ----------
        walk_length : int
            Length of the random walk.
        start_node : 2-tuple of strs
            Starting node of the random walk, e.g., ('n1','l1').

        Returns
        -------
        list of 2-tuples of strs (nodes)
            Random walk of length `walk_length` starting from `start_node`.
        """
        N = self.N
        transition_probs_nodes = self.transition_probs_nodes
        transition_probs_edges = self.transition_probs_edges

        walk = [start_node]

        while len(walk) < walk_length:
            current = walk[-1]
            neighbors = sorted(N.neighbors(current))
            if len(neighbors) > 0:
                # First step of the walk
                if len(walk) == 1:
                    J = transition_probs_nodes[current][0]
                    q = transition_probs_nodes[current][1]
                    next = neighbors[alias_draw(J, q)]
                    walk.append(next)
                # All other steps of the walk
                else:
                    previous = walk[-2]
                    J = transition_probs_edges[(previous, current)][0]
                    q = transition_probs_edges[(previous, current)][1]
                    next = neighbors[alias_draw(J, q)]
                    walk.append(next)
            else:
                break

        return walk

    def simulate_walks(self, num_walks, walk_length):
        """
        Simulate `num_walks` random walks of length `walk_length` for each node.

        Parameters
        ----------
        num_walks : int
            Number of random walks to simulate for each node.
        walk_length : int
            Length of each random walk.

        Returns
        -------
        list of list of 2-tuples of strs
            List of random walks.
        """
        N = self.N
        nodes = list(N.nodes)
        walks = []

        for _ in range(num_walks):
            random.shuffle(nodes)  # Shuffle nodes to switch up the order
            for node in nodes:
                walk = self.henhoe2vec_walk(walk_length=walk_length, start_node=node)
                walks.append(walk)

        return walks

    # ----------------------------------------------------------------------------------
    # CALCULATE TRANSITION PROBABILITIES
    # ----------------------------------------------------------------------------------
    def get_node_trans_probs(self, node):
        """
        Using alias sampling, calculate the discrete transition probability distribution
        from node to all its neighbors based on edge weights and switching parameters.
        Only used for first step of each walk where there is no previous node.

        Parameters
        ----------
        node : 2-tuple of strs
            Node for which to get the transition probabilities, e.g., ('n1','l1').

        Returns
        -------
        J : list of ints
            The alias table.
        q : list of floats
            The probability table.
        """
        N = self.N
        s = self.s

        # Unnormalized transition probabilities based on edge weights
        unnormalized_probs = []
        for nbr in sorted(N.neighbors(node)):
            src_layer = N.nodes[node]["layer"]
            trgt_layer = N.nodes[nbr]["layer"]
            weight = N[node][nbr]["weight"]

            if src_layer == trgt_layer:
                unnormalized_probs.append(weight)
            else:
                # Get switching parameter
                if (src_layer, trgt_layer) in s:
                    switch_param = s[(src_layer, trgt_layer)]
                else:
                    try:
                        switch_param = s["default"]
                    except:
                        raise ValueError(
                            f"[ERROR] The dict of switching parameters s must contain a"
                            f" 'default' entry."
                        )
                unnormalized_probs.append(weight / switch_param)

        # Normalization constant
        norm_const = sum(unnormalized_probs)
        # Normalized transition probabilities
        normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]

        return alias_setup(normalized_probs)

    def get_edge_trans_probs(self, previous, current):
        """
        Using alias sampling, calculate the discrete transition probability distribution
        from `current` to all its neighbors based on edge weights, p, q, and switching
        parameters. `previous` is the previous node of the walk. Used for all steps of
        the walk except for the first one.

        Parameters
        ----------
        previous : 2-tuple of strs
            Previous node on the random walk, e.g., ('n1','l1').
        current : 2-tuple of strs
            Current node on the random walk for which we want to calculate the
            transition probabilities to its neighbors, e.g., ('n2','l1').

        Returns
        -------
        J : list of ints
            The alias table.
        q : list of floats
            The probability table.
        """
        N = self.N
        p = self.p
        q = self.q
        s = self.s

        # Unnormalized transition probabilities
        unnormalized_probs = []
        for nbr in sorted(N.neighbors(current)):
            src_layer = N.nodes[current]["layer"]
            trgt_layer = N.nodes[nbr]["layer"]
            weight = N[current][nbr]["weight"]

            # Neighbor is on the same layer
            if src_layer == trgt_layer:
                if nbr == previous:
                    unnormalized_probs.append(weight / p)  # Return
                elif N.has_edge(previous, nbr):
                    unnormalized_probs.append(weight)
                else:
                    unnormalized_probs.append(weight / q)  # Explore
            # Neighbor is on a different layer
            else:
                # Get switching parameter
                if (src_layer, trgt_layer) in s:
                    switch_param = s[(src_layer, trgt_layer)]
                else:
                    try:
                        switch_param = s["default"]
                    except:
                        raise ValueError(
                            f"[ERROR] The dict of switching parameters s must contain a"
                            f" 'default' entry."
                        )

                if nbr == previous:
                    unnormalized_probs.append(weight / (p * switch_param))  # Return
                elif N.has_edge(previous, nbr):
                    unnormalized_probs.append(weight / switch_param)
                else:
                    unnormalized_probs.append(weight / (q * switch_param))  # Explore

        # Normalization constant
        norm_const = sum(unnormalized_probs)
        # Normalized transition probabilities
        normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]

        return alias_setup(normalized_probs)

    def preprocess_transition_probs(self):
        """
        Preprocessing of transition probabilities for guiding the random walks.
        """
        N = self.N
        is_directed = self.is_directed

        transition_probs_nodes = {}
        transition_probs_edges = {}

        # Calculate the transition probabilities for the first step of the walks
        for node in N.nodes:
            transition_probs_nodes[node] = self.get_node_trans_probs(node)

        # Calculate the transition probabilities for all other steps of the walks
        if is_directed:
            for edge in N.edges:
                transition_probs_edges[edge] = self.get_edge_trans_probs(
                    edge[0], edge[1]
                )
        else:
            for edge in N.edges:
                transition_probs_edges[edge] = self.get_edge_trans_probs(
                    edge[0], edge[1]
                )
                transition_probs_edges[(edge[1], edge[0])] = self.get_edge_trans_probs(
                    edge[1], edge[0]
                )

        self.transition_probs_nodes = transition_probs_nodes
        self.transition_probs_edges = transition_probs_edges

        return
