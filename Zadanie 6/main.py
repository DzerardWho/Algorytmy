from __future__ import annotations

import argparse
from typing import Any, Dict, Tuple

import numpy as np
from prettytable import PrettyTable

from genetic import Genetic


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
    description="Program znajduje najoptymalniejsze konfiguracje "
    "się do podanej liczby. Stosowany jest algorytm genetyczny. Używany "
    "selektor: selektor rankingowy."
)

parser.add_argument('-v', '--verbose', default=False, action='store_true',
                    help="Wypisuj informacje o kolejnych generacjach.")
parser.add_argument('-g', '--generations', default=100,
                    type=isNonNegative, help="Maksymalna liczba generacji.")
parser.add_argument('-p', '--population', default=500,
                    type=isNonNegative, help="Rozmiar populacji.")
parser.add_argument('-s', '--select', default=100, type=isNonNegative,
                    help="Rozmiar populacji, która ma zostać użyta do "
                    "stowrzenia nowej generacji.")
parser.add_argument('-c', '--clone', default=5, type=cloneMutationInRange,
                    help="Z jakim prawdopodobieństwem ma nowy genotym zostać "
                    "stworzony w wyniku klonowania. Przedział [0, 20].")
parser.add_argument('-m', '--mutate', default=13, type=cloneMutationInRange,
                    help="Z jakim prawdopodobieństwem ma nowy genotym zostać "
                    "stworzony w wyniku mutacji. Przedział [0, 20].")
parser.add_argument('-i', '--info', default=False,
                    action='store_true', help="Wypisz ustawienia.")
parser.add_argument('-ws', '--withoutStagnation', default=False,
                    action='store_true', help="Wyłącz sprawdzanie, czy funkcja"
                    " dopasowania utrzymuje się na tym samym poziomie.")
parser.add_argument('-z', '--zadanie', default=False, action='store_true',
                    help='Wypisz dane użyte w zadaniu.')


def fitFunc(instalation: np.ndarray, constants: Dict[str, Any]) -> np.ndarray:
    costs = np.apply_along_axis(
        lambda x: np.sum(constants['costs'][x]), 1, instalation
    )
    smartPoints = np.apply_along_axis(
        lambda x: np.sum(constants['smartPoints'][x]), 1, instalation
    )
    smartPoints[costs > constants['limit']] = 0
    return smartPoints


def stopFunction(fittnes: np.ndarray, constants: Dict[str, Any]) -> np.ndarray:
    bestFit = fittnes.max()
    if bestFit == constants['currBestFit']:
        constants['currBestFitForXGenerations'] += 1
        if constants['currBestFitForXGenerations'] == \
                constants['stagnationLimit']:
            return fittnes == fittnes[np.argmax(fittnes)]
    else:
        constants['currBestFit'] = bestFit
        constants['currBestFitForXGenerations'] = 1


def printResults(
    results: np.ndarray,
    costs: np.ndarray,
    smartPoints: np.ndarray,
    items: Tuple[int, str]
) -> None:
    tab = PrettyTable()
    legend = []
    dataLegend = []
    data = []
    idx = 0
    for i in range(len(items)):
        legend.append(f'*{i + 1}* - {items[i][1]}')
        dataLegend.append(f'*{i + 1}*')
        data.append(np.sum(results[:, idx:idx + items[i][0]], 1))

        idx += items[i][0]

    legend.append(f'*{i + 2}* - Koszt')
    dataLegend.append(f'*{i + 2}*')
    data.append(np.apply_along_axis(lambda x: np.sum(costs[x]), 1, results))

    legend.append(f'*{i + 3}* - Punkty smart')
    dataLegend.append(f'*{i + 3}*')
    data.append(
        np.apply_along_axis(lambda x: np.sum(smartPoints[x]), 1, results)
    )

    data = np.unique(np.array(data).T, axis=0)

    tab.field_names = dataLegend
    for i in data:
        tab.add_row(i)

    print('Tabela przedstawia ilość sztuk danych elementów.')
    print('Legenda:')
    print('\t' + '\n\t'.join(legend))
    print(tab)


def printData(
    costs: np.ndarray,
    smartPoints: np.ndarray,
    items: Tuple[int, str]
) -> None:
    tab = PrettyTable(["Element", "Ilość elementów", "Koszt", "Punkty smart"])
    for i in zip(items, costs, smartPoints):
        tab.add_row([i[0][1], i[0][0], i[1], i[2]])
    print(tab)


def main():
    args = parser.parse_args()
    costs = np.array([*([500] * 4), *([1500] * 2), *([300] * 10),
                      *([750] * 3), 1000, 750, 350, 350, 1000, 700, 700])

    smartPoints = np.array([*([1] * 4), *([4] * 2), *([1] * 10),
                            *([2] * 3), *([3] * 4), 4, 2, 2])

    items = (
        (4, 'Zestaw sterowania roletami'),
        (1, 'Zestaw zdalnego sterowania'),
        (1, 'System zabezpieczeń'),
        (4, 'Zestaw sterowania ogrzewaniem'),
        (6, 'Zestaw inteligentnych kontaktów elektrycznych'),
        (3, 'Zestaw sterowania oświetleniem'),
        (1, 'System łączący multimedia z oświetleniem'),
        (1, 'Zestaw czujników'),
        (2, 'Home assistant'),
        (1, 'Zestaw sterowania multimediami'),
        (2, 'Automatyczne odkurzacze'),
    )

    if args.zadanie:
        printData(costs, smartPoints, items)
        return

    if args.withoutStagnation:
        stagnationLimit = args.generations + 1
    else:
        stagnationLimit = args.generations // 4
        if stagnationLimit == 0:
            stagnationLimit = args.generations // 2

    gen = Genetic(
        fitFunc,
        costs.shape[0],
        {
            'costs': costs,
            'smartPoints': smartPoints,
            'limit': 9000,
            'currBestFit': 0,
            'currBestFitForXGenerations': 0,
            'stagnationLimit': stagnationLimit,
        },
        stopFunction,
        args.population,
        args.select,
        args.generations,
        args.mutate,
        args.clone,
        args.verbose,
        True
    )

    if args.info:
        gen.printInfo()
        input("Naciśnij ENTER, aby kontynuować.")

    solutions, generation = gen.solve()
    solutions = np.unique(solutions, axis=0)

    if generation == -1:
        print(f"\nOsiągnięto limit generacji: {gen.maxNumOfGenerations}.")
        print("\nRozwiązania:\n")
        printResults(solutions, costs, smartPoints, items)
        return

    print("\nOsiągnięto stagnację.")
    print(f"Rozwiązanie znalezione po {generation} generacjach.")
    print("\nRozwiązania:\n")

    printResults(solutions, costs, smartPoints, items)


if __name__ == "__main__":
    main()
