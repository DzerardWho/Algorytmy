from __future__ import annotations

from typing import Tuple

from ..baseNode import BaseNode


class Node(BaseNode):
    def __init__(self, label: str):
        super().__init__(label)
        self.parent: Node = None

    def addChild(self, node: Node, weight: int = 0):
        if node is self:
            raise ValueError("Tree cannot contain loops!")
        if node.parent:
            return
        super().addChild(node, weight)
        node.parent = self

    def removeParent(self) -> Tuple[Node, int]:
        if (parent := self.parent):
            self.parent = None
            out = parent.children.pop(self, None)
            return parent, out

    def swapParents(self, other: Node):
        selfParent = self.removeParent()
        otherParent = other.removeParent()
        if selfParent:
            selfParent[0].addChild(other, selfParent[1])
        if otherParent:
            otherParent[0].addChild(self, otherParent[1])

    def isHead(self) -> bool:
        return self.parent is None

    @property
    def edges(self) -> List[Tuple[int, Node, Node]]:
        out = []
        for i in self.children:
            out.append((i[1], i[0], self))
        return out
