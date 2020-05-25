from __future__ import annotations
from genetic import Genetic
import numpy as np
import argparse
from typing import Dict, Any


def cloneMutationInRange(x: str) -> float:
    x = float(x)
    if 0 <= x <= 20:
        return x
    raise argparse.ArgumentTypeError("Poza oczekiwanym przedziałem [0, 20]")


def isNonNegative(x: str) -> int:
    x = int(x)
    if x >= 0:
        return x
    raise argparse.ArgumentTypeError("Wartość jest ujemnna")


parser = argparse.ArgumentParser(
    description="Program znajduje liczby z zadanego przedziału, które sumują "
    "się do podanej liczby. Stosowany jest algorytm genetyczny. Używany "
    "selektor: selektor rankingowy."
)
parser.add_argument('-v', '--verbose', default=False, action='store_true',
                    help="Wypisuj informacje o kolejnych generacjach.")
parser.add_argument('-g', '--generations', default=100,
                    type=isNonNegative, help="Maksymalna liczba generacji.")
parser.add_argument('-p', '--population', default=1000,
                    type=isNonNegative, help="Rozmiar populacji.")
parser.add_argument('-s', '--select', default=200, type=isNonNegative,
                    help="Rozmiar populacji, która ma zostać użyta do "
                    "stowrzenia nowej generacji.")
parser.add_argument('-c', '--clone', default=5, type=cloneMutationInRange,
                    help="Z jakim prawdopodobieństwem ma nowy genotym zostać "
                    "stworzony w wyniku klonowania. Przedział [0, 20].")
parser.add_argument('-m', '--mutate', default=13, type=cloneMutationInRange,
                    help="Z jakim prawdopodobieństwem ma nowy genotym zostać "
                    "stworzony w wyniku mutacji. Przedział [0, 20].")
parser.add_argument('-b', '--printBest', default=False, action='store_true',
                    help="Wypisz genotyp najlepszego wyniku w przypadku "
                    "niepowodzenia.")
parser.add_argument('-i', '--info', default=False,
                    action='store_true', help="Wypisz ustawienia.")


def fitFunc(population: np.ndarray, constants: Dict[str, Any]) -> np.ndarray:
    numbers: np.ndarray = constants['numbers']
    value: int = constants['value']
    out = []

    for i in population:
        out.append(np.abs(np.sum(numbers[i]) - value))

    return np.array(out)


def minSum(x: np.ndarray) -> int:
    nums = np.where(x <= 0)[0]
    if len(nums):
        return np.sum(x[nums])
    return x.min()


def maxSum(x: np.ndarray) -> int:
    nums = np.where(x >= 0)[0]
    if len(nums):
        return np.sum(x[nums])
    return x.max()


def main():
    args = parser.parse_args()
    minRange = int(input("Podaj dolny przedział liczb: "))
    maxRange = int(input("Podaj górny przedział liczb: "))
    if minRange >= maxRange:
        print("Nieprawidłowy przedział.")
        return
    t = np.arange(minRange, maxRange + 1)
    minVal = minSum(t)
    maxVal = maxSum(t)
    searchedNumber = int(
        input(
            "Podaj liczbę, której składniki są poszukiwane w przedziale"
            f" [{minVal}, {maxVal}]: "
        ))
    if searchedNumber < minVal or searchedNumber > maxVal:
        print("Liczba nie znajduje się w przedziale.")
        return
    gen = Genetic(
        fitFunc,
        t.shape[0],
        {
            'numbers': t,
            'value': searchedNumber,
        },
        args.population,
        args.select,
        args.generations,
        args.mutate,
        args.clone,
        args.verbose
    )

    if args.info:
        gen.printInfo()
        input("Naciśnij ENTER, aby kontynuować.")

    solutions, generation = gen.solve()
    solutions = np.unique(solutions, axis=0)

    if generation == -1:
        print("\nNie udało się znaleźć rozwiązania.")
        if args.printBest:
            print(''.join(str(int(i)) for i in solutions[0]))
            print(
                f"{' + '.join(str(x) for x in t[solutions[0]])}"
                f" = {np.sum(t[solutions[0]])}")
        return

    print(f"\nRozwiązanie znalezione w {generation} generacji.")
    print("\nRozwiązania:\n")

    for i in solutions:
        print(f"{' + '.join(str(x) for x in t[i])} = {searchedNumber}")


if __name__ == "__main__":
    main()
