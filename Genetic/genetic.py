from __future__ import annotations
import sys

sys.path.append(".")
from copy import deepcopy
from typing import Any, Callable, Dict, List

import numpy as np

from Graph import Graph

from TaskData import TaskData

# TODO: input from user
ALPHA = 10
BETA = 0.6
GAMMA = 0.2
DELTA = 0.2
C = 3
T = 3
EPSILON = 3


class Genetic:
    def __init__(
            self,
            graph: Graph,
            # I hope this Nones are temporary?
            fitFunction: Callable[
                [np.ndarray, Dict[str, Any]], np.ndarray] = None,
            genes: List[List[Callable[np.ndarray], np.ndarray]] = None,
            genesProbability: List[List[int]] = None,
            constants: Dict[str, Any] = None,
            populationSize: int = 1000,
            populationFromSelector: int = 200,
            maxNumOfGenerations: int = 1000,
            populationFromReproduction: int = 333,  # clones
            populationFromMutations: int = 333,
            populationFromCrossbreads: int = 334,
            stagnationLimit: int = 50,
            minimalizeFittnes: bool = True,
            verbose: bool = False,
            procs=None
    ):
        # if populationSize <= 0:
        #     raise ValueError("Population must be a positive inteager.")
        #
        # if populationFromMutations + populationFromCrossbreads != populationSize:
        #     raise ValueError("Size of future populations must equal the size"
        #                      " of the first generation.")
        #
        # if not self.sameShape(genes, genesProbability):
        #     raise ValueError("Shape of gene array does not match the shape of"
        #                      "it's probability array.")

        self.maxNumOfGenerations = maxNumOfGenerations
        self.graph: Graph = graph
        self.constants = constants or {}

        self.populationSize = populationSize
        self.populationFromSelector = populationFromSelector
        self.stagnationLimit = stagnationLimit
        self.minimalizeFittness = minimalizeFittnes

        self.populationFromReproduction = populationFromReproduction
        self.populationFromCrossbreads = populationFromCrossbreads

        # Count once what doesn't change later
        self.__crossbreadSize = np.array([
            np.ceil(self.populationFromCrossbreads / 2), 2
        ], dtype=int)

        self.populationFromMutations = populationFromMutations

        self.probability = self.normalize(
            (self.populationSize - np.arange(self.populationSize))
            / self.populationSize
        )

        self.genesProbability = genesProbability
        self.genes = genes

        self.population = None
        self.fittness = np.empty(self.populationSize)
        # self.createInitialPopulation()

        self.bestFittnessFinder = (lambda: np.min(self.fittness)) \
            if minimalizeFittnes else (lambda: np.max(self.fittness))

        self.fitFunction = fitFunction

        if verbose:
            self.__log = lambda *msg: print(*msg)
        else:
            self.__log = lambda *msg: None
        self.procs = procs

    @staticmethod
    def sameShape(a1: List[Any], a2: List[Any]) -> bool:
        #  TODO: recursion
        return True

    @staticmethod
    def normalize(v: np.ndarray):
        return v / np.sum(v)

    def generate_embryo(self):
        # I think we need to generate as many embryos as large as the size
        # of the entire population
        _embryo = []
        # I think this is a bad idea to copy entire object if we modify only
        # a primitive type. Much better approach would be to store num of used
        # processes in original object and reset it between each generation of
        # embryo
        _procs = deepcopy(self.procs)
        for task in self.graph:
            proc, _procs = self.get_random_proc(_procs)
            _embryo.append([task, proc])
        return _embryo

    def get_random_nodes_value(self):
        return np.random.randint(2, high=len(self.graph))

    def create_genotype_skeleton(self, nr_of_nodes):
        pass

    def get_genes_for_node(self):
        # return proc and comm gene
        pass

    def createInitialPopulation(self):
        self.population = np.array(
            [
                np.random.choice(
                    a=i,
                    size=[len(self.graph), self.populationSize, ],
                    p=j,
                ) for i, j in zip(self.genes, self.genesProbability)
            ]
        ).T

    def createNewPopulation(self):
        newPopulation = np.empty_like(self.population)

        newPopulation[:self.populationFromReproduction] = \
            self.reproduce(self.populationFromReproduction)
        t = self.populationFromReproduction

        newPopulation[t: t + self.populationFromCrossbreads] = \
            self.crossbread(
                self.reproduce(self.__crossbreadSize)
        ).flatten()[:self.populationFromCrossbreads]

        t += self.populationFromCrossbreads

        newPopulation[t:] = self.mutate(
            self.reproduce(self.populationFromMutations))

        self.population[:] = newPopulation

    def reproduce(self, size: int or np.ndarray) -> np.ndarray:
        return np.random.choice(
            self.population,
            size,
            False,  # Can we reselect already selected genotypes?
            self.probability
        )

    def mutate(self, genotype: np.ndarray) -> np.ndarray:
        # TODO: rewrite function after implementation of decision tree
        # In decision tree implement '~' operator for mutation
        # This should let us to iterate over array on Numpy/C++ side

        # mutationSpot = np.random.choice(np.arange(0, genotype.shape[0]))
        # newGenotype = genotype.copy()
        # newGenotype[mutationSpot] = [
        #     np.random.choice(
        #         a=i,
        #         p=j,
        #     ) for i, j in zip(self.genes, self.genesProbability)
        # ]
        return genotype

    def crossbread(self, parents):
        # TODO: rewrite function after implementation of decision tree
        # In decision tree implement '^' operator for crossbread
        # This should let us to iterate over array on Numpy/C++ side

        # parent1, parent2 = parents
        # splitSpot = np.random.choice(np.arange(0, parent1.shape[0]))
        # childNodes = self.graph[splitSpot].collectChildrenLabels()
        # child1, child2 = parent1.copy(), parent2.copy()

        # child1[childNodes] = parent2[childNodes]
        # child2[childNodes] = parent1[childNodes]

        return parents

    # def reproduce(self, genotype: np.ndarray):
    #     return genotype

    def __sortFittness(self):
        positions = np.argsort(self.fittness)

        if not self.minimalizeFittness:
            positions = positions[::-1]

        self.fittness[:] = self.fittnes[positions]
        self.population[:] = self.population[positions]

    def compute(self):
        lastBestFittness = np.inf
        lastChangeOfBestFittness = 0
        for gen in range(self.maxNumOfGenerations - 1):
            self.fittness[:] = self.fitFunction(
                self.population,
                self.constants
            )
            self.__sortFittness()

            bestFittness = self.bestFittnessFinder()
            if bestFittness == lastBestFittness:
                lastChangeOfBestFittness += 1
                if lastChangeOfBestFittness >= self.stagnationLimit:
                    return
            else:
                lastBestFittness = bestFittness
                lastChangeOfBestFittness = 0

            self.createNewGeneration()

        self.fittness[:] = self.fitFunction(
            self.population,
            self.constants
        )
        self.__sortFittness()

    def get_random_proc(self, procs):
        # works on a copy of procs, doesnt modify original objects
        _rand_proc = None
        while not _rand_proc:
            _i = np.random.randint(4)
            if procs[_i].limit:
                _rand_proc = procs[_i]
                procs[_i].limit -= 1
        return _rand_proc, procs

    def generate_genotype(self):
        embryo = gen.generate_embryo()
        _nr_of_nodes = gen.get_random_nodes_value()
        _gen_tree = gen.build_random_tree(_nr_of_nodes)
    #     TODO rest of genotype creation

    @staticmethod
    def build_random_tree(nr_of_nodes):
        _tree = Graph(nr_of_nodes)
        _from = [_tree.nodes[0].label]
        _available_nodes = [_n.label for _n in _tree.nodes[1:]]
        while _available_nodes:
            _new_from = _from[:]
            for _f in _from:
                _range = int(np.random.gamma(shape=int(nr_of_nodes/3), scale=0.5))
                _range = _range if _range <= nr_of_nodes else nr_of_nodes
                for i in range(_range):
                    _to = np.random.choice(_available_nodes)
                    _tree.connectNodes(_f, _to)
                    _available_nodes.remove(_to)
                    if not _available_nodes:
                        return _tree
                    _new_from.append(_to)
                    try:
                        _new_from.remove(_from)
                    except ValueError:
                        pass
            _from = _new_from

        return _tree

if __name__ == '__main__':
    # Out of curiosity: how do you run this file? Do you load it as a module?
    _td = TaskData.loadFromFile(r"Grafy\Z_wagami\test.6")
    gen = Genetic(graph=_td.graph, procs=_td.proc)
    genotype = gen.generate_genotype()
