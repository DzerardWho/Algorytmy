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
        super().addChild(node, weight)
        if node.parent:
            node.parent.children.pop(node, None)
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
