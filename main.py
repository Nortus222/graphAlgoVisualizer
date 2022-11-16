import sys
from PyQt6 import QtWidgets, uic

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from mainWindow import Ui_MainWindow
from graphCanvas import GraphCanvas
from utilities import *


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

    def cbGraphSelectionValueChanged(self, i):
        self.graphCanvas.loadGraph(self.cbGraphSelection.currentText())

    def loadcbGraphSelection(self, folderName):
        cbItems = getDirList(folderName)
        
        self.cbGraphSelection.addItems(cbItems)
        self.cbGraphSelection.currentIndexChanged.connect(self.cbGraphSelectionValueChanged)
        self.cbGraphSelection.setCurrentText('statesCapitals')

        

    def buttonClick(self):
      self.graphCanvas.visualizeMST()
      
        
        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()