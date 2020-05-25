import argparse
import re
from pathlib import Path

from Graph.graph import Graph
from Graph.Tree.tree import Tree


def checkPath(path):
    p = Path(path)
    if p.exists() and p.is_file():
        return p
    raise argparse.ArgumentError('Podany plik nie istnieje.')


parser = argparse.ArgumentParser(
    description='Program wczytuje z pliku graf oraz sprawdza, '
    'czy zawiera cykle'
)
parser.add_argument(
    'file',
    type=checkPath,
    nargs=1,
    help='Ścieżka do pliku zawierającego dane do stworzenia grafu i drzewa '
         'rozpinającego. Kolejne wierzchołki powinny być w formacie: etykieta '
         'liczba_wierzchołków indeks_wierzchołka(waga_krawędzi)*'
         'liczba_wierzchołków'
)


def getLabel(x):
    return x.replace('T', '')


def getEdgeData(x):
    out = re.findall(r'(\d*)\((\d*)\)', x)[0]
    return out[0], int(out[1])


if __name__ == "__main__":
    outText = []
    args = parser.parse_args()
    text = args.file[0].read_text()

    exp = re.compile(r'@tasks\s*\d*\s*((?:.*\s?)*?)@')

    data = exp.findall(text)[0]

    graph = Graph.fromString(data, getLabel, getEdgeData)
    tree = Tree.fromGraph(graph)

    print(f"Podany graf{'' if graph.checkCycles() else ' nie'} "
          "zawiera cykle/cykli.")
    print(f"Podane drzewo{'' if tree.checkCycles() else ' nie'} "
          "zawiera cykle/cykli.")
