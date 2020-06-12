"""Summary
"""
from __future__ import annotations

from typing import Iterable, List, Dict, Callable
from dataclasses import dataclass, field
from graphviz import Digraph
from copy import deepcopy

import numpy as np

from Graph import Graph, Node as GNode
from TaskData import Process, ProcessInstance
import configuration

from Genetic.genes import GeneInfo, Genes


@dataclass(init=False, order=True)
class TaskImplementation:

    """Implementacja zadania.

    Attributes:
        proc (TYPE): Instancja zasobu
        task (TYPE): Węzeł drzewa decyzyjnego
        weight (TYPE): waga
    """

    task: GNode = field(compare=False)
    proc: ProcessInstance = field(compare=False)
    weight: int

    def __init__(self, task: GNode, proc: ProcessInstance):
        """Summary

        Args:
            task (GNode): Węzeł drzewa decyzyjnego
            proc (ProcessInstance): Instancja procesu aktualnie przypisana do realizacji zadania
        """
        self.task = task
        self.proc = proc
        time, cost = proc.proc[task.label]
        self.weight = time * cost

    def __deepcopy__(self, memo):
        return TaskImplementation(self.task, deepcopy(self.proc, memo))


class Embryo:

    """Embrion

    Attributes:
        data (TYPE): dane
        edgesData (TYPE): Dane o krawędziach
        label (str): Etykieta
        processData (TYPE): Dane o zasobach
    """

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

    """Węzeł drzewa decyzyjnego

    Attributes:
        children (list): Dzieci
        genes (List[Callable]): Funkcje Genów
        label (TYPE): Etykieta
        parent (TYPE): Rodzic
    """

    def __init__(
            self,
            embryo: Embryo,
            data: Iterable[int],
            label: str = ''
    ):
        """
        Args:
            embryo (Embryo): Embrion
            data (Iterable[int]): dane
            label (str, optional): Etykieta
        """
        self.embryo = embryo
        self.data = data
        self.children = []
        self.parent = None
        self.label = label
        self.interIdx = str(id(self))

    def addParent(self, parent: Node):
        """Dodaje rodzica.

        Args:
            parent (Node): Węzeł rodzica
        """
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
        """Summary

        Returns:
            List[Node]: Description
        """
        out = [self]
        for i in self.children:
            out.extend(i.collectChildren())
        return out

    # NumPy thinks, that this object is annother array when used
    # in np.random.choice
    # def __getitem__(self, index: int):
    #     return self.data[index]


