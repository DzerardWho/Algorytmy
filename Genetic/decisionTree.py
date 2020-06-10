from __future__ import annotations

from typing import Iterable, List
from dataclasses import dataclass, field
from graphviz import Digraph

import numpy as np

from Graph import Graph, Node as GNode
from TaskData import TaskData, Process
from TaskData.process import ProcessInstance


@dataclass(init=False, order=True)
class TaskImplementation:
    task: GNode = field(compare=False)
    proc: Process = field(compare=False)
    weight: int

    def __init__(self, task: GNode, proc: ProcessInstance):
        self.task = task
        self.proc = proc
        time, cost = proc.proc[task.label]
        self.weight = time * cost


class Embryo:
    def __init__(
        self,
        data: Iterable[List[GNode, Process]]
    ):
        self.processData = data
        self.data = [i.task.label for i in np.sort(data)]
        self.children = []
        self.label = 'embryo'
        self.interIdx = str(id(self))

    def render(self, graph: Digraph):
        graph.node(self.interIdx, label=self.label)
        for i in self.children:
            i.render(graph)
            graph.edge(self.interIdx, i.interIdx)

    def __len__(self):
        return len(self.data)


class Node:
    def __init__(
            self,
            embryo: Embryo,
            data: Iterable[int],
            label: str = ''
    ):
        self.embryo = embryo
        self.data = data
        self.children = []
        self.parent = None
        self.label = label
        self.interIdx = str(id(self))

    def addParent(self, parent: Node):
        self.parent = parent
        parent.children.append(self)

    def render(self, graph: Digraph):
        graph.node(self.interIdx, label=self.label)
        for i in self.children:
            i.render(graph)
            graph.edge(self.interIdx, i.interIdx)

    def __len__(self):
        return len(self.data)

    # NumPy thinks, that this object is annother array when used
    # in np.random.choice
    # def __getitem__(self, index: int):
    #     return self.data[index]


class DecisionTree:
    def __init__(self, embryo: Embryo, nodes: List[Node], procInst):
        self.embryo = embryo
        self.nodes = nodes
        self.procInstancess = procInst

    def render(self):
        graph = Digraph('decisionTree')
        self.embryo.render(graph)
        graph.render(format='png')

    @staticmethod
    def getRandomProcess(procs: Iterable[Process], procInstancess: Iterable[Iterable[ProcessInstance]]):
        for i in np.random.permutation(procs):
            n = len(procInstancess[i.idx])
            if n >= i.limit:
                continue
            p = np.random.randint(n + 1)
            if p == n:
                out = ProcessInstance(i)
                procInstancess[i.idx].append(out.allocate())
            else:
                out = procInstancess[i.idx][p]
                tmp = out.allocate()
                if tmp is not out:
                    if n + 1 >= i.limit:
                        continue
                    procInstancess[i.idx].append(tmp)
                    return tmp
            return out
        raise ValueError("Not enough resources to choose from.")

    @staticmethod
    def createEmbryo(
            tasks: Graph, procs: Iterable[Process]
    ) -> Iterable[TaskImplementation, Iterable[Iterable[ProcessInstance]]]:
        procInstancess = [[] for i in range(len(procs))]
        out = np.array(
            [TaskImplementation(task, DecisionTree.getRandomProcess(procs, procInstancess))
             for task in tasks]
        )
        return out, procInstancess

    @classmethod
    def createRandomTree(cls, task: TaskData) -> DecisionTree:
        _embryo, procInst = cls.createEmbryo(task.graph, task.proc)
        embryo = Embryo(_embryo)
        numOfNodes = np.random.randint(2, len(task.graph) - 1)

        nodes = []
        parents = [embryo]

        for i in range(numOfNodes):
            parent = np.random.choice(parents)
            sizeOfPassedData = np.random.randint(1, len(parent) - 1)
            child = Node(embryo, parent.data[:sizeOfPassedData], str(i))
            child.addParent(parent)

            nodes.append(child)
            if sizeOfPassedData > 2:
                parents.append(child)

        return cls(embryo, nodes, procInst)
