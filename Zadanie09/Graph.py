from Node import GraphNode
from Node import TreeNode

class Graph:
  @classmethod
  def setTypes(cls,types=None):
    cls.types=types or dict()

  def __init__(self,name='Graph'):
    self.name=name
    self.nodes=dict()

  def __getitem__(self,key):
    return self.nodes[key]
  def __iter__(self):
    return iter(self.nodes)

  def addNode(self,label):
    if label not in self.nodes:
      self.nodes[label]=GraphNode(label)
    return self.nodes[label]

  def getNode(self,label):
    return self.nodes[label]

  def addEdge(self,l1,l2,cost=0):
    n1=self.addNode(l1)
    n2=self.addNode(l2)
    n1.addChild(n2,cost)

  def show(self):
    keys=sorted(self.nodes.keys())
    for k in keys:
      print(k)
      for c in self.nodes[k]:
        print(f' ├{c.label} ({self.nodes[k][c]})')
  def clone(self):
    C=Graph()
    for n in self.nodes.values():
      for c in n:
        C.addEdge(n.label,c.label,n[c])
    return C

  def DFS(self,node=None):
    if type(node) is str:
      node=self.nodes[node]
    if node==None:
      node=next(iter(self.nodes.values()))
    self.visited=dict()
    return self._DFS( node )


  def _DFS(self,node):
    if node.label in self.visited:
      return True

    self.visited[node.label]=True

    cycle=False
    for c in node:
      cycle=self._DFS(c) or cycle

    del self.visited[node.label]
    return cycle

  def toImage(self):
    from importlib import util as importlib_util
    if importlib_util.find_spec('graphviz')!=None:
      from graphviz import Digraph
      import os
      dot=Digraph(format='png')
      dot.attr('graph',label=self.name)
      dot.attr('graph',labelloc='top')

      for n in self.nodes.values():
        dot.node(n.label,n.label)
        for c in n:
          dot.node(c.label,c.label)
          dot.edge(n.label,c.label,label=str(n[c]))
      dot.render('viz/'+self.name+'.gv',view=False)
    else:
      self.show()


class Tree(Graph):
  def addNode(self,label):
    if label not in self.nodes:
      self.nodes[label]=TreeNode(label)
    return self.nodes[label]


if __name__=='__main__':
  pass