class DecisionTree:

    """Drzewo decyzyjne.

    Attributes:
        embryo (TYPE): Embrion do modyfikacji
        nodes (TYPE): Węzły drzewa
        procInstances (TYPE): Instancje zasobów
    """

    def __init__(
            self,
            embryo: Embryo,
            nodes: List[Node],
            procInstances: List[ProcessInstance],
            genes: List[List[Callable]],
    ):
        """Summary

        Args:
            embryo (Embryo): Description
            nodes (List[Node]): Description
            procInstances (List[ProcessInstance]): Description
            genes (List[List[Callable]]): Description
        """
        self.embryo = embryo
        if genes:
            for i, node in enumerate(nodes):
                node.genes = genes[i]

        self.nodes = nodes
        self.procInstances = procInstances
        self.tasks_graph = configuration.taskData.graph

    def __deepcopy__(self, memo):
        embryo = deepcopy(self.embryo, memo)
        return DecisionTree(
            embryo,
            embryo.children[0].collectChildren(),
            deepcopy(self.procInstances),
            self.genes.copy()
        )

    def execGenes(self):
        """Przechodzi drzewo w szerz i wykonuje kolejne funkcje genów.
        """
        info = GeneInfo(configuration.taskData, self.procInstances)
        queue = []
        queue.append(self.embryo)
        while len(queue) > 0:
            node = queue.pop(0)
            for child in node.children:
                queue.append(child)
                child.genes[0](child.data, info, self.embryo)
                child.genes[1](child.data, info, self.embryo)

    def render(self):
        graph = Digraph('decisionTree')
        self.embryo.render(graph)
        graph.render(format='png')

    @staticmethod
    def getRandomProcess(
            procs: Iterable[Process],
            procInstances: Iterable[Iterable[ProcessInstance]]
    ):
        """Losowo przypisuje zasoby zadaniom.

        Args:
            procs (Iterable[Process]): Definicje zasobów
            procInstances (Iterable[Iterable[ProcessInstance]]):  Instancje zasobów
        """
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
        """Tworzy emrion dla podanej struktury grafu zadań.

        Args:
            tasks (Graph): Graf zadań.
            procs (Iterable[Process]): Definicje zasobów
        """
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
    def createRandomTree(cls) -> DecisionTree:
        """Tworzy losowe drzewo.

        Returns:
            DecisionTree
        """
        task = configuration.taskData
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

        genes = Genes.createRandomGenes(numOfNodes)
        return cls(embryo, nodes, procInst, genes)

    def crossbread(self, other: DecisionTree) -> (DecisionTree, DecisionTree):
        """Krzyżuje drzewa decyzyjne

        Args:
            other (DecisionTree): Drzewo z którym skrzyżować.

        Returns:
            DecisionTree, DecisionTree: Zwraca z modyfikowane drzewa
        """
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

    def get_max_path_from_node(self, start_node: Node, proc_inst) -> float:
        _n = [node for node in self.tasks_graph.nodes if self.embryo.processData[node.label].proc == proc_inst]
        _leafs = deepcopy(_n)
        for node in _n:
            for child in node.children:
                if self.embryo.processData[child.label].proc == proc_inst:
                    if node in _leafs:
                        _leafs.remove(node)

        all_paths = [[start_node]]
        for _nod in self.tasks_graph.nodes:
            for child in _nod.children:
                for path in all_paths:
                    if self.tasks_graph.nodes[path[-1].label] in child.parents:
                        new_path = path[:]
                        new_path.append(child)
                        all_paths.append(new_path)

        all_paths = [_p for _p in all_paths if _p[-1] in _leafs]
        all_paths = [ele for ind, ele in enumerate(all_paths) if ele not in all_paths[:ind]]
        _max_path_value = 0
        for path in all_paths:
            _p_value = 0
            for n in path:
                print(n)
                _p_value += 0
            if _p_value > _max_path_value:
                _max_path_value = _p_value

        return _max_path_value

    def get_fit_value(self) -> float:
        """Oblicza funkcje dopasowania.

        Args:
            c (int)
            t (int)
        """
        # TODO extract capcity for channel
        capacity = 1
        _cost = 0
        _time = 0

        #     add costs of all used universal proc resources
        for p in self.procInstances:
            if len(p) and p[0].proc.universal:
                _cost += len(p) * p[0].proc.cost
        # add costs of execution tasks on proc resources
        for i, task in enumerate(self.embryo.processData):
            _cost += task.proc.proc.costs[i]

        # add costs of joining procs to comms
        #     for p in self.procInstances:
        # for inst in p:
        # _cost += inst.comm_join_cost

        # # times

        available_tasks = []
        ongoing_tasks = [self.tasks_graph.nodes[0]]
        self.embryo.processData[0].proc.time_remaining = self.embryo.processData[0].proc.proc.times[0]
        finished_tasks = []
        while len(finished_tasks) != len(self.tasks_graph.nodes):
            _tasks_ = [(a[0], a[1], self.get_max_path_from_node(a[0], self.embryo.processData[a[0].label].proc))
                               for a in available_tasks]
            _tasks_to_start = sorted(_tasks_, key=lambda x: x[2])
            for a, _parent, _maxpath in _tasks_to_start:
                if not self.embryo.processData[a.label].proc.time_remaining:
                    ongoing_tasks.append(a)
                    _t = self.embryo.processData[a.label].proc.proc.times[a.label]
                    if self.embryo.processData[a.label].proc != self.embryo.processData[_parent.label].proc:
                        _t += np.ceil(a.parents[_parent] / capacity)
                    self.embryo.processData[a.label].proc.time_remaining = _t

            available_tasks = [
                a for a in available_tasks if a not in ongoing_tasks]

            _time += 1
            for o in ongoing_tasks:
                self.embryo.processData[o.label].proc.time_remaining -= 1
                if self.embryo.processData[o.label].proc.time_remaining < 1:
                    finished_tasks.append(o)
                    if type(available_tasks) is set:
                        available_tasks = list(available_tasks)
                    available_tasks.extend([(t, o) for t in list(o.children.keys())])
                    available_tasks = [a for a in available_tasks if a not in finished_tasks]
                    available_tasks = set(available_tasks)

                    ongoing_tasks = [o for o in ongoing_tasks if o not in finished_tasks]

        _fit = configuration.constC * _cost + configuration.constT * _time
        return _fit

    def __xor__(self, other: DecisionTree) -> (DecisionTree, DecisionTree):
        return self.crossbread(other)

    def mutate(self):
        """Mutuje drzewo

        Returns:
            DecisionTree: zwraca zmutowane drzewo
        """
        node = np.random.choice(self.nodes)
        node.genes = Genes.createRandomGenes(1)
        return self

    def __invert__(self) -> DecisionTree:
        return self.mutate()

    def __neg__(self):
        self.execGenes()

    def __pos__(self) -> float:
        return self.get_fit_value()
