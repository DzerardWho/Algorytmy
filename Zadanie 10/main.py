from __future__ import annotations

import argparse
import re
from pathlib import Path

from channel import Channel
from Graph.graph import Graph
from graphData import GraphData
from graphPaths import Paths
from proc import Proc


def checkPath(path):
    p = Path(path)
    if p.exists() and p.is_file():
        return p
    raise argparse.ArgumentError('Podany plik nie istnieje.')


parser = argparse.ArgumentParser(
    description='Program generuje szereg węzłów za pomocą algorytmu '
    'listwego'
)

parser.add_argument(
    '-p',
    '--proc',
    type=int,
    nargs='?',
    default=0,
    help='Wybór zasobu'
)

parser.add_argument(
    '-c',
    '--chann',
    type=int,
    nargs='?',
    default=0,
    help='Wybór kanału'
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


def szeregLinowe(startNode: str, graph: Graph, proc: Proc, channel: Channel):
    out = []
    paths = Paths(graph[startNode].allPaths, proc, channel)

    while len(paths):
        out.append(paths.pop())
    return out


if __name__ == "__main__":
    outText = []
    args = parser.parse_args()
    text = args.file[0].read_text()
    proc = args.proc
    channel = args.chann

    graphData = GraphData(text, getLabel, getEdgeData)
    print(
        szeregLinowe(
            '0',
            graphData.graph,
            graphData.proc[proc],
            graphData.channels[channel]
        )
    )
