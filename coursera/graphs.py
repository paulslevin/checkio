"""Algorithmic Thinking Project 1"""
# import unittest

EX_GRAPH0 = {0: {1, 2}, 1: set(), 2: set()}
EX_GRAPH1 = {0: {1, 4, 5}, 1: {2, 6}, 2: {3}, 3: {0}, 4: {1}, 5: {2}, 6: set()}
EX_GRAPH2 = {0: {1, 4, 5}, 1: {2, 6}, 2: {3, 7}, 3: {7}, 4: {1}, 5: {2},
             6: set(), 7: {3}, 8: {1, 2}, 9: {0, 3, 4, 5, 6, 7}}


def make_complete_graph(num_nodes):
    """Return complete graph on the given number of nodes"""
    if not num_nodes:
        return {}
    elif num_nodes == 1:
        return {0: set()}
    highest_node = num_nodes - 1
    complete_graph = {highest_node: set()}
    for node, nodes in make_complete_graph(highest_node).items():
        new_nodes = nodes | {highest_node}
        complete_graph[node] = new_nodes
        complete_graph[highest_node].add(node)
    return complete_graph


def compute_in_degrees(digraph):
    """Compute in-degrees for each node"""
    in_degrees = {node: 0 for node in digraph}
    for nodes in digraph.values():
        for receiving_node in nodes:
            in_degrees[receiving_node] += 1
    return in_degrees


def in_degree_distribution(digraph):
    """Compute degree distribution"""
    distribution = {}
    for degree in compute_in_degrees(digraph).values():
        if degree in distribution:
            distribution[degree] += 1
        else:
            distribution[degree] = 1
    return distribution


###########
# TESTING #
###########

# class TestGraphMethods(unittest.TestCase):
#     def test_complete(self):
#         self.assertEqual(make_complete_graph(0),
#                          {})
#         self.assertEqual(make_complete_graph(1),
#                          {0: set()})
#         self.assertEqual(make_complete_graph(2),
#                          {0: {1}, 1: {0}})
#         self.assertEqual(make_complete_graph(3),
#                          {0: {1, 2}, 1: {0, 2}, 2: {0, 1}})
#         self.assertEqual(make_complete_graph(4),
#                          {0: {1, 2, 3}, 1: {0, 2, 3},
#                           2: {0, 1, 3}, 3: {0, 1, 2}})
#
#     def test_in_degrees(self):
#         self.assertEqual(compute_in_degrees(EX_GRAPH0),
#                          {0: 0, 1: 1, 2: 1})
#         self.assertEqual(compute_in_degrees(EX_GRAPH1),
#                          {0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1})
#         self.assertEqual(compute_in_degrees(EX_GRAPH2),
#                          {0: 1, 1: 3, 2: 3, 3: 3, 4: 2,
#                           5: 2, 6: 2, 7: 3, 8: 0, 9: 0})
#
#     def test_distribution(self):
#         self.assertEqual(in_degree_distribution(EX_GRAPH0),
#                          {0: 1, 1: 2})
#         self.assertEqual(in_degree_distribution(EX_GRAPH1),
#                          {1: 5, 2: 2})
#         self.assertEqual(in_degree_distribution(EX_GRAPH2),
#                          {0: 2, 1: 1, 2: 3, 3: 4})
#         self.assertEqual(
#             in_degree_distribution({0: {1}, 1: {2}, 2: {3}, 3: {0}}), {1: 4})
#
#
# if __name__ == '__main__':
#     unittest.main()
