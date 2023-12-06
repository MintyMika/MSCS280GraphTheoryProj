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
import itertools as it
import matplotlib.pyplot as plt
import random

# First we will create K5, K3,3, and K4 as graphs to test against.
K5 = nx.Graph()
K5.add_nodes_from([1,2,3,4,5])
K5.add_edges_from([(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)])

K33 = nx.Graph()
K33.add_nodes_from([1,2,3,4,5,6])
K33.add_edges_from([(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)])


def drawGraph(graph):
    # This function will draw the graph using the networkx library.
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()

def isPlanar(graph):
    # This function will determine if a graph is planar by using Kuratowski's Theorem.
    # Kuratowski's Theorem states that a graph is planar if and only if it does not contain a subgraph that is a subdivision of K5 or K3,3.
    # Another point to consider is that of Theorem 10.4 which states: If G is a graph of order n >= 5 and size m such that m > 3n - 6, then G is nonplanar.
    # Its Corollary 10.5 states: Every planar graph has a vertex of degree 5 or less.
    # We will use these theorems to determine if a graph is planar.

    # First we will check Theorem 10.4.

    # Make sure the graph is not disconnected.
    if not nx.is_connected(graph):
        return 'Graph is not connected'

    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    
    if m > 3*n - 6:
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

    """
    function checks if graph G has K(5) or K(3,3) as minors,
    returns True /False on planarity and nodes of "bad_minor"
    """
    result=True
    bad_minor=[]
    n=len(graph.nodes())
    if n>5:
        for subnodes in it.combinations(graph.nodes(),6):
            subG=graph.subgraph(subnodes)
            if bipartite.is_bipartite(subG):# check if the graph G has a subgraph K(3,3)
                X, Y = bipartite.sets(subG)

                if len(X)==3: 
                    result=False
                    # return false as well as each partite set
                    bad_minor=[X,Y]
    if n>4 and result:
        for subnodes in it.combinations(graph.nodes(),5):
            subG=graph.subgraph(subnodes)
            if len(subG.edges())==10:# check if the graph G has a subgraph K(5)
                result=False
                bad_minor=subnodes
    return result,bad_minor


def graphFromAdjacency(adjacency_matrix):
    # This function will create a graph from an adjacency matrix.
    # The adjacency matrix will be a list of lists.
    # The adjacency matrix will be a square matrix.
    # The adjacency matrix will be symmetric.

    nodes = []
    edges = []

    for i in range(len(adjacency_matrix)):
        nodes.append(i+1)
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                edges.append((i+1, j+1))
    
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
        for j in range(i+1, n):
            adjacency_matrix[i][j] = adjacency_matrix[j][i] = random.randint(0,1)
    
    return adjacency_matrix
    

def main():

    for i in range(3):
        # Create random graphs, display them, and determine if they are planar.
        randint = random.randint(5, 10)
        randomGraph = graphFromAdjacency(randomAdjacencyMatrix(randint))
        print("My random graph is planar: " + str(isPlanar(randomGraph)))
        drawGraph(randomGraph)

    print("K5 is planar: " + str(isPlanar(K5)))

if __name__ == "__main__":
    main()
