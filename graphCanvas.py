from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx

from graph import Graph


class GraphCanvas(FigureCanvas):

    def __init__(self, parent=None):
        figure = plt.figure()
        super(GraphCanvas, self).__init__(figure)

    def loadGraph(self, datasetName):
      self.figure.clf()
      g = Graph(datasetName)
      
    #   nx.draw(g, pos=g.pos, with_labels=True)
      nx.draw_networkx_nodes(g, pos=g.pos)
      self.draw()
      
      