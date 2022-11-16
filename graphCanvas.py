from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
from functools import partial
import matplotlib.animation as animation

from graph import Graph


class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None):
        figure = plt.figure()
        super(GraphCanvas, self).__init__(figure)

    def loadGraph(self, datasetName):
      self.g = Graph(datasetName)
      
      self.drawIncomplete()
      
      

    def drawComplete(self):
      self.figure.clf()
      nx.draw(self.g, pos=self.g.pos, with_labels=True)
      self.draw()

    def drawIncomplete(self):
      self.figure.clf()
      nx.draw_networkx(self.g, pos=self.g.pos, edgelist=self.g.edgesListIncomplete, with_labels=True)
      self.draw()

    def drawEmpty(self):
      self.figure.clf()
      nx.draw_networkx(self.g, pos=self.g.pos, edgelist=[], with_labels=True)
      self.draw()

    def reset(self, algo):
        if (algo == "Kruskal's" or algo == "Prim's"):
            self.drawIncomplete()

    def mst(self, algo):
        if (algo == "Kruskal's"):
            mst = self.g.kruskals()
        elif (algo == "Prim's"):
            mst = self.g.prims()
        self.drawMST(mst=mst)

    def drawMST(self, mst):
      self.figure.clf()
      nx.draw_networkx(self.g, pos=self.g.pos, edgelist=mst, with_labels=True)
      self.draw()

    def animEmpty(self):
      self.figure.clf()
      nx.draw_networkx(self.g, pos=self.g.pos, edgelist=[], node_size=100, with_labels=False)

    def animate(self, frame, mst):
      nx.draw_networkx_edges(self.g, pos=self.g.pos, edgelist=mst[0:frame])

    def visualize(self, algo):
      if (algo == "Kruskal's"):
            mst = self.g.kruskals()
      elif (algo == "Prim's"):
            mst = self.g.prims()

      _ = animation.FuncAnimation(self.figure, partial(self.animate, mst=mst), frames=len(mst)+1, interval=400, repeat=False, init_func=self.animEmpty)
      self.draw()

      

      