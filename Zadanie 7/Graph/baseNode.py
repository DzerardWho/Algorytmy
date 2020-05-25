from __future__ import annotations

from typing import List, Dict, Type


class BaseNode:
    def __init__(self, label: str):
        self.children: Dict[Type[BaseNode], int] = {}
        self.label = label
        self.interIdx = str(id(self))

    def addChild(self, node: Type[BaseNode], weight: int = 0):
        self.children[node] = weight

    def collectChildren(self) -> List[Type[BaseNode]]:
        out = [self]
        for i in self.children:
            out.extend(i.collectChildren())
        return out

    def __str__(self):
        return '\n'.join(
            f'{self.label} -({v})-> {k.label}' for k, v in
            self.children.items()
        )
