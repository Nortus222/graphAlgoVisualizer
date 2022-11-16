import sys
from PyQt6 import QtWidgets, uic

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from mainWindow import Ui_MainWindow
from graphCanvas import GraphCanvas
from utilities import *

ALGORITHMS = ["Kruskal's", "Prim's", "Dijkstra's"]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.dataSetsFolder = 'dataSets'

        self.graphCanvas = GraphCanvas()
        self.gridLayout.addWidget(self.graphCanvas, 0, 0, 0, 0)

        toolbar = NavigationToolbar(self.graphCanvas, self)
        self.gridLayout.addWidget(toolbar, 1, 0)

        self.pushButton.clicked.connect(self.buttonClick)
        
        self.loadcbGraphSelection(self.dataSetsFolder)
        self.loadcbAlgorithms()

    def cbGraphSelectionValueChanged(self, i):
        self.graphCanvas.loadGraph(self.cbGraphSelection.currentText())

    def loadcbGraphSelection(self, folderName):
        cbItems = getDirList(folderName)
        
        self.cbGraphSelection.addItems(cbItems)
        self.cbGraphSelection.currentIndexChanged.connect(self.cbGraphSelectionValueChanged)
        self.cbGraphSelection.setCurrentText('statesCapitals')

    def cbAlgorirthmsValueChanged(self):
        self.graphCanvas.reset(self.cboAlgo.currentText())

    def loadcbAlgorithms(self):
        self.cboAlgo.addItems(ALGORITHMS)
        self.cboAlgo.currentIndexChanged.connect(self.cbAlgorirthmsValueChanged)

    def buttonClick(self):
        self.graphCanvas.visualize(self.cboAlgo.currentText())
    #   self.graphCanvas.visualizeMST()
      
        
        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()