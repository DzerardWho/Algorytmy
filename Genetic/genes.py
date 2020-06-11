from __future__ import annotations

import sys
from copy import deepcopy
from typing import Any, Callable, Dict, List, Iterable

import numpy as np

sys.path.append(".")

from decisionTree import TaskImplementation
from Graph import Graph
from Graph import Node as GNode
from TaskData import Process, TaskData
from TaskData.process import ProcessInstance



"""
Dla jednostek obliczeniowych:

  1. Najtańsza implementacja zadań – zadania są przydzielane do zasobów, dla
  których koszt ich wykonania jest najmniejszy,

  2. Najszybsza implementacja zadań – zadania są przydzielane do zasobów, dla
  których czas ich wykonania jest najmniejszy,

  3. Najmniejsze t*k – zadania są przydzielane do zasobów, dla których iloczyn
  czasu i kosztu ich wykonania jest najmniejszy

  4. Tak samo jak dla poprzednika – zadania są przydzielane do tych samych
  zasobów co ich poprzedniki,

  5. Najmniej obciążone zasoby – zadania są przydzielane sekwencyjnie do
  zasobów wykonujących najmniej zadań.

"""


class Genes:
    """
      helpers
    """
    @staticmethod
    def isAvailable(p: Process, instances: Iterable[ProcessInstance]):
        return len(instances)+1 < p.limit

    @staticmethod
    def allocateProcInstance(p: Process, proc_instances: Iterable[ProcessInstance]):
        t = None
        if len(proc_instances) < 1:
            t = ProcessInstance(p)
        else:
            t = proc_instances[0]
        t = t.allocate()
        proc_instances.append(t)
        return t

    @staticmethod
    def O1(data: List[TaskImplementationID], procs: ProcInfo, embryo: Embryo):
        for i, id in enumerate(data):
            imp = embryo.processData[id]

            proc_id = min([
                (proc_id, p[imp.task.label][0])
                for proc_id, p in enumerate(procs.defs)
                if Genes.isAvailable(p, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]

            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], procs.instances)


    @staticmethod
    def O2(data: List[TaskImplementationID], procs: ProcInfo, embryo: Embryo):
        for i, id in enumerate(data):
            imp = embryo.processData[id]
            proc_id = min([
                (proc_id, p[imp.task.label][1])
                for proc_id, p in enumerate(procs.defs)
                if Genes.isAvailable(p, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]

            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], procs.instances)

    @staticmethod
    def O3(data: List[TaskImplementationID], procs: ProcInfo, embryo: Embryo):

        for i, id in enumerate(data):
            imp = embryo.processData[id]
            proc_id = min([
                (proc_id, p[imp.task.label][1]*p[imp.task.label][0])
                for proc_id, p in enumerate(procs.defs)
                if Genes.isAvailable(p, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]

            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], procs.instances)

    @staticmethod
    def O4(data: List[TaskImplementationID], procs: ProcInfo, embryo: Embryo):

        for id in data:
            node = embryo.processData[id]
            if len(node.task.parents) > 0:
                proc_count = {}
                for p in node.task.parents:
                    parent_id = p.label
                    parent_proc = embryo.processData[parent_id].proc.proc
                    if parent_proc.idx in proc_count:
                        proc_count[parent_proc.idx] += 1
                    else:
                        proc_count[parent_proc.idx] = 1

                proc_id = min(proc_count.items(), key=lambda x: x[1])[0]
                embryo.processData[id].proc = Genes.allocateProcInstance(
                    procs.defs[proc_id], procs.instances)

    @staticmethod
    def O5(data: List[TaskImplementationID], procs: ProcInfo, embryo: Embryo):
        for i, id in enumerate(data):
            proc_id = min([
                (proc_id, len(procs.instances[proc_id]))
                for proc_id, proc in enumerate(procs.defs)
                if Genes.isAvailable(proc, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]
            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], 
                procs.instances[proc_id]
            )
            
    """
    Dla zasobów komunikacyjnych:
        1. Najmniejszy wzrost kosztu – wybierany jest kanał komunikacyjny który powoduje najmniejszy
        wzrost kosztu całego układu

        2. Najszybsza transmisja (największe b) – wybierany jest kanał komunikacyjny posiadający
        największą przepustowość

        3. Najrzadziej używany
    """

    @staticmethod
    def K1(data: List[TaskImplementationID] ,procs :ProcsInfo ,embryo: Embryo):

        for id in data:
            imp = embryo.processData[ id ]
            for e in imp.task.edges:
                if e in embryo.edgesData:
                    pass
                

        


    @staticmethod
    def K2():
        pass

    @staticmethod
    def K3():
        pass


class ProcsInfo:
    def __init__(self,
                 definitions: List[Process],
                 instances: Iterable[Iterable[ProcessInstance]]
                 ):
        self.defs = definitions
        self.instances = instances


if __name__ == "__main__":
    from Genetic.decisionTree import DecisionTree
    _td = TaskData.loadFromFile(r"Grafy\Z_wagami\GRAPH.20")


    tree = DecisionTree.createRandomTree(_td)
    


    #Genes.O1(tree.nodes[1].data, ProcsInfo(_td.proc, tree.procInstances), tree.embryo)
    #Genes.O2(tree.nodes[1].data, ProcsInfo(_td.proc, tree.procInstances), tree.embryo)
    #Genes.O3(tree.nodes[1].data, ProcsInfo(_td.proc, tree.procInstances), tree.embryo)
    #Genes.O4(tree.nodes[1].data, ProcsInfo(_td.proc, tree.procInstances), tree.embryo)
    #Genes.O5(tree.nodes[1].data, ProcsInfo(_td.proc, tree.procInstances), tree.embryo)

    Genes.K1(tree.nodes[1].data, ProcsInfo(_td.proc, tree.procInstances), tree.embryo)