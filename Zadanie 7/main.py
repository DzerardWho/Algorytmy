import argparse
import re
from pathlib import Path

from Graph.Tree.tree import Tree


def checkPath(path):
    p = Path(path)
    if p.exists() and p.is_file():
        return p
    raise argparse.ArgumentError('Podany plik nie istnieje.')


parser = argparse.ArgumentParser(
    description='Wczytaj dwa drzewa na podstawie grafów, a następnie zamień '
    'pomiędzy nimi losowo wybrane poddrzewo. Wyniki końcowe są przedstawione '
    'w formie graficznej. Pliki "preSwapTree1" i "preSwapTree2" przedstawiają '
    'drzewa przed zamianą poddrzew. Pliki "postSwapTree1 i "postSwapTree2" '
    'zawierają drzewa po zamianie poddrzew.'
    )
parser.add_argument(
    'files',
    type=checkPath,
    nargs=2,
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
    text1 = args.files[0].read_text()
    text2 = args.files[1].read_text()

    exp = re.compile(r'@tasks\s*\d*\s*((?:.*\s?)*?)@')

    data1 = exp.findall(text1)[0]
    data2 = exp.findall(text2)[0]

    tree1 = Tree.fromString(data1, getLabel, getEdgeData)
    tree2 = Tree.fromString(data2, getLabel, getEdgeData)

    tree1.render('preSwapTree1')
    tree2.render('preSwapTree2')

    tree1.swapSubtrees(tree2)

    tree1.render('postSwapTree1')
    tree2.render('postSwapTree2')
