from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(order=True)
class Edge:
    """Klasa do przechowywania danych o krawędzi pomiędzy dwoma wierzchołkami.
    """
    parent: Node = field(compare=False)
    child: Node = field(compare=False)
    weight: int

    def __hash__(self):
        return hash(f'{self.parent}{self.child}')


class Node:
    """Klasa implementująca wierzchołek grafu.
    """    
    def __init__(self, label: int):
        """Konstruktor klasy

        Args:
            label (int): identyfikator węzła
        """        
        self.children: Dict[Node, int] = {}
        self.parents: Dict[Node, int] = {}
        self.label = label
        self.interIdx = str(id(self))

    def addChild(self, node: Node, weight: int = 0):
        """Dodaje następnik węzła

        Args:
            node (Node): Następnik
            weight (int, optional): Waga krawędzi. Defaults to 0.
        """        
        self.children[node] = weight
        node.parents[self] = weight

    def collectChildren(self) -> List[Node]:
        """Metoda zbiera wszystkie węzły, do których można dojść
        z obecnego węzła

        Returns:
            List[Node]: Lista węzłów
        """        
        out = [self]
        for i in self.children:
            out.extend(i.collectChildren())
        return out

    def collectChildrenLabels(self) -> List[int]:
        return [i.label for i in self.collectChildren()]

    @property
    def edges(self) -> List[Edge]:
        """Lista krawędzi wychodzących z węzła.

        Returns:
            List[Edge]: Lista krawędzi `Edge`
        """        
        return [Edge(self, k, v) for k, v in self.children.items()]

    def __str__(self):
        return f'T{self.label}'

    # def __repr__(self):
    #     # Without the '- children' part, this repr is identical to the one used
    #     # to load the data from
    #     return f'T{self.label} {len(self.children)} ' \
    #            f'{" ".join([f"{k}({v})" for k, v in self.children.items()])}'

    def __getitem__(self, key: Node) -> int:
        return self.children[key]
