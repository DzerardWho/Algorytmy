from GraphParser import GraphParser
from Graph import Graph

import sys
import itertools as it
import argparse

"""
szeregowanie listowe zawsze wybiera zadanie znajdujące się na najdłuższej ścieżce
przykladowy program dla P0 i CHAN0
"""

def calcPath(path,proc,chan):
  cost=0
  for x in path:
    if type(x) is str:
      cost+=proc.tasks[x].time
    else:
      cost+=round(x/chan.band)
  return cost

def calcPaths(paths,proc,chan):
  costs = []
  for i in range( len(paths) ):
    costs.append([ calcPath(paths[i],proc,chan) , i ])
  return costs

def removeFromPaths(paths,l):
  for path in paths:
    try:
      i=path.index(l)
      del path[i-1:i+1]
    except:
      pass
  

arguments = argparse.ArgumentParser()
arguments.add_argument("-p",help="Numer zasobu do wykorzystania[domyślnie 0]",default='0',type=int)
arguments.add_argument("-c",help="Numer kanalu do transmisji[domyślnie 0]",default='0',type=int)
arguments.add_argument("file",help="plik do wczytania",type=str)
args=arguments.parse_args()


PROC = f'P{args.p}'
CHAN = f'CHAN{args.c}'

FILE=args.file

graph,info=GraphParser.Load(Graph,FILE)
graph.name='Listowe'



paths = graph.paths(graph['T0'])

new_paths=[]
for path in paths:
  p1,p2=it.tee(path,2)
  next(p2,None)
  new_paths.append( [0,'T0']+list( it.chain.from_iterable( (graph.getCost(k,v),v) for k,v in zip(p1,p2)) ) )

paths = new_paths
del new_paths

done = []
costs = calcPaths(paths,info.procs[PROC],info.channels[CHAN])

while len(done)<len(graph.nodes):
  costs.sort(key = lambda x:-x[0])
  critical_path = paths[costs[0][1]]
  if len(critical_path)<1:
    break
  to_remove = critical_path[1]
  done.append(to_remove)
  removeFromPaths(paths,to_remove)
  costs = calcPaths(paths,info.procs[PROC],info.channels[CHAN])

print(done)
