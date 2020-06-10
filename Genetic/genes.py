from __future__ import annotations
import numpy as np
from typing import Any, Callable, Dict, List
from copy import deepcopy
import sys

import numpy as np

sys.path.append(".")

from Graph import Graph, Node as GNode
from TaskData import TaskData, Process
from decisionTree import TaskImplementation


"""
Dla jednostek obliczeniowych:

  1. Najtańsza implementacja zadań – zadania są przydzielane do zasobów, dla których koszt ich
  wykonania jest najmniejszy,

  2. Najszybsza implementacja zadań – zadania są przydzielane do zasobów, dla których czas ich
  wykonania jest najmniejszy,

  3. Najmniejsze t*k – zadania są przydzielane do zasobów, dla których iloczyn czasu i kosztu ich
  wykonania jest najmniejszy

  4. Tak samo jak dla poprzednika – zadania są przydzielane do tych samych zasobów co ich
  poprzedniki,

  5. Najmniej obciążone zasoby – zadania są przydzielane sekwencyjnie do zasobów wykonujących
  najmniej zadań.

"""

class Genes:
  """
    helpers
  """
  @staticmethod
  def isAvailable( p: Process ,instances: Iterable[ProcessInstance] ):
    return len(instances)+1<p.limit


  @staticmethod
  def allocateProcInstance(p: Process ,instances: Iterable[ProcessInstance]):
    t=None
    if len(instances[ p.idx ])==0:
      t=ProcessInstance( p )
    else:
      t=instances[p.idx][0]
    t=t.allocate()
    instances[p.idx].append( t )
    return t


  @staticmethod
  def O1(data: List[TaskImplementationID] ,procs: ProcInfo,embryo):

    for i,id in enumerate(data):
      imp=embryo.processData[id]

      proc_id = min([ 
        ( proc_id ,p[imp.task.label][0] )
        for proc_id,p in enumerate(procs.defs)
        if Genes.isAvailable(p ,procs.instances[proc_id])
      ] ,key=lambda v:v[1])[0]
      

      embryo.processData[ id ].proc = Genes.allocateProcInstance( procs.defs[proc_id],procs.instances )
      



  @staticmethod
  def O2(data: List[TaskImplementationID] ,procs: ProcInfo,embryo):
    
    for i,id in enumerate(data):
      imp=embryo.processData[id]
      proc_id = min([ 
        ( proc_id ,p[imp.task.label][1] )
        for proc_id,p in enumerate(procs.defs)
        if Genes.isAvailable(p ,procs.instances[proc_id])
      ] ,key=lambda v:v[1])[0]

      
      embryo.processData[ id ].proc = Genes.allocateProcInstance( procs.defs[proc_id],procs.instances )
      
      
    


  @staticmethod
  def O3(data: List[TaskImplementationID] ,procs: ProcInfo ,embryo):

    for i,id in enumerate(data):
      imp=embryo.processData[id]
      proc_id = min([ 
        ( proc_id ,p[imp.task.label][1]*p[imp.task.label][0] )
        for proc_id,p in enumerate(procs.defs)
        if Genes.isAvailable(p ,procs.instances[proc_id])
      ] ,key=lambda v:v[1])[0]

      embryo.processData[ id ].proc = Genes.allocateProcInstance( procs.defs[proc_id],procs.instances )
      
      

  @staticmethod
  def O4(data: List[TaskImplementationID] ,procs: ProcInfo ,embryo):

    for id in data:
      node = embryo.processData[id]
      if len(node.task.parents)>0:
        proc_count = {}
        for p in node.task.parents:
          parent_id = p.label
          parent_proc = embryo.processData[ parent_id ].proc.proc
          if parent_proc.idx in proc_count:
            proc_count[parent_proc.idx]+=1
          else:
            proc_count[parent_proc.idx]=1

        proc_id=min( proc_count.items(),key=lambda x:x[1] )[0]
        embryo.processData[ id ].proc = Genes.allocateProcInstance( procs.defs[proc_id],procs.instances )



  @staticmethod    
  def O5(data: List[TaskImplementationID] ,procs: ProcInfo ,embryo):

    for i,id in enumerate(data):
      proc_id=min([ 
        ( proc_id ,len(procs.instances[proc_id]) )
        for proc_id ,proc in enumerate(procs.defs)
        if Genes.isAvailable(proc,procs.instances[proc_id])
      ], key=lambda v:v[1])[0]
      
      embryo.processData[ id ].proc = Genes.allocateProcInstance( procs.defs[ proc_id ] ,procs.instances )


  
      



class ProcsInfo:
  def __init__(self,
    definitions: List[Process],
    instances: Iterable[Iterable[ProcessInstance]]
  ):
    self.defs=definitions
    self.instances=instances




if __name__=="__main__":
  from Genetic.decisionTree import DecisionTree
  _td = TaskData.loadFromFile(r"Grafy\Z_wagami\GRAPH.20")

  tree = DecisionTree.createRandomTree(_td)
  #print(tree.procInstancess)
  #Genes.O2(tree.nodes[1].data,_td.proc,,tree.embryo)

  #print(tree.nodes[1].data)

  #print(*tree.embryo.processData,sep='\n')
  Genes.O1(tree.nodes[1].data,ProcsInfo(_td.proc,tree.procInstancess),tree.embryo)
  Genes.O2(tree.nodes[1].data,ProcsInfo(_td.proc,tree.procInstancess),tree.embryo)
  Genes.O3(tree.nodes[1].data,ProcsInfo(_td.proc,tree.procInstancess),tree.embryo)
  Genes.O4(tree.nodes[1].data,ProcsInfo(_td.proc,tree.procInstancess),tree.embryo)
  Genes.O5(tree.nodes[1].data,ProcsInfo(_td.proc,tree.procInstancess),tree.embryo)

  #print('------')
  #print(*tree.embryo.processData,sep='\n')
  

  #print('---------')
  #print(tree.nodes[1].data)
  
  
