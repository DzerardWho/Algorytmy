class Obj:
  def __init__(self,**kw):
    self.__dict__.update()
    self.__dict__.update(kw)

  def __str__(self):
    return str(self.__dict__)
  def __repr__(self):
    return str(self.__dict__)

class Proc():
  def __init__(self,name='',cost=0,limit=0,type=0):
    self.cost=cost
    self.type=type
    self.tasks=dict()
    self.channels=dict()
    
  def addTask(self,name):
    if name not in self.tasks:
      self.tasks[name]=Obj()
    return self.tasks[name]

class GraphInfo:
  def __init__(self,procs=None,channels=None):
    self.procs=procs or dict()
    self.channels=channels or dict()
    self.edges=None

class GraphParser:
  def __init__(self,Graph=None):
    self.graph=Graph
    self.procs=dict()
    self.channels=dict()
    self.parse={'@tasks':self.parseTasks,'@proc':self.parseProc,'@times':self.parseTimes,'@cost':self.parseCost,'@comm':self.parseComm}
    self.prefix='T'

  def dummy(self):
    pass
  
  def parseTasks(self,line):
    line=line.split()
    parent=self.graph.addNode(line[0])
    line=line[2:]
    for x in line:
      t=x.replace('(',' ').replace(')','').split()
      self.graph.addEdge(parent.label,self.prefix+t[0],int(t[1]))
      
  def parseProc(self,line):
    name=f'P{self.i}'
    self.procs[name]=Proc(name,*(line.split()))
    self.i+=1

  
  def parseTimes(self,line):
    task=f'{self.prefix}{self.i}'
    line=line.split()
    for k,v in enumerate(line):
      self.procs[f'P{k}'].addTask(task).time=int(v)

    self.i+=1

  def parseCost(self,line):
    task=f'{self.prefix}{self.i}'
    line=line.split()
    for k,v in enumerate(line):
      self.procs[f'P{k}'].addTask(task).cost=int(v)
    self.i+=1

  def parseComm(self,line):
    line=line.split()
    channel=Obj(conn=int(line[1]),band=int(line[2]))
    i=0
    for j in range(3,len(line)):
      if line[j]!='0':
        self.procs[f'P{i}'].channels[line[0]]=channel
      i+=1
    self.channels[line[0]]=channel

  def parseLoad(self,filepath):
    if type(filepath) is str:
      file = open(filepath,'r')
    else:
      file=filepath
    callback=self.dummy
    for line in file:
      if line[0]=='@':
        self.i=0
        callback=self.parse[line.split()[0]]
      else:
        #callback(line.replace('\n',''))
        callback(line[:-1])

    return GraphInfo(self.procs,self.channels)

  @staticmethod
  def Load(graphCls,filepath):
    G=graphCls()
    parser=GraphParser(G)
    info=parser.parseLoad(filepath)
    info.edges=G.edges
    G.edges=None
    return (G,info)




if __name__=="__main__":
  from Graph import Graph
  from Node import GraphNode
  G=GraphParser(Graph,GraphNode)
  G.parseLoad('GRAF.10')

  G.graph.show()    
  

  


