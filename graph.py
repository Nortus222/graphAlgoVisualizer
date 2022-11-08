from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from dataParser import DataSet
INFINITY = float("inf")


class Graph(nx.Graph):
    def __init__(self, datasetName):
        super(Graph, self).__init__() 

        dataSet = DataSet(datasetName)

        self.pos = dataSet.nodePos
        self.edgesList = []
        
        # Get nodes list based on Adjacemcy Matrix -> (source, target, weight)
        n = len(self.pos)
        for i in range(n):
          for j in range(i + 1, n):
            self.edgesList.append((i, j, dataSet.adjMatrix[i, j])) # Need to add ability to create graphs without adjacency matrix (Unweighted)

        if (len(self.edgesList[0]) == 3):
          self.add_weighted_edges_from(self.edgesList)

        elif (len(self.edgesList[0]) == 2):
          self.add_edges_from(self.edgesList)
        

        self.add_nodes_from(self.pos.keys())


if __name__ == "__main__":
  g = Graph('statesCapitals')
    


