from __future__ import annotations

from typing import Iterable, List
from dataclasses import dataclass, field
from graphviz import Digraph

import numpy as np

from Graph import Graph, Node as GNode
from TaskData import TaskData, Process


@dataclass(init=False, order=True)
class TaskImplementation:
    task: GNode = field(compare=False)
    proc: Process = field(compare=False)
    weight: int

    def __init__(self, task: GNode, proc: Process):
        self.task = task
        self.proc = proc
        time, cost = proc[task.label]
        self.weight = time * cost


class Node:
    def __init__(
            self,
            data: Iterable[List[GNode, Process]],
            label: str = ''
    ):
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
    def __init__(self, root: Node):
        self.root = root

    def render(self):
        graph = Digraph('decisionTree')
        self.root.render(graph)
        graph.render(format='png')

    @staticmethod
    def getRandomProcess(procs: Iterable[Process]):
        for i in np.random.permutation(procs):
            if i.limit:
                i.limit -= 1
                return i
        raise ValueError("Not enough resources to choose from.")

    @staticmethod
    def createEmbryo(
            tasks: Graph, procs: Iterable[Process]
    ) -> Iterable[List[GNode, Process]]:
        out = np.array(
            [TaskImplementation(task, DecisionTree.getRandomProcess(procs))
             for task in tasks]
        )
        out.sort()
        ~procs
        return out

    @classmethod
    def createRandomTree(cls, task: TaskData) -> DecisionTree:
        embryo = Node(cls.createEmbryo(task.graph, task.proc), 'embryo')
        numOfNodes = np.random.randint(2, len(task.graph) - 1)

        parents = [embryo]

        for i in range(numOfNodes):
            # print(parents)
            parent = np.random.choice(parents)
            sizeOfPassedData = np.random.randint(1, len(parent) - 1)
            child = Node(parent.data[:sizeOfPassedData], str(i))
            child.addParent(parent)

            if sizeOfPassedData > 2:
                parents.append(child)

        return cls(embryo)
