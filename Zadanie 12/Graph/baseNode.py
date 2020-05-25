from __future__ import annotations

from typing import List, Dict, Type, Tuple, Iterable


class BaseNode:
    def __init__(self, label: str):
        self.children: Dict[Type[BaseNode], int] = {}
        self.label = label
        self.interIdx = str(id(self))

    def addChild(self, node: Type[BaseNode], weight: int = 0):
        self.children[node] = weight

    def removeChild(self, label: str = None, child: Type[BaseNode] = None):
        if child is None:
            if label is None:
                return
            child = next(
                filter(lambda x: x.label == label, self.children),
                None
            )
        if child:
            return self.children.pop(child, None)

    def collectChildren(self) -> List[Type[BaseNode]]:
        out = [self]
        for i in self.children:
            out.extend(i.collectChildren())
        return out

    @property
    def edges(self) -> List[Tuple[int, Type[BaseNode], Type[BaseNode]]]:
        out = []
        for k, v in self.children.items():
            out.append((v, self, k))
        return out

    @property
    def allPaths(self) -> Iterable[Iterable[Type[BaseNode]]]:
        out = []
        for i in self.children:
            t: Iterable[Iterable[Type[BaseNode]]] = i.allPaths
            if any(self in j for j in t):
                continue
            for j in t:
                j.insert(0, self)
            out.extend(t)
        return out if len(out) else [[self]]

    def __str__(self):
        return f'{self.label}'

    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, key: Type[BaseNode]):
        return self.children[key]
