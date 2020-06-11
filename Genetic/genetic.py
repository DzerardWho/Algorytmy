from __future__ import annotations
import numpy as np
from typing import Any, Callable, Dict, List, Iterable
from copy import deepcopy
import sys

sys.path.append(".")

from Genetic.decisionTree import DecisionTree
from Graph import Graph
from TaskData import TaskData, Process


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
            maxNumOfGenerations: int = 1000,
            populationFromReproduction: int = 333,  # clones
            populationFromMutations: int = 333,
            populationFromCrossbreads: int = 334,
            stagnationLimit: int = 50,
            minimalizeFittnes: bool = True,
            verbose: bool = False,
            procs: Iterable[Process] = None
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

        self.population: Iterable[DecisionTree] = None
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
        return deepcopy(np.random.choice(
            self.population,
            size,
            False,  # Can we reselect already selected genotypes?
            self.probability
        ))

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
        return ~genotype

    def crossbread(self, parents: np.ndarray):
        # TODO: rewrite function after implementation of decision tree
        # In decision tree implement '^' operator for crossbread
        # This should let us to iterate over array on Numpy/C++ side
        return parents[:, 0] ^ parents[:, 1]

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


if __name__ == '__main__':
    _td = TaskData.loadFromFile(r"Grafy\Z_wagami\GRAPH.20")
    # print(_td.proc)
    # print(_td.channels)
    # for i in _td.proc:
    #     print(i.cost)
    # _td = TaskData.loadFromFile(r"Grafy\Z_wagami\test.6")
    tree = DecisionTree.createRandomTree(_td)
    tree.render()
    # gen = Genetic(graph=_td.graph, procs=_td.proc)
    # genotype = gen.generate_genotype()
    # gen.build_random_tree(len(gen.graph)).render('genotype')
