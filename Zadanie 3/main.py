import argparse
import re
import sys
from pathlib import Path
from typing import List

from Graphs.graph import Graph
from Graphs.node import Node


def checkPath(path):
    if not path:
        raise argparse.ArgumentError('Nie podano pliku')
    p = Path(path)
    if p.exists() and p.is_file():
        return p
    raise argparse.ArgumentError('Podany plik nie istnieje.')


parser = argparse.ArgumentParser(
    description='Program generuje ścieżkę przeszukiwania grafu '
                'w głąb i wszerz. Program wypisuje etykiety '
                'kolejnych wierzchołków'
)

parser.add_argument(
    'file',
    type=checkPath,
    nargs='?',
    help='Ścieżka do pliku z grafem'
)


def getLabel(x):
    return x.replace('T', '')


def getEdgeData(x):
    return re.findall(r'(\d*)\((\d*)\)', x)[0]


def printTraversal(data: List[Node]) -> None:
    out = []
    for i in data:
        out.append(i.label)
    print('->'.join(out))


if __name__ == "__main__":
    args = parser.parse_args()
    text = args.file.read_text()

    data = re.findall(r'@tasks\s*\d*\s*((?:.*\s?)*?)@', text)
    if len(data) == 0:
        print('Plik nie zawiera poprawnych danych')
        sys.exit()

    g = Graph.fromString(
        data[0],
        getLabel,
        getEdgeData
    )
    print('Przeszukiwanie w głąb:')
    printTraversal(g.dephTraversal())
    print('Przeszukiwanie wszerz:')
    printTraversal(g.breadthTraversal())
