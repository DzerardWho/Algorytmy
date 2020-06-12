from __future__ import annotations

from copy import deepcopy
from typing import Iterable, List

import numpy as np

from Graph import Graph
from TaskData import Process, TaskData
import configuration

from .decisionTree import DecisionTree


class Genetic:
    """Klasa implementująca algorytm ewolucyjny w postaci programowania
     generycznego.
    """

    def __init__(self, verbose: bool = False):
        """Inicjalizacja klasy.

        Args:
            verbose (bool, optional): Czy wypisywać informacje przy generowaniu
             każdego pokolenia. Domyślnie `False`.
        """
        self.maxNumOfGenerations = 10_000

        self.populationSize = configuration.populationSize
        self.stagnationLimit = configuration.stagnationLimit

        self.populationFromReproduction = configuration.reproduction
        self.populationFromCrossbreads = configuration.crossbread

        # Count once what doesn't change later
        self.__crossbreadSize = np.array([
            np.ceil(self.populationFromCrossbreads / 2), 2
        ], dtype=int)

        self.populationFromMutations = configuration.mutate

        self.probability = self.normalize(
            (self.populationSize - np.arange(self.populationSize))
            / self.populationSize
        )

        self.population: Iterable[DecisionTree] = None
        self.createInitialPopulation()
        self.fittness = np.empty(self.populationSize, dtype=float)

        self.bestFittnessFinder = lambda: np.min(self.fittness)

        if verbose:
            self.__log = lambda *msg: print(*msg)
        else:
            self.__log = lambda *msg: None

    @staticmethod
    def normalize(v: np.ndarray):
        """Normalizuje podaną tablicę.

        Args:
            v (np.ndarray): tablica do normalizacji

        Returns:
            np.ndarray: znormalizowana tablica
        """
        return v / np.sum(v)

    def createInitialPopulation(self):
        """Generowanie początkowej populacji genotypów.
        """
        self.population = np.array(
            [DecisionTree.createRandomTree() for i in range(self.populationSize)])

    def createNewPopulation(self):
        """Generowanie nowej populacji genotypów używając operatorów selekcji,
         krzyżowania i mutacji.
        """
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
        """Implementacja operatora selekcji.

        Args:
            size (int or np.ndarray): rozmiar lub kształt wybieranej populacji

        Returns:
            np.ndarray: nowa populacja, kopia
        """
        return deepcopy(np.random.choice(
            self.population,
            size,
            False,  # Can we reselect already selected genotypes?
            self.probability
        ))

    def mutate(self, genotype: np.ndarray) -> np.ndarray:
        """Implementacja operatora mutacji.

        Args:
            genotype (np.ndarray): genotypy, które mają zostać poddane
            operatorowi mutacji

        Returns:
            np.ndarray: zmutowane genotypy
        """
        return ~genotype

    def crossbread(self, parents: np.ndarray):
        """Implementacja operatora krzyżowania.

        Args:
            genotype (np.ndarray): genotypy, które mają zostać poddane
            operatorowi krzyżowaniu; oczekuje się, że będzie ona kształtu Nx2

        Returns:
            np.ndarray: zkrzyżowane genotypy
        """
        return parents[:, 0] ^ parents[:, 1]

    def __sortFittness(self):
        """Sortowanie wartości fittness i korelujących im genotypów.
        """
        positions = np.argsort(self.fittness)

        if not self.minimalizeFittness:
            positions = positions[::-1]

        self.fittness[:] = self.fittnes[positions]
        self.population[:] = self.population[positions]

    def compute(self) -> int:
        """Główna metoda obliczająca nowe pokolenia

        Returns:
            int: numer generacji, w którym skończyło się działanie metody
        """
        lastBestFittness = np.inf
        lastChangeOfBestFittness = 0
        for gen in range(self.maxNumOfGenerations - 1):
            -self.population

            # +self.population is fit function
            print(+self.population)
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
        """Zwraca najlepszy genotyp.

        Returns:
            DecisionTree: najlepszy genotyp
        """
        return self.population[0]
