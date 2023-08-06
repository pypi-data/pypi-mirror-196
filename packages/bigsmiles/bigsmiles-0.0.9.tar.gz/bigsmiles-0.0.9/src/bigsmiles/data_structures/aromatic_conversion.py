import heapq
import itertools
from collections import deque
from typing import List, Optional
from bigsmiles.data_structures.bigsmiles import BigSMILES


def kekulize(BigSMILES) -> BigSMILES:
    """
    kekulize: is the process of assigning double bonds to a molecular graph.
    Specifically, it will convert aromatic_elements symbols and 1.5 bonds in aromatic_elements rings
    to alternating double bonds and normal symbol symbols.

    """
    ds = self._delocal_subgraph
    kept_nodes = set(itertools.filterfalse(self._prune_from_ds, ds))

    # relabel kept DS nodes to be 0, 1, 2, ...
    label_to_node = list(sorted(kept_nodes))
    node_to_label = {v: i for i, v in enumerate(label_to_node)}

    # pruned and relabelled DS
    pruned_ds = [list() for _ in range(len(kept_nodes))]
    for node in kept_nodes:
        label = node_to_label[node]
        for adj in filter(lambda v: v in kept_nodes, ds[node]):
            pruned_ds[label].append(node_to_label[adj])

    matching = find_perfect_matching(pruned_ds)
    if matching is None:
        return False

    # de-aromatize and then make double bonds
    for node in ds:
        for adj in ds[node]:
            self.update_bond_order(node, adj, new_order=1)
        self._atoms[node].is_aromatic = False
        self._bond_counts[node] = int(self._bond_counts[node])

    for matched_labels in enumerate(matching):
        matched_nodes = tuple(label_to_node[i] for i in matched_labels)
        self.update_bond_order(*matched_nodes, new_order=2)

    self._delocal_subgraph = dict()  # clear DS
    return True


def _prune_from_ds(self, node):
    adj_nodes = self._delocal_subgraph[node]
    if not adj_nodes:
        return True  # aromatic_elements atom with no aromatic_elements bonds

    atom = self._atoms[node]
    valences = AROMATIC_VALENCES[atom.element]

    # each bond in DS has order 1.5 - we treat them as single bonds
    used_electrons = int(self._bond_counts[node] - 0.5 * len(adj_nodes))

    if atom.h_count is None:  # account for implicit Hs
        assert atom.charge == 0
        return any(used_electrons == v for v in valences)
    else:
        valence = valences[-1] - atom.charge
        used_electrons += atom.h_count
        free_electrons = valence - used_electrons
        return not ((free_electrons >= 0) and (free_electrons % 2 != 0))


def find_perfect_matching(graph: List[List[int]]) -> Optional[List[int]]:
    """Finds a perfect matching for an undirected graph (without self-loops).
    :param graph: an adjacency list representing the input graph.
    :return: a list representing a perfect matching, where j is the i-th
        symbol if nodes i and j are matched. Returns None, if the graph cannot
        be perfectly matched.
    """

    # start with a maximal matching for efficiency
    matching = _greedy_matching(graph)

    unmatched = set(i for i in range(len(graph)) if matching[i] is None)
    while unmatched:

        # find augmenting path which starts at root
        root = unmatched.pop()
        path = _find_augmenting_path(graph, root, matching)

        if path is None:
            return None
        else:
            _flip_augmenting_path(matching, path)
            unmatched.discard(path[0])
            unmatched.discard(path[-1])

    return matching


def _greedy_matching(graph):
    matching = [None] * len(graph)
    free_degrees = [len(graph[i]) for i in range(len(graph))]
    # free_degrees[i] = number of unmatched neighbors for node i

    # prioritize nodes with fewer unmatched neighbors
    node_pqueue = [(free_degrees[i], i) for i in range(len(graph))]
    heapq.heapify(node_pqueue)

    while node_pqueue:
        _, node = heapq.heappop(node_pqueue)

        if (matching[node] is not None) or (free_degrees[node] == 0):
            continue  # node cannot be matched

        # match node with first unmatched neighbor
        mate = next(i for i in graph[node] if matching[i] is None)
        matching[node] = mate
        matching[mate] = node

        for adj in itertools.chain(graph[node], graph[mate]):
            free_degrees[adj] -= 1
            if (matching[adj] is None) and (free_degrees[adj] > 0):
                heapq.heappush(node_pqueue, (free_degrees[adj], adj))

    return matching


def _find_augmenting_path(graph, root, matching):
    assert matching[root] is None

    # run modified BFS to find path from root to unmatched node
    other_end = None
    node_queue = deque([root])

    # parent BFS tree - None indicates an unvisited node
    parents = [None] * len(graph)
    parents[root] = [None, None]

    while node_queue:
        node = node_queue.popleft()

        for adj in graph[node]:
            if matching[adj] is None:  # unmatched node
                if adj != root:  # augmenting path found!
                    parents[adj] = [node, adj]
                    other_end = adj
                    break
            else:
                adj_mate = matching[adj]
                if parents[adj_mate] is None:  # adj_mate not visited
                    parents[adj_mate] = [node, adj]
                    node_queue.append(adj_mate)

        if other_end is not None:
            break  # augmenting path found!

    if other_end is None:
        return None
    else:
        path = []
        node = other_end
        while node != root:
            path.append(parents[node][1])
            path.append(parents[node][0])
            node = parents[node][0]
        return path


def _flip_augmenting_path(matching, path):
    for i in range(0, len(path), 2):
        a, b = path[i], path[i + 1]
        matching[a] = b
        matching[b] = a
