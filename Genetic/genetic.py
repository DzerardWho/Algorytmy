from __future__ import annotations

from copy import deepcopy
from typing import Iterable, List

import numpy as np

from Graph import Graph
from TaskData import Process, TaskData
import configuration

from .decisionTree import DecisionTree


class Genetic:
    def __init__(self, verbose: bool = False):
        self.maxNumOfGenerations = 10_000

        self.populationSize = configuration.populationSize
        self.stagnationLimit = configuration.stagnationLimit

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

        self.population: Iterable[DecisionTree] = None
        self.fittness = np.empty(self.populationSize)
        # self.createInitialPopulation()

        self.bestFittnessFinder = lambda: np.min(self.fittness)

        if verbose:
            self.__log = lambda *msg: print(*msg)
        else:
            self.__log = lambda *msg: None

    @staticmethod
    def normalize(v: np.ndarray):
        return v / np.sum(v)

    def createInitialPopulation(self):
        self.population = np.array(
            [DecisionTree.createRandomTree() for i in range(self.populationSize)])

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
        return ~genotype

    def crossbread(self, parents: np.ndarray):
        return parents[:, 0] ^ parents[:, 1]

    def __sortFittness(self):
        positions = np.argsort(self.fittness)

        if not self.minimalizeFittness:
            positions = positions[::-1]

        self.fittness[:] = self.fittnes[positions]
        self.population[:] = self.population[positions]

    def compute(self) -> int:
        lastBestFittness = np.inf
        lastChangeOfBestFittness = 0
        for gen in range(self.maxNumOfGenerations - 1):
            -self.population

            # +self.population is fit function
            self.fittness[:] = +self.population
            self.__sortFittness()

            bestFittness = self.bestFittnessFinder()
            if bestFittness == lastBestFittness:
                lastChangeOfBestFittness += 1
                if lastChangeOfBestFittness >= self.stagnationLimit:
                    return gen
            else:
                lastBestFittness = bestFittness
                lastChangeOfBestFittness = 0

            -self.population
            self.createNewGeneration()

        self.fittness[:] = self.fitFunction(
            self.population,
            self.constants
        )
        self.__sortFittness()
        return self.maxNumOfGenerations

    def returnBest(self) -> DecisionTree:
        return self.population[0]
