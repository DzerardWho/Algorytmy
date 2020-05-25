from __future__ import annotations

from typing import Tuple, Type

from ..baseNode import BaseNode
from ..node import Node as GraphNode


class Node(BaseNode):
    def __init__(self, label: str):
        super().__init__(label)
        self._root = self
        self.parent: Node = None

    def addChild(self, node: Node, weight: int = 0):
        if node is self:
            raise ValueError("Tree cannot contain loops!")
        if node.parent:
            return
        super().addChild(node, weight)
        node.root = self.root
        node.parent = self

    @property
    def root(self) -> Node:
        return self._root

    @root.setter
    def root(self, root: Node):
        self._root = root
        for i in self.children:
            i.root = root

    def removeParent(self) -> Tuple[Node, int]:
        parent = self.parent
        if (parent):
            self.parent = None
            self.root = self
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
        return self.root is self

    def removeChild(self, label: str = None, child: Node = None) -> Node:
        child = super().removeChild(label, child)
        if child:
            child.parent = None
            child.root = child
        return child

    @classmethod
    def fromGraphNode(cls, node: GraphNode) -> Type[Node]:
        return cls(node.label)
