import sys
from PyQt6 import QtWidgets, uic

from mainWindow import Ui_MainWindow
from graph import GraphCanvas




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.buttonClick)

        self.graphCanvas = GraphCanvas()
        self.gridLayout.addWidget(self.graphCanvas, 0, 0, 0, 0)

    def buttonClick(self):
      self.graphCanvas.createGraph()
      
        
        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()