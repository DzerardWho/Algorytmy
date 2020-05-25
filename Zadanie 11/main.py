from __future__ import annotations

import argparse
import heapq
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Tuple, Type

from channel import Channel
from Graph.baseNode import BaseNode
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
    description='Program znajduje najkrótszą ścieżkę w grafie za pomocą '
    'algorytmu Dijkstry.'
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


@dataclass(order=True)
class DijkstraData:
    cost: int or float
    parent: DijkstraData or None = field(compare=False)
    node: Type[BaseNode] = field(compare=False)
    visited: bool = field(default=False, compare=False, init=False)
    children: int = field(default=0, compare=False, init=False)


def dijkstra(graph: Graph, start: str = '0') -> Iterable[DijkstraData]:
    nodes = {}

    startNodeData = DijkstraData(0, None, graph[start])
    queue = [startNodeData]

    while len(queue):
        elem = heapq.heappop(queue)
        for _child, cost in elem.node.children.items():
            child = nodes.get(_child)
            totalCost = elem.cost + cost
            if child is None:
                child = DijkstraData(totalCost, elem, _child)
                heapq.heappush(queue, child)
                nodes[_child] = child
                elem.children += 1
            else:
                if totalCost < child.cost:
                    child.cost = totalCost
                    child.parent.children -= 1
                    child.parent = elem
                    elem.children += 1
                if not child.visited:
                    heapq.heappush(queue, child)
        elem.visited = True
    return nodes


def shortestPath(graph: Graph, start: str = '0') -> Tuple[Iterable[str], int]:
    rawPaths = dijkstra(graph, start)
    leafs = list(filter(lambda x: x.children == 0, rawPaths.values()))
    paths = []
    for i in leafs:
        p = i
        path = [i.node]
        while p.parent is not None:
            p = p.parent
            path.append(p.node)
        paths.append((path, i.cost))
    if len(paths):
        paths.sort(key=lambda x: x[1])
        out = paths[0]
        return out[0][::-1], out[1]
    return [], 0


if __name__ == "__main__":
    outText = []
    args = parser.parse_args()
    text = args.file[0].read_text()

    graphData = GraphData(text, getLabel, getEdgeData)
    path, cost = shortestPath(graphData.graph)
    print(f'Koszt: {cost}\nŚcieżka: {"->".join(i.label for i in path)}')
