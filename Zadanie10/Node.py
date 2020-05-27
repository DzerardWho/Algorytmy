class GraphNode():
  def __init__(self,label,data=None):
    self.label=label
    self.data=data
    self._edges=dict()
    
  def __hash__(self):
    return hash(self.label)

  def addChild(self,node,cost=0):
    self._edges[node]=cost
    node.addParent(self)

  def addParent(self,node):
    pass




  def __iter__(self):
    return iter(self._edges)

  def __getitem__(self,key):
    return self._edges[key]

  def edges(self):
    for c in self._edges:
      yield [self.label,c.label,self._edges[c]]

  #def __setitem__(self,key,value):
  #  return self.edges[key]

  def __delitem__(self,key):
    del self._edges[key]



class TreeNode(GraphNode):
  def __init__(self,label,data=None):
    super().__init__(label,data)
    self.parent=None
  def addChild(self,node,cost=0):
    if node.parent==None:
      self._edges[node]=cost
      node.addParent(self)
    else:
      print('[WARN] Node already had parent')

  def addParent(self,node):
    if self.parent==None:
      self.parent=node
    else:
      print('[WARN] Node already had parent')
    