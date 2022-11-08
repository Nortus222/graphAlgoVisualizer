import numpy as np

class DataSet:
  def __init__(self, dataSetName):
    self.folder = "dataSets"
    self.dsName = dataSetName
    self.fullPath = "%s/%s" %(self.folder, self.dsName)
    self.nodePos = {} #positions for nodes -> {node: (x, y)}
    self.adjMatrix = np.loadtxt("%s/%s_ajm.txt" %(self.fullPath, self.dsName))

    counter = 0
    for node in np.loadtxt("%s/%s_xy.txt" %(self.fullPath, self.dsName)):
      self.nodePos[counter] = node
      counter += 1


  



    