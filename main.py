import sys
from PyQt6 import QtWidgets, uic

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from mainWindowTest import Ui_MainWindow
from graphCanvas import GraphCanvas
from qStyle import style
from utilities import *

ALGORITHMS = ["Kruskal's", "Prim's", "Dijkstra's", "Bellman Ford's"]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.dataSetsFolder = 'dataSets'

        self.graphCanvas = GraphCanvas(interval=self.horizontalSlider)
        self.canvasGrid.addWidget(self.graphCanvas, 0, 0, 0, 0)

        toolbar = NavigationToolbar(self.graphCanvas, self)
        self.canvasGrid.addWidget(toolbar, 1, 0)

        self.centralwidget.setStyleSheet(style)

        self.pushButton.clicked.connect(self.buttonClick)

        self.sliderValueChanged()
        self.horizontalSlider.valueChanged.connect(self.sliderValueChanged)
        
        self.loadcbGraphSelection(self.dataSetsFolder)
        self.loadcbAlgorithms()

    def sliderValueChanged(self):
        self.animationSpeed.setText("%.2f s"%(self.horizontalSlider.value() / 1000))

    def cbGraphSelectionValueChanged(self, i):
        graph = self.graphCanvas.loadGraph(self.cbGraphSelection.currentText())
        self.adjustNodeBox(graph)

    def loadcbGraphSelection(self, folderName):
        cbItems = getDirList(folderName)
        
        self.cbGraphSelection.addItems(cbItems)
        self.cbGraphSelection.currentIndexChanged.connect(self.cbGraphSelectionValueChanged)
        self.cbGraphSelection.setCurrentText('statesCapitals')

    def cbAlgorirthmsValueChanged(self):
        self.graphCanvas.reset(self.cboAlgo.currentText())

        self.nodesSelectionBox.setVisible(ALGORITHMS.index(self.cboAlgo.currentText()) > 1)

    def loadcbAlgorithms(self):
        self.cboAlgo.currentIndexChanged.connect(self.cbAlgorirthmsValueChanged)
        self.cboAlgo.addItems(ALGORITHMS)

    def buttonClick(self):
        self.graphCanvas.visualize(self.cboAlgo.currentText(), self.startNodeBox.value(), self.endNodeBox.value())

    def adjustNodeBox(self, graph):
        self.endNodeBox.setMaximum(graph.number_of_nodes()-1)
        self.startNodeBox.setMaximum(graph.number_of_nodes()-1)
        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()