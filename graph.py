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


if __name__ == "__main__":
  g = Graph('statesCapitals')
    


