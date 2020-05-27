import re
class GraphParser:
  def __init__(self,Graph=None,Node=None):
    self.graph=Graph
    self.Node=Node
    self.parse={'@tasks':self.parseTasks,'@proc':self.parseProc,'@times':self.parseTimes,'@cost':self.parseCost,'@comm':self.parseComm}

  def dummy(self):
    pass
  
  def parseTasks(self,line): # CHANGE 2020-05-01: added int():
    line=line.split()
    parent=self.graph.addNode(line[0])
    line=line[2:]
    for x in line:
      tmp = re.match('([0-9]+)\(([0-9]+)\)',x)
      label='T'+tmp.group(1)
      cost=int(tmp.group(2))
      parent.addChild( self.graph.addNode( label ) , cost )

  
  def parseProc(self,line):
    pass

  
  def parseTimes(self,line):
    pass


  def parseCost(self,line):
    pass


  def parseComm(self,line):
    pass


  def parseLoad(self,filepath):
    if type(filepath) is str:
      file = open(filepath,'r')
    else:
      file=filepath
    callback=self.dummy
    for line in file:
      if line[0]=='@':
        callback=self.parse[line.split()[0]]
      else:
        callback(line.replace('\n',''))


if __name__=="__main__":
  from Graph import Graph
  from Node import GraphNode
  G=GraphParser(Graph,GraphNode)
  G.parseLoad('GRAF.10')

  G.graph.show()    
  

  


