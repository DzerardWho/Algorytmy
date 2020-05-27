from GraphParser import GraphParser
from Graph import Graph

import sys
import itertools as it
import argparse

arguments = argparse.ArgumentParser()
arguments.add_argument("-s",help="Numer węzła początkowego[domyślnie 0]",default='0',type=int)
arguments.add_argument("file",help="plik do wczytania",type=str)
args=arguments.parse_args()

SRC=f'T{args.s}'
FILE=args.file

graph,info = GraphParser.Load(Graph,FILE)

costs = { k:float('inf') for k in graph }
done = {}
paths = { k:[] for k in graph }

paths[SRC].append(SRC)
costs[SRC] = 0

while len(costs)>0:

  parent = min(costs,key=costs.get)
  cost = costs.pop(parent)
  done[parent]=cost
  for s,t,c in graph[parent].edges():
    try:
      if (cost+c)<costs[t]:
        costs[t]=cost+c
        paths[t]=paths[parent] + [t]
    except:
      pass


leaf_ended=[ (done[l],paths[l])  for l in graph.nodes if len(graph.nodes[l]._edges)<1]


m=min(leaf_ended,key=lambda x:x[0])

print("Cost:",m[0])
print("Path:",  '->'.join(m[1])  )

#graph.toImage()
