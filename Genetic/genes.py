from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict, Iterable, List, Type

import numpy as np

from TaskData import Process, TaskData
from TaskData.process import ProcessInstance

#from .decisionTree import TaskImplementation

TaskImplementationID = Type[int]

from TaskData import Process, TaskData

import configuration

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
    def O1(data: List[TaskImplementationID], procs: GeneInfo, embryo: Embryo):
        for i, id in enumerate(data):
            imp = embryo.processData[id]

            proc_id = min([
                (proc_id, p[imp.task.label][0])
                for proc_id, p in enumerate(procs.defs)
                if Genes.isAvailable(p, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]

            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], procs.instances[proc_id])


    @staticmethod
    def O2(data: List[TaskImplementationID], procs: GeneInfo, embryo: Embryo):
        for i, id in enumerate(data):
            imp = embryo.processData[id]
            proc_id = min([
                (proc_id, p[imp.task.label][1])
                for proc_id, p in enumerate(procs.defs)
                if Genes.isAvailable(p, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]

            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], procs.instances[proc_id])

    @staticmethod
    def O3(data: List[TaskImplementationID], procs: GeneInfo, embryo: Embryo):

        for i, id in enumerate(data):
            imp = embryo.processData[id]
            proc_id = min([
                (proc_id, p[imp.task.label][1]*p[imp.task.label][0])
                for proc_id, p in enumerate(procs.defs)
                if Genes.isAvailable(p, procs.instances[proc_id])
            ], key=lambda v: v[1])[0]

            embryo.processData[id].proc = Genes.allocateProcInstance(
                procs.defs[proc_id], procs.instances[proc_id])

    @staticmethod
    def O4(data: List[TaskImplementationID], procs: GeneInfo, embryo: Embryo):

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
                    procs.defs[proc_id], procs.instances[proc_id])

    @staticmethod
    def O5(data: List[TaskImplementationID], procs: GeneInfo, embryo: Embryo):
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
    def K1(data: List[TaskImplementationID] ,info :GeneInfo ,embryo: Embryo):
        for id in data:
            imp = embryo.processData[ id ]
            parent_proc = imp.proc
            for e in imp.task.edges:
                child_proc = embryo.processData[ e.child.label ].proc
                availableChannels = [
                    chan for chan in info.chans 
                    if chan.availableProcs[ child_proc.proc.idx ]
                    and chan.availableProcs[ parent_proc.proc.idx ]
                ]
                minCost = float('inf')
                new_chan=None
                for chan in availableChannels:
                    cost=0
                    if chan not in parent_proc.channels:
                        cost+=chan.cost
                    if chan not in child_proc.channels:
                        cost+=chan.cost
                    if cost<minCost:
                        minCost=cost
                        new_chan=chan
                embryo.edgesData[e] = new_chan
                embryo.processData[ imp.task.label ].proc.channels[ new_chan ] = True
                embryo.processData[ e.child.label ].proc.channels[ new_chan ] = True
                
                

    @staticmethod
    def K2(data: List[TaskImplementationID] ,info :GeneInfo ,embryo: Embryo):
        for id in data:
            imp = embryo.processData[ id ]
            for e in imp.task.edges:
                s,t = e.parent,e.child
                parent_proc = embryo.processData[ s.label ].proc.proc.idx
                child_proc = embryo.processData[ t.label ].proc.proc.idx
                chan_max = max([
                    chan for chan in info.chans
                    if chan.availableProcs[parent_proc] 
                    and chan.availableProcs[child_proc]
                ],key=lambda c:c.rate)
                embryo.edgesData[e] = chan_max
                embryo.processData[ imp.task.label ].proc.channels[ chan_max ] = True
                embryo.processData[ e.child.label ].proc.channels[ chan_max ] = True


    @staticmethod
    def K3(data: List[TaskImplementationID] ,info :GeneInfo ,embryo: Embryo):
        count={ chan:0 for chan in info.chans }
        for edge,chan in embryo.edgesData.items():
            count[ chan ]+=1
        for id in data:
            imp=embryo.processData[ id ]
            for e in imp.task.edges:
                chan_to_use=min( count.items(),key=lambda x:x[1] )[0]
                embryo.edgesData[e]=chan_to_use
                embryo.processData[ e.child.label ].proc.channels[ chan_to_use ] = True
                embryo.processData[ imp.task.label ].proc.channels[ chan_to_use ] = True
                count[chan_to_use]+=1

    @staticmethod
    def createRandomGenes(size: int):
        #TODO probabilities from CONFIG
        return list(zip(
            np.random.choice( [ Genes.O1,Genes.O2,Genes.O3,Genes.O4,Genes.O5 ],p=configuration.genesProbability[0],size=size),
            np.random.choice( [ Genes.K1,Genes.K2,Genes.K3 ],p=configuration.genesProbability[1],size=size)))


class GeneInfo:
    #defs = configuration.taskData.proc
    #chans = td.channels
    def __init__(self,
                 td: TaskData,
                 instances: Iterable[Iterable[ProcessInstance]],
                 ):
        #self.defs = td.proc
        self.defs = configuration.taskData.proc
        self.chans = td.channels
        self.instances = instances
        


if __name__ == "__main__":
    from Genetic.decisionTree import DecisionTree
    _td = TaskData.loadFromFile(r"Grafy\Z_wagami\GRAPH.20")


    tree = DecisionTree.createRandomTree(_td)
    


    #Genes.O1(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    #Genes.O2(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    #Genes.O3(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    #Genes.O4(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    #Genes.O5(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)

    Genes.K1(tree.nodes[0].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K1(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K1(tree.nodes[2].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K2(tree.nodes[0].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K2(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K2(tree.nodes[2].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K3(tree.nodes[0].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K3(tree.nodes[1].data, GeneInfo(_td, tree.procInstances), tree.embryo)
    Genes.K3(tree.nodes[2].data, GeneInfo(_td, tree.procInstances), tree.embryo)