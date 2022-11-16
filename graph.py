from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from dataParser import DataSet
INFINITY = float("inf")


class Graph(nx.Graph):
    def __init__(self, datasetName):
        super(Graph, self).__init__() 

        dataSet = DataSet(datasetName)

        self.pos = dataSet.nodePos
        self.edgesList = []
        self.edgesListIncomplete = []
        self.adjMatrix = dataSet.adjMatrix
        
        # Get nodes list based on Adjacemcy Matrix -> (source, target, weight)
        n = len(self.pos)
        for i in range(n):
          counter = 0
          for j in range(i + 1, n):
            self.edgesList.append((i, j, dataSet.adjMatrix[i, j])) 
            if (random.choice([0, 1]) == 0 and counter < 4):
              counter += 1
              self.edgesListIncomplete.append((i, j, dataSet.adjMatrix[i, j]))

        if (len(self.edgesList[0]) == 3):
          self.add_weighted_edges_from(self.edgesList)

        elif (len(self.edgesList[0]) == 2):
          self.add_edges_from(self.edgesList)
        

        self.add_nodes_from(self.pos.keys())

    # union find
    def find(self, root, i):
        if root[i] == i:
            return i
        return self.find(root, root[i])

    def union(self, root, rank, x, y):
        xroot = self.find(root, x)
        yroot = self.find(root, y)
        if rank[xroot] < rank[yroot]:
            root[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            root[yroot] = xroot
        else:
            root[yroot] = xroot
            rank[xroot] += 1


    def kruskals(self):
        # initialize an empty MST list
        result = []
        # initialize i, the iteration and e, the edges added
        i, e  = 0, 0
        # sort the graph based on edge weights
        edges = sorted(self.edgesList, key = lambda item: item[2])
        # initialize root, which keeps track of the MST
        # and the rank, which keeps track of where each node belongs
        root = []
        rank = []
        for node in range(self.number_of_nodes()):
            root.append(node)
            rank.append(0)
  
        # while we haven't yet added each edge
        # increment iterator and run the union find algorithm
        while e < self.number_of_nodes() - 1:
            u, v, w = edges[i]
            i = i + 1
            x = self.find(root, u)
            y = self.find(root, v)
            
            if x != y:
                e = e + 1
                result.append((u, v, w))
                self.union(root, rank, x, y)
  
        return result

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.number_of_nodes()):
            print(node, "\t\t", dist[node])

    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.number_of_nodes()):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
 
        dist = [1e7] * self.number_of_nodes()
        dist[src] = 0
        sptSet = [False] * self.number_of_nodes()
 
        for _ in range(self.number_of_nodes()):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.number_of_nodes()):
                if (self.adjMatrix[u][v] > 0 and
                   sptSet[v] == False and
                   dist[v] > dist[u] + self.adjMatrix[u][v]):
                    dist[v] = dist[u] + self.adjMatrix[u][v]
 
        self.printSolution(dist)
        print(dist)

    # prim's algo, graph is represented as an v by v adjacency list
    def prims(self):
        # used to pick minimum weight edge
        key = [1e7] * self.number_of_nodes()
        # used to store MST
        parent = [1e7] * self.number_of_nodes()
        result = []
        # pick a random vertex, ie 0
        key[0] = 0
        # create list for t/f if a node is connected to the MST
        mstSet = [False] * self.number_of_nodes()
          # set the first node to the root (ie have a parent of -1)
        parent[0] = -1
  
        for _ in range(self.number_of_nodes()):
            # 1) pick the minimum distance vertex from the current key
            # from the set of points not yet in the MST
            u = self.minDistance(key, mstSet)
            # 2) add the new vertex to the MST
            mstSet[u] = True
  
            # loop through the vertices to update the ones that are still
            # not in the MST
            for v in range(self.number_of_nodes()):
                # if the edge from the newly added vertex (v) exists,
                # the vertex hasn't been added to the MST, and
                # the new vertex's distance to the graph is greater than the distance
                # stored in the initial graph, update the "key" value to the
                # distance initially given and update the parent of
                # of the vertex (v) to the newly added vertex (u)
                if self.adjMatrix[u][v] > 0 and mstSet[v] == False and key[v] > self.adjMatrix[u][v]:
                    key[v] = self.adjMatrix[u][v]
                    parent[v] = u
                    
        for i in range(1, self.number_of_nodes()):
          result.append((i, parent[i], self.adjMatrix[i][parent[i]]))
        
        return result


if __name__ == "__main__":
  g = Graph('statesCapitals')
    


