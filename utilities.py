import re
import os

def camelCaseSplit(str):
    words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)

    name = ''.join(map(lambda x: x.capitalize(), words))

    return name

def getDirList(folderName):
  root = os.getcwd()
  dest = os.path.join(root, folderName)
  
  dirList = [i for i in os.listdir(dest) if os.path.isdir(os.path.join(dest, i))]

  return dirList