from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
from functools import partial
import matplotlib.animation as animation

from graph import Graph


class GraphCanvas(FigureCanvas):
    def __init__(self, interval=None):
        figure = plt.figure()
        super(GraphCanvas, self).__init__(figure)
        self.interval = interval
  

    def loadGraph(self, datasetName) -> Graph:
      self.g = Graph(datasetName)
      
      self.drawIncomplete()

      return self.g
      
      

    def drawComplete(self):
      self.figure.clf()
      nx.draw(self.g, pos=self.g.pos, with_labels=True)
      self.draw()

    def drawIncomplete(self):
      self.figure.clf()
      nx.draw(self.g, pos=self.g.pos, edgelist=self.g.edgesListIncomplete, with_labels=True)
      self.draw()

    def drawEmpty(self):
      self.figure.clf()
      nx.draw(self.g, pos=self.g.pos, edgelist=[], with_labels=True)
      self.draw()

    def reset(self, algo):
      self.drawIncomplete()

    def animEmpty(self):
      self.figure.clf()
      nx.draw(self.g, pos=self.g.pos, edgelist=[], node_size=100, with_labels=False)

    def animIncomplete(self):
      self.figure.clf()
      nx.draw(self.g, pos=self.g.pos, edgelist=self.g.edgesListIncomplete, with_labels=True)

    def animateMST(self, frame, mst):
      nx.draw_networkx_edges(self.g, pos=self.g.pos, edgelist=mst[0:frame])

    def animateShortestPath(self, frame, fullPath, path):
      if (len(fullPath)+1 < frame):
        self.drawIncomplete()
        nx.draw_networkx_edges(self.g, pos=self.g.pos, edgelist=path, edge_color=(1,0,0), width=2)
      else:
        nx.draw_networkx_edges(self.g, pos=self.g.pos, edgelist=fullPath[0:frame], edge_color=(1,0,0), width=2)

    def visualize(self, algo, startNode=None, endNode=None):
      print(startNode, endNode)
      if (algo == "Kruskal's"):
            self.visualizeMST(self.g.kruskals())
      elif (algo == "Prim's"):
            self.visualizeMST(self.g.prims())
      elif (algo == "Dijkstra's"):
        path, fullpath = self.g.dijkstra(startNode, endNode)
        self.visualizeShortestPath(path, fullpath)
      elif (algo == "Bellman Ford's"):
        path, fullpath = self.g.bellmanFord(startNode, endNode)
        self.visualizeShortestPath(path, fullpath)

    def visualizeMST(self, mst):
      _ = animation.FuncAnimation(self.figure, partial(self.animateMST, mst=mst), frames=len(mst)+1, interval=self.interval.value(), repeat=False, init_func=self.animEmpty)
      self.draw()

    def visualizeShortestPath(self, path, fullPath):
      _ = animation.FuncAnimation(self.figure, partial(self.animateShortestPath, fullPath=fullPath, path=path), frames=len(fullPath)+3, interval=self.interval.value(), repeat=False, init_func=self.animIncomplete)
      self.draw()
      

      

      

      