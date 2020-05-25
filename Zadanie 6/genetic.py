from __future__ import annotations

from typing import Tuple, Dict, Any, Callable

import numpy as np

MUTATION_THRESHOLD_DEFAULT = 5
CLONE_THRESHOLD_DEFAULT = 5


class Genetic:
    def __init__(
            self,
            fitFunction: Callable[[np.ndarray, Dict[str, Any]], np.ndarray],
            genotypeSize: int,
            constants: Dict[str, Any] = None,
            stopFunction: Callable[
                [np.ndarray, Dict[str, Any]],
                np.ndarray or None
            ] = None,
            population: int = 500,
            populationFromSelector: int = 100,
            maxNumOfGenerations: int = 100,
            mutationThreshold: int or float = MUTATION_THRESHOLD_DEFAULT,
            cloneThreshold: int or float = CLONE_THRESHOLD_DEFAULT,
            verbose: bool = False,
            risingFitness: bool = True
    ):
        self.maxNumOfGenerations = maxNumOfGenerations
        self.constants = constants or {}

        self.fitFunction: Callable[
            [np.ndarray, Dict[str, Any]],
            np.ndarray
        ] = fitFunction

        self.stopFunction: Callable[
            [np.ndarray, Dict[str, Any]],
            np.ndarray or None
        ] = stopFunction or (lambda x: np.where(x == 0)[0])

        self.populationSize = population if population else 100
        self.populationFromSelector = populationFromSelector \
            if populationFromSelector < population else population // 2

        self.probability = self.normalize(np.random.chisquare(2, population))
        self.probability.sort()
        self.probability = self.probability[::-1]
        self.risingFitness = risingFitness
        self.bestFitnessSelector = (lambda x: x[np.argmax(x)]) \
            if risingFitness else (lambda x: x[np.argmin(x)])

        mutationThreshold = (mutationThreshold
                             if 0 <= mutationThreshold <= 20
                             else MUTATION_THRESHOLD_DEFAULT)
        cloneThreshold = (cloneThreshold
                          if 0 <= cloneThreshold <= 20
                          else CLONE_THRESHOLD_DEFAULT)

        if verbose:
            self.__log = lambda *msg: print(*msg)
        else:
            self.__log = lambda *msg: None

        self.breedingFuncs = {
            'a': (
                self.mutate,
                self.clone,
                self.crossbreed,
            ),
            'p': (
                mutationThreshold / 100,
                cloneThreshold / 100,
                1 - ((mutationThreshold + cloneThreshold) / 100)
            ),
        }

        self.population: np.ndarray = np.random.randint(
            0,
            2,
            (self.populationSize, genotypeSize),
            dtype=bool
        )

    def printInfo(self) -> None:
        print("\n\n")
        print("-" * 10)
        print("Rozmiar populacji: ", self.populationSize)
        print("Rozmiar populacji po selekcji: ", self.populationFromSelector)
        print("Maksymalna liczba generacji: ", self.maxNumOfGenerations)
        print("Prawdopodobmieństwo mutacji: ", self.breedingFuncs['p'][0])
        print("Prawdopodobmieństwo klonowania: ", self.breedingFuncs['p'][1])
        print("Prawdopodobmieństwo krzyżowania: ", self.breedingFuncs['p'][2])
        print("-" * 10)
        print("\n\n")

    def solve(self) -> Tuple[np.ndarray, int]:
        for gen in range(self.maxNumOfGenerations - 1):
            fitness = self.fitFunction(self.population, self.constants)
            stop = self.stopFunction(fitness, self.constants)

            if stop is not None:
                return self.population[stop], gen + 1
            self.__log(
                f'Generacja: {gen + 1}',
                f'Najlepsze dopasowanie: {self.bestFitnessSelector(fitness)}'
            )

            self.createNewGeneration(fitness)

        fitness = self.fitFunction(self.population, self.constants)
        final = self.stopFunction(fitness, self.constants)

        self.__log(
            f'Generacja: {self.maxNumOfGenerations}',
            f'Najlepsze dopasowanie: {self.bestFitnessSelector(fitness)}'
        )

        if final:
            return self.population[final], self.maxNumOfGenerations

        return (
            self.population[fitness == self.bestFitnessSelector(fitness)],
            -1
        )

    def createNewGeneration(self, fitness: np.ndarray) -> None:
        newGeneration = []
        elements = 0
        basePopulation = self.selectBasePopulation(fitness)
        while elements < self.populationSize:
            func = np.random.choice(**self.breedingFuncs)
            if func is self.crossbreed:
                newGeneration.extend(
                    func(
                        *basePopulation[
                            np.random.choice(
                                self.populationFromSelector,
                                2,
                                False
                            )
                        ]
                    )
                )
                elements += 2
            else:
                newGeneration.append(
                    basePopulation[np.random.choice(
                        self.populationFromSelector)]
                )
                elements += 1
        while elements > self.populationSize:
            newGeneration.pop(
                np.random.randint(elements)
            )
            elements -= 1

        self.population = np.array(newGeneration)

    def selectBasePopulation(self, fitness: np.ndarray) -> np.ndarray:
        positions = np.argsort(fitness)
        if self.risingFitness:
            positions = positions[::-1]
        tmp = np.random.choice(
            positions,
            self.populationFromSelector,
            False,
            self.probability
        )

        return self.population[tmp]

    @staticmethod
    def mutate(genotype: np.ndarray) -> np.ndarray:
        length = genotype.shape[0]
        newGenotype = genotype[:]
        mutations = np.random.randint(
            0,
            length,
            np.random.randint(1, length // 2)
        )
        newGenotype[mutations] = ~newGenotype[mutations]
        return newGenotype

    @staticmethod
    def crossbreed(
            parent1: np.ndarray,
            parent2: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        position = np.random.randint(1, parent1.shape[0] - 1)

        return (
            np.array([*parent1[:position], *parent2[position:]]),
            np.array([*parent2[:position], *parent1[position:]])
        )

    @staticmethod
    def clone(genotype: np.ndarray) -> np.ndarray:
        return genotype.copy()

    @staticmethod
    def normalize(v: np.ndarray) -> np.ndarray:
        return v / np.sum(v)
