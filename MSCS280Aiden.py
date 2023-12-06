# Stephen, Aiden, and Nathaen
# Dr. Laura Schmidt
# MSCS 280
# 12/6/23
#
# This program will determine whether or not a graph is planar, and if it is, it will draw it.
# For sake of simplicity, we will use the networkx library.
# Even though this library already has a function to determine if a graph is planar, we will try to write our own.

import networkx as nx
from networkx.algorithms import bipartite
# import planarity testing library
from networkx.algorithms.planarity import check_planarity
from itertools import combinations, product
import matplotlib.pyplot as plt
import random

# First we will create K5, K3,3, and K4 as graphs to test against.
K5 = nx.Graph()
K5.add_nodes_from([1, 2, 3, 4, 5])
K5.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)])

K5var = nx.Graph()
K5var.add_nodes_from([1, 2, 3, 4, 5, 6])
K5var.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 6), (4, 5), (5, 6)])

K33 = nx.Graph()
K33.add_nodes_from([1, 2, 3, 4, 5, 6])
K33.add_edges_from([(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)])

K33var = nx.Graph()
K33var.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
K33var.add_edges_from([(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 7), (6, 7)])

K4 = nx.Graph()
K4.add_nodes_from([1, 2, 3, 4])
K4.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])


def drawGraph(graph):
    # This function will draw the graph using the networkx library.
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()



#checks to see if a graph has a subgraph isomorphic to k5
def has_k5_subgraph(graph):
    # ensure graph is of at least order 5
    if len(graph) < 5:
        return False

    #iterate through all combinations
    for subset in combinations(graph.nodes(), 5):
        # Create a subgraph induced by the current subset
        subgraph = graph.subgraph(subset)

        # checks if is isomorphic
        if nx.is_isomorphic(subgraph, nx.complete_graph(5)):
            return True

    return False


#checks to see if a graph has a subgraph isomorphic to k33
def has_k33_subgraph(graph):

    if len(graph) < 6:
        return False

    for subset in combinations(graph.nodes(), 6):
        subgraph = graph.subgraph(subset)

        if nx.is_bipartite(subgraph) and len(subgraph) == 6:
            partitions = bipartite.sets(subgraph)
            if len(partitions[0]) == 3 and len(partitions[1]) == 3:
                return True

    return False


def has_nonplanar_minor(graph):

    if has_k5_subgraph(graph) or has_k33_subgraph(graph):
        return True
    copy_graph = graph
    k5_minor_found = False
    k33_minor_found = False

    while True:
        #all degree 2 vertices in the graph
        degree_2_vertices = [v for v in copy_graph.nodes() if copy_graph.degree(v) == 2]

        if not degree_2_vertices:
            break

        #for each degree 2 vertex we gather its neighbors and begins contracting edges if its neighbors are also degree 2
        for v in degree_2_vertices:
            neighbors = list(copy_graph.neighbors(v))

            if len(neighbors) == 2:
                u, w = neighbors
                contracted_graph = nx.contracted_edge(copy_graph, (u, v), self_loops=False)
                if k5_minor_found and  k33_minor_found:
                    break;
                elif has_k5_subgraph(contracted_graph) and not k5_minor_found:
                    k5_minor_found = True
                elif has_k33_subgraph(contracted_graph) and not k33_minor_found:
                    k33_minor_found = True
                else:
                    copy_graph = contracted_graph

        if k5_minor_found or k33_minor_found:
            return True

    return False


def isPlanar(graph):
    # This function will determine if a graph is planar by using Kuratowski's Theorem.
    # Kuratowski's Theorem states that a graph is planar if and only if it does not contain a subgraph that is a subdivision of K5 or K3,3.
    # Another point to consider is that of Theorem 10.4 which states: If G is a graph of order n >= 5 and size m such that m > 3n - 6, then G is nonplanar.
    # Its Corollary 10.5 states: Every planar graph has a vertex of degree 5 or less.
    # We will use these theorems to determine if a graph is planar.

    # First we will check Theorem 10.4

    for node in graph.nodes:
        if graph.degree(node) == 0:
            graph.remove_node(node)

    n = graph.number_of_nodes()
    m = graph.number_of_edges()

    if m > (3 * n - 6):
        return False

    # Now we will check Theorem 10.5.
    # We just need 1 vertex of degree 5 or less.

    vertOfDegreeLEQ5 = False
    for node in graph.nodes():
        if graph.degree(node) <= 5:
            vertOfDegreeLEQ5 = True
            break

    if not vertOfDegreeLEQ5:
        return False

    # Now we will check Kuratowski's Theorem.
    # We will do this by checking if the graph contains a subdivision of K5 or K3,3.
    return not has_nonplanar_minor(graph)



def graphFromAdjacency(adjacency_matrix):
    # This function will create a graph from an adjacency matrix.
    # The adjacency matrix will be a list of lists.
    # The adjacency matrix will be a square matrix.
    # The adjacency matrix will be symmetric.

    nodes = []
    edges = []

    for i in range(len(adjacency_matrix)):
        nodes.append(i + 1)
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                edges.append((i + 1, j + 1))

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph


def randomAdjacencyMatrix(n):
    # This function will create a random adjacency matrix of size n.
    # The adjacency matrix will be a list of lists.
    # The adjacency matrix will be a square matrix.
    # The adjacency matrix will be symmetric.

    # First we will create an empty adjacency matrix.

    adjacency_matrix = []

    for i in range(n):
        adjacency_matrix.append([])
        for j in range(n):
            adjacency_matrix[i].append(0)

    # Now we will randomly fill in the adjacency matrix.

    for i in range(n):
        for j in range(i + 1, n):
            adjacency_matrix[i][j] = adjacency_matrix[j][i] = random.randint(0, 1)

    return adjacency_matrix


def main():
    # graphFile = open("Graphs.txt", "r")

    # TODO: Read in the graphs from the file and determine if they are planar.
    # drawGraph(K5)
    # drawGraph(K5var)
    # drawGraph(K33)
    # drawGraph(K33var)
    # drawGraph(K4)
    # print("K5 is planar: " + str(isPlanar(K5)))
    # print("K5var is planar: " + str(isPlanar(K5var)))
    # print("K33 is planar: " + str(isPlanar(K33)))
    # print("K33var is planar: " + str(isPlanar(K33var)))
    # print("K4 is planar: " + str(isPlanar(K4)))

    for i in range(3):
        # Create random graphs, display them, and determine if they are planar.
        randint = random.randint(5, 10)
        randomGraph = graphFromAdjacency(randomAdjacencyMatrix(randint))
        print("My random graph is planar: " + str(isPlanar(randomGraph)))
        drawGraph(randomGraph)

    # graphFile.close()


if __name__ == "__main__":
    main()
