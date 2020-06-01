from __future__ import annotations

from typing import Any, Callable, Dict, List

import numpy as np

from Graph import Graph


class Generic:
    def __init__(
            self,
            fitFunction: Callable[[np.ndarray, Dict[str, Any]], np.ndarray],
            graph: Graph,
            genes: List[List[Callable[np.ndarray], np.ndarray]],
            genesProbability: List[List[int]],
            constants: Dict[str, Any] = None,
            populationSize: int = 1000,
            populationFromSelector: int = 200,
            maxNumOfGenerations: int = 1000,
            numOfReproductions: int = 333,  # clones
            numOfMutations: int = 333,
            numOfCrossbreads: int = 334,
            stagnationLimit: int = 50,
            minimalizeFittnes: bool = True,
            verbose: bool = False,
    ):
        if populationSize <= 0:
            raise ValueError("Population must be a positive inteager.")

        if numOfMutations + numOfCrossbreads != populationSize:
            raise ValueError("Size of future populations must equal the size"
                             " of the first generation.")

        if not self.sameShape(genes, genesProbability):
            raise ValueError("Shape of gene array does not match the shape of"
                             "it's probability array.")

        self.maxNumOfGenerations = maxNumOfGenerations
        self.graph: Graph = graph
        self.constants = constants or {}

        self.populationSize = populationSize
        self.populationFromSelector = populationFromSelector
        self.stagnationLimit = stagnationLimit
        self.minimalizeFittness = minimalizeFittnes

        self.numOfReproductions = numOfReproductions
        self.numOfMutations = numOfMutations
        self.numOfCrossbreads = numOfCrossbreads

        # Nie czaję jego wzoru, jeżeli się tego nie znormalizuje,
        # to prawdopodobieństwo nie będzie równe 1
        self.probability = self.normalize((
            self.populationSize - np.arange(self.populationSize)
        ) / self.populationSize)

        self.genesProbability = genesProbability
        self.genes = genes

        self.population = None
        self.fittness = np.empty(self.populationSize)
        self.createInitialPopulation()

        self.bestFittnessFinder = (lambda: np.min(self.fittness)) \
            if minimalizeFittnes else (lambda: np.max(self.fittness))

        self.fitFunction = fitFunction

        if verbose:
            self.__log = lambda *msg: print(*msg)
        else:
            self.__log = lambda *msg: None

    @staticmethod
    def sameShape(a1: List[Any], a2: List[Any]) -> bool:
        #  todo: rekurencujnie
        return True

    @staticmethod
    def normalize(v: np.ndarray):
        return v / np.sum(v)

    def createInitialPopulation(self):
        # Zamienić dla węzła 0 gen 'Tak samo jak dla poprzednika' ???
        # Może lepiej to zaimplementować inaczej, jeżeli
        # będzie trzeba zamieniać
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
        basePopulation = self.selectBasePopulation()
        # self.population = np.empty_like(self.population)

        elements = 0

        # Przydałaby się mała refaktoryzacja
        while elements < self.numOfReproductions:
            self.population[elements] = self.reproduce(
                np.random.choice(basePopulation)
            )
            elements += 1

        while elements < self.numOfReproductions + self.numOfMutations:
            self.population[elements] = self.mutate(
                np.random.choice(basePopulation)
            )
            elements += 1

        while elements < self.populationSize:
            c1, c2 = self.mutate(
                np.random.choice(basePopulation)
            )
            self.population[elements] = c1
            elements += 1
            if elements < self.populationSize:
                self.population[elements] = c2
                elements += 1

    def selectBasePopulation(self) -> np.ndarray:
        return np.random.choice(
            self.population,
            self.populationFromSelector,
            False,
            self.probability
        )

    def mutate(
            self,
            genotype: np.ndarray
    ) -> np.ndarray:
        mutationSpot = np.random.choice(np.arange(0, genotype.shape[0]))
        newGenotype = genotype.copy()
        newGenotype[mutationSpot] = [
            np.random.choice(
                a=i,
                p=j,
            ) for i, j in zip(self.genes, self.genesProbability)
        ]
        return newGenotype

    def crossbread(self, parent1, parent2):
        splitSpot = np.random.choice(np.arange(0, parent1.shape[0]))
        childNodes = self.graph[splitSpot].collectChildrenLabels()
        child1, child2 = parent1.copy(), parent2.copy()

        child1[childNodes] = parent2[childNodes]
        child2[childNodes] = parent1[childNodes]

        return child1, child2

    def reproduce(self, genotype: np.ndarray):
        return genotype

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
