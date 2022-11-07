from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
INFINITY = float("inf")

# node list , edgelist, 
class Graph:
    def __init__(self,filename):
        # in file from_node, to_node, weight
        g = nx.Graph()
        edge_list = []
        with open(filename) as fhandle:
            for line in fhandle:
                edge_from, edge_to,weight,*_= line.strip().split(" ")
                edge_list.append((edge_from,edge_to,weight))
        g.add_edges_from(edge_list)
        self.nodes = set() # set of all unique nodes
        for edge in edge_list:
            self.nodes.update([edge[0], edge[1]])
        g.add_nodes_from(self.nodes)
        #dict mapping each node to an unordered set of (neighbor,dist) tuples
        self.adjacency_list = {node: set() for node in self.nodes}
        for edge in edge_list:
            self.adjacency_list[edge[0]].add((edge[1], edge[2]))
    def shortest_path(self,start_node,end_node):
        
        #all nodes are initially unvisited
        unvisited_nodes = self.nodes.copy()

        #create a dictionary of each node's distance from start node
        # update each node's distance when a shorter path found
        distance_from_start = {node: (0 if node == start_node else INFINITY)
                               for node in self.nodes}
        #initialize prev node, the dict that maps each node to the node it was visited from
        #when the shortest path to it was found.
        
        previous_node = {node: Node for node in self.nodes}

        while unvisited_nodes:
            #set current_node to the unvisited_node with shortest dist calculated
            current_node = min(unvisited_nodes,key=lambda node: distance_from_start[node])
            unvisited_nodes.remove(current_node)
            #if current_node's distance is INFINITY, the remaing unvisited nodes are not
            # connected to start_node, done
            if distance_from_start[current_node] == INFINITY:
                break
            #for each neighbor of current_node, check whether the total dist to the neighbor
            #via current_node is shorter than the dist we currently have for that node.
            # if it is , update the neighbor's values for distance_from_start and previous_node
            for neighbor,distance in self.adjacency_list[current_node]:
                new_path = distance_from_start[current_node] + distance
                if new_path < distance_from_start[neighbor]:
                    distance_from_start[neighbor] = new_path
                    previous_node[neighbor] = current_node
            if current_node == end_node:
                break # we have visited the dest node, done here
            
        # iterate through the nodes from end_node back to start_node to generate the path
        # use deque() because of performance O(1)
        path = deque()
        current_node = end_node
        while previous_node[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_node[current_node]
        path.appendleft[start_node]

        return path
if __name__ == "__main__":
        g = Graph("input_file.txt")
        path = shortest_path(g,start_node,end_node)
##        pos = nx.spring_layout(g)
##        nx.draw_networkx_nodes(g, pos, nodelist=g.nodes,
##                       node_color='b', node_size=600)
##        nx.draw_networkx_edges(g, pos, edgelist=g.edge_list)
##        nx.draw_networkx_edges(g, pos, edgelist=path,
##                       width=8, alpha=0.5, edge_color='r')
##        plt.show()




    
