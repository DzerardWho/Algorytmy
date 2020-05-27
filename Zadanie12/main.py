from GraphParser import GraphParser
from Graph import Graph

import sys
import itertools as it
import argparse

arguments = argparse.ArgumentParser()
arguments.add_argument("file",help="plik do wczytania",type=str)
args=arguments.parse_args()

graph,info = GraphParser.Load(Graph,args.file)
graph.name=args.file


"""

def show(name,a):
  print(name)
  for k in a:
    print(*[f'{x: 4}' for x in a[k].values()])
  print()

prev={}
for v1 in graph.nodes.values():
  prev[v1.label]={}
  for v2 in graph.nodes.values():

    if v2 in v1._edges:
      print(v1.label,v2.label,v1[v2])
      prev[v1.label][v2.label]=v1[v2]
    else:
      prev[v1.label][v2.label]=float('inf')

  prev[v1.label][v1.label]=0




import copy

#show('START',prev)

for current in graph.nodes:
  next={}
  for v1 in graph.nodes:
    next[v1]={}
    for v2 in graph.nodes:
      if current in (v1,v2):
        next[v1][v2]=prev[v1][v2]
      else:
        tmp=prev[v1][current]+prev[current][v2]
        if tmp<prev[v1][v2]:
          next[v1][v2]=tmp
        else:
          next[v1][v2]=prev[v1][v2]

  prev=copy.deepcopy(next)
  #show(current,next)


"""


#show('START',prev)

def show(name,a):
  print(name)
  for k in a:
    print(*[f'{x: 4}' for x in a[k].values()])
  print()

import copy
prev={}

for v1 in range(len(graph.nodes)):
  prev[v1]={}
  for v2 in range(len(graph.nodes)):
    if graph[f'T{v2}'] in graph[f'T{v1}']._edges:
      prev[v1][v2]=graph[f'T{v1}'][graph[f'T{v2}']]
    else:
      prev[v1][v2]=float('inf')

  prev[v1][v1]=0


for current in range(len(graph.nodes)):
  next={}
  for v1 in range(len(graph.nodes)):
    next[v1]={}
    for v2 in range(len(graph.nodes)):
      if current in (v1,v2):
        next[v1][v2]=prev[v1][v2]
      else:
        tmp=prev[v1][current]+prev[current][v2]
        if tmp<prev[v1][v2]:
          next[v1][v2]=tmp
        else:
          next[v1][v2]=prev[v1][v2]

  prev=copy.deepcopy(next)
  show(f'T{current}',next)
  