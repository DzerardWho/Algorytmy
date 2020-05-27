import sys
from Graph import Graph
from Graph import Tree
from Node import GraphNode
from Node import TreeNode
from GraphParser import GraphParser


"""
  Algorytm Prima
"""
def prim(G):
  P=Tree(name='prim')
  edges=dict( zip( G.nodes.keys(),[None]*len(G.nodes) ) )
  costs=dict( zip( G.nodes.keys(),[float('inf')]*len(G.nodes) ) )
  costs['T0']=-1
  Q=dict(zip(G.nodes.keys(),[False]*len(G.nodes)))
  
  def getMin():
    v=float('inf')
    k=None
    for c in costs:
      if costs[c]<v and Q[c]==False:
        v=costs[c]
        k=c
    return k
  
  for _ in G.nodes:
    m=getMin()
    Q[m]=True

    for s,t,c in G[m].edges():
      if s is t:
        continue

      if costs[t]>c:
        costs[t]=c
        edges[t]=[s,t,c]

  for e in edges.values():
    if e==None:
      continue
    P.addEdge(*e)

  return P

"""
  Algorytm Kruskala
"""
#def kruskal_old(G):
def kruskal(G):
  K=Tree(name='kruskal')
  edges=list()
  parents=dict()
  for n in G.nodes.values():
    parents[n.label]=n.label
    for e in n.edges():
      edges.append(e)
  
  edges.sort(key=lambda e:e[2] )
  
  def getParent(l):
    if parents[l]==l:
      return l
    return getParent(parents[l])
  
  for e in edges:
    s,t,c=e
    p1=getParent(s)
    p2=getParent(t)

    if p1==p2:
      continue
    if t==p2:
      parents[t]=p1
      K.addEdge(s,t,c)
  
  return K


G=Graph(name='loaded')
parser=GraphParser(G,GraphNode)

#parser.parseLoad('graph_10_2.txt')
#parser.parseLoad('graph_20_1.txt')
parser.parseLoad(sys.stdin)

K=kruskal(G)
P=prim(G)

"""
from importlib import util as importlib_util
if importlib_util.find_spec('graphviz')!=None:
  from graphviz import Digraph
  import os

  def toGraphViz(G,file='out.gv'):

    dot=Digraph(format='png')
    dot.attr('graph',label=file)
    dot.attr('graph',labelloc='top')

    for n in G.nodes.values():
      dot.node(n.label,n.label)
      for c in n:
        dot.node(c.label,c.label)
        dot.edge(n.label,c.label,label=str(n[c]))
    dot.render('viz/'+file,view=False)



  toGraphViz(G,'loaded.gv')
  toGraphViz(K,'kruskal.gv')
  toGraphViz(P,'prim.gv')
else:
  G.show()
  K.show()
  P.show()
"""

G.toImage()
K.toImage()
P.toImage()