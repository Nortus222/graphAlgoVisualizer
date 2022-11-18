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

    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = INFINITY
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.number_of_nodes()):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index

    def dijkstra(self,start_node,end_node):
        print(self.edgesListIncomplete)
        
        #all nodes are initially unvisited
        unvisited_nodes = list(self.nodes()._nodes.keys())

        #create a dictionary of each node's distance from start node
        # update each node's distance when a shorter path found
        distance_from_start = {node: (0 if node == start_node else INFINITY)
                               for node in self.nodes}

        #initialize prev node, the dict that maps each node to the node it was visited from
        #when the shortest path to it was found.
        previous_node = {node: None for node in self.nodes}

        fullPath = []
        
        while unvisited_nodes:
            
            #set current_node to the unvisited_node with shortest dist calculated
            current_node = min(unvisited_nodes,key=lambda node: distance_from_start[node])
            print(current_node)
            unvisited_nodes.remove(current_node)

            #if current_node's distance is INFINITY, the remaing unvisited nodes are not
            # connected to start_node, done
            if distance_from_start[current_node] == INFINITY:
                break
            
            # Questionable        
            if current_node == end_node:
                break # we have visited the dest node, done here

            #for each neighbor of current_node, check whether the total dist to the neighbor
            #via current_node is shorter than the dist we currently have for that node.
            # if it is , update the neighbor's values for distance_from_start and previous_node
            for src, neighbor, distance in [edge for edge in self.edgesListIncomplete if edge[0] == current_node]:
                new_path = distance_from_start[current_node] + distance
                print((src, neighbor))
                fullPath.append((src, neighbor))
                if new_path < distance_from_start[neighbor]:
                    distance_from_start[neighbor] = new_path
                    previous_node[neighbor] = current_node

        # iterate through the nodes from end_node back to start_node to generate the path
        # use deque() because of performance O(1)
        path = deque()
        current_node = end_node
        while previous_node[current_node] is not None:
            path.appendleft((previous_node[current_node],current_node))
            current_node = previous_node[current_node]
        
        return list(path), fullPath

    # prim's algo, graph is represented as an v by v adjacency list
    def prims(self):
        # used to pick minimum weight edge
        key = [INFINITY] * self.number_of_nodes()
        # used to store MST
        parent = [INFINITY] * self.number_of_nodes()
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

    def bellmanFord(self, src, end_node):

        print(self.edgesListIncomplete)

        # Step 1: fill the distance array and predecessor array
        dist = [INFINITY] * self.number_of_nodes()
        # Mark the source vertex
        dist[src] = 0

        #initialize prev node, the dict that maps each node to the node it was visited from
        #when the shortest path to it was found.
        previous_node = {node: None for node in self.nodes}

        # Step 2: relax edges |V| - 1 times
        for _ in range(self.number_of_nodes() - 1):
            for s, d, w in self.edgesListIncomplete:
                if dist[s] != INFINITY and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w
                    previous_node[d] = s

        # Step 3: detect negative cycle
        # if value changes then we have a negative cycle in the graph
        # and we cannot find the shortest distances
        for s, d, w in self.edgesListIncomplete:
            if dist[s] != INFINITY and dist[s] + w < dist[d]:
                print("Graph contains negative weight cycle")
                return

        # iterate through the nodes from end_node back to start_node to generate the path
        # use deque() because of performance O(1)
        path = deque()
        current_node = end_node
        while previous_node[current_node] is not None:
            path.appendleft((previous_node[current_node],current_node))
            current_node = previous_node[current_node]

        return list(path), self.edgesListIncomplete
        
