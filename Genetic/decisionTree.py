from __future__ import annotations

from typing import Iterable, List, Dict
from dataclasses import dataclass, field
from graphviz import Digraph
from copy import deepcopy

import numpy as np

from Graph import Graph, Node as GNode
from TaskData import TaskData, Process
from TaskData.process import ProcessInstance


@dataclass(init=False, order=True)
class TaskImplementation:
    task: GNode = field(compare=False)
    proc: ProcessInstance = field(compare=False)
    weight: int

    def __init__(self, task: GNode, proc: ProcessInstance):
        self.task = task
        self.proc = proc
        time, cost = proc.proc[task.label]
        self.weight = time * cost

    def __deepcopy__(self, memo):
        return TaskImplementation(self.task, deepcopy(self.proc, memo))


class Embryo:
    def __init__(
        self,
        processData: Iterable[TaskImplementation],
        data: Iterable[int] = None,
        children: Iterable[Node] = None,
        edgesData: Dict[Edge, Channel] = None,
    ):
        self.processData = processData
        self.data = data or np.array(
            [i.task.label for i in np.sort(processData)])
        self.children = children or []
        self.edgesData = edgesData or {}
        self.label = 'embryo'
        self.interIdx = str(id(self))

    def render(self, graph: Digraph):
        graph.node(self.interIdx, label=self.label)
        for i in self.children:
            i.render(graph)
            graph.edge(self.interIdx, i.interIdx)

    def __len__(self):
        return len(self.data)

    def __deepcopy__(self, memo):
        return Embryo(
            deepcopy(self.processData),
            self.data.copy(),
            deepcopy(self.children)
        )


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

    def __deepcopy__(self, memo):
        out = Node(self.embryo, self.data.copy())
        for i in self.children:
            t = deepcopy(i, memo)
            t.addParent(out)
        return out

    def collectChildren(self) -> List[Node]:
        out = [self]
        for i in self.children:
            out.extend(i.collectChildren())
        return out

    # NumPy thinks, that this object is annother array when used
    # in np.random.choice
    # def __getitem__(self, index: int):
    #     return self.data[index]


class DecisionTree:
    def __init__(
            self,
            embryo: Embryo,
            nodes: List[Node],
            procInstances: List[ProcessInstance]
    ):
        self.embryo = embryo
        self.nodes = nodes
        self.procInstances = procInstances

    def __deepcopy__(self, memo):
        embryo = deepcopy(self.embryo, memo)
        return DecisionTree(
            embryo,
            embryo.children[0].collectChildren(),
            deepcopy(self.procInstances)
        )

    def execGenes(self):
        pass

    def render(self):
        graph = Digraph('decisionTree')
        self.embryo.render(graph)
        graph.render(format='png')

    @staticmethod
    def getRandomProcess(
            procs: Iterable[Process],
            procInstances: Iterable[Iterable[ProcessInstance]]
    ):
        for i in np.random.permutation(procs):
            n = len(procInstances[i.idx])
            if n >= i.limit:
                continue
            p = np.random.randint(n + 1)
            if p == n:
                out = ProcessInstance(i)
                procInstances[i.idx].append(out.allocate())
            else:
                out = procInstances[i.idx][p]
                tmp = out.allocate()
                if tmp is not out:
                    if n + 1 >= i.limit:
                        continue
                    procInstances[i.idx].append(tmp)
                    return tmp
            return out
        raise ValueError("Not enough resources to choose from.")

    @staticmethod
    def createEmbryo(
            tasks: Graph, procs: Iterable[Process]
    ) -> Iterable[TaskImplementation, Iterable[Iterable[ProcessInstance]]]:
        procInstances = [[] for i in range(len(procs))]
        out = np.array(
            [
                TaskImplementation(
                    task,
                    DecisionTree.getRandomProcess(procs, procInstances)
                )
                for task in tasks
            ]
        )
        return out, procInstances

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

    def crossbread(self, other: DecisionTree) -> (DecisionTree, DecisionTree):
        def removeNodes(allNodes, toRemove):
            for i in toRemove:
                allNodes.pop(i, None)

        split1: Node = np.random.choice(self.nodes)
        split2: Node = np.random.choice(other.nodes)

        children1: List[Node] = split1.collectChildren()
        children2: List[Node] = split2.collectChildren()

        removeNodes(self.nodes, children1)
        removeNodes(other.nodes, children2)
        self.nodes.extends(children2)
        other.nodes.extends(children1)

        split1.parent.children.pop(split1, None)
        split2.parent.children.pop(split2, None)

        tmp = split2.parent
        split2.addParent(split1.parent)
        split1.addParent(tmp)

        return self, other

    def get_fit_value(self, c: int, t: int) -> float:
        _cost = 0
        _time = 0

    #     add costs of all used universal proc resources
        for p in self.procInstances:
            if p[0].proc.universal:
                _cost += len(p) * p.proc.cost
    # add costs of execution tasks on proc resources
        for i, task in enumerate(self.embryo.processData):
            _cost += task.proc.proc.costs[i]

    # add costs of joining procs to comms
        for p in self.procInstances:
            for inst in p:
                _cost += inst.comm_join_cost

        # # times
        # for i, task in enumerate(self.embryo.processData):
        #     _time += task.proc.proc.times[i]
        #


        _fit = c * _cost + t * _time
        return _fit

    def __xor__(self, other: DecisionTree) -> (DecisionTree, DecisionTree):
        return self.crossbread(other)

    def mutate(self):
        pass

    def __invert__(self) -> DecisionTree:
        return self.mutate()
