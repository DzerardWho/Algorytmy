import argparse
import re
from pathlib import Path

from Graphs.graph import Graph
from Graphs.tree import Tree


def checkPath(path):
    p = Path(path)
    if p.exists() and p.is_file():
        return p
    raise argparse.ArgumentError('Podany plik nie istnieje.')


parser = argparse.ArgumentParser(description='Na podstawie danych z pliku'
                                 ' wygeneruj graf, a z niego drzewo rozpięte.')
parser.add_argument(
    'file',
    type=checkPath,
    nargs='?',
    help='Ścieżka do pliku zawierającego dane do stworzenia grafu i drzewa '
    'rozpinającego. Dane wyjściowe są zapisywane do plików .gv w języku "dot" '
    'i wymagany jest program "Graphviz" w celu wygenerowania grafu w formie '
    'graficznej. Kolejne wierzchołki powinny być w formacie: etykieta '
    'liczba_wierzchołków indeks_wierzchołka(waga_krawędzi)*liczba_wierzchołków'
)

parser.add_argument(
    '-o',
    '--out',
    type=str,
    nargs='?',
    default=None,
    help='Nazwa docelowa pliku wyjściowego drzewa'
)

parser.add_argument(
    '-og',
    '--outGraph',
    type=str,
    nargs='?',
    default=None,
    help='Nazwa docelowa pliku wyjściowego grafu. Jeżeli zapisywanie grafu '
    'jest wyłączone, argument jest pomijany.'
)

parser.add_argument(
    '-g',
    '--graph',
    help='Zapisz graf do pliku.',
    action='store_true'
)


def getLabel(x):
    return x.replace('T', '')


def getEdgeData(x):
    return re.findall(r'(\d*)\((\d*)\)', x)[0]


if __name__ == "__main__":
    outText = []
    args = parser.parse_args()
    text = args.file.read_text()
    data = re.findall(
        r'@tasks\s*\d*\s*((?:.*\s?)*?)@', text)[0]
    if args.graph:
        g = Graph.fromString(
            data,
            getLabel,
            getEdgeData
        )
        t = Tree.fromGraph(g)
        outText.append(f'Graf zapisano do pliku {g.render(args.outGraph)}')
    else:
        t = Tree.fromString(
            data,
            getLabel,
            getEdgeData
        )
    outText.append(f'Drzewo zapisano do pliku {t.render(args.out)}')
    print('\n'.join(outText))
