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
K5.add_nodes_from([1,2,3,4,5])
K5.add_edges_from([(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)])

K5var = nx.Graph()
K5var.add_nodes_from([1,2,3,4,5,6])
K5var.add_edges_from([(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,6),(4,5),(5,6)])

K33 = nx.Graph()
K33.add_nodes_from([1,2,3,4,5,6])
K33.add_edges_from([(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)])

K33var = nx.Graph()
K33var.add_nodes_from([1,2,3,4,5,6,7])
K33var.add_edges_from([(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,7),(6,7)])

K4 = nx.Graph()
K4.add_nodes_from([1,2,3,4])
K4.add_edges_from([(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)])

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
    
    # Now we will check Kuratowski's Theorem.
    # We will do this by checking if the graph contains a subdivision of K5 or K3,3.

    # First we will check for a subdivision of K5.

    for subgraph in combinations(graph.nodes(), 5):
        if nx.is_connected(graph.subgraph(subgraph)):
            return False
    
    # Now we will check for a subdivision of K3,3.

    for subgraph in combinations(graph.nodes(), 6):
        if nx.is_connected(graph.subgraph(subgraph)):
            if bipartite.is_bipartite(graph.subgraph(subgraph)):
                return False
            
    return True
    
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
    #graphFile = open("Graphs.txt", "r")

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

    #graphFile.close()

if __name__ == "__main__":
    main()
