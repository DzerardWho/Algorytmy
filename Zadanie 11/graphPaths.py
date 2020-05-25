from __future__ import annotations

from math import ceil
from typing import Iterable, Type

from channel import Channel
from Graph.baseNode import BaseNode
from proc import Proc


class GraphPath:
    def __init__(
        self,
        nodes: Iterable[Type[BaseNode]],
        proc: Iterable[int],
        channelRate: int
    ):
        self.nodes = nodes
        self.proc = proc
        self.channelRate = channelRate
        self.__dirty = True
        self.__time = 0

    def pop(self) -> Type[BaseNode]:
        self.__dirty = True
        return self.nodes.pop(0)

    def __contains__(self, item: Type[BaseNode]):
        return item in self.nodes

    def splitRemove(self, item: Type[BaseNode]) -> GraphPath:
        index = self.nodes.index(item)
        out = GraphPath(self.nodes[index+1:], self.proc, self.channelRate)
        self.__dirty = True
        self.nodes = self.nodes[:index]
        return out

    def __len__(self):
        return len(self.nodes)

    @property
    def time(self) -> int:
        if self.__dirty:
            if not len(self.nodes):
                return -1
            prev = self.nodes[0]
            out = self.proc[int(prev.label[1:])]
            for i in range(1, len(self.nodes)):
                curr = self.nodes[i]
                out += ceil(prev.children[curr] / self.channelRate) + \
                    self.proc[int(curr.label[1:])]
                prev = curr
            self.__time = out
            self.__dirty = False
        return self.__time


class Paths:
    def __init__(
        self,
        paths: Iterable[Iterable[Type[BaseNode]]],
        proc: Proc,
        channel: Channel
    ):
        #  ścieżka krytyczna jest zawsze na pierwszym miejscu
        self.paths = [
            GraphPath(i, proc.costs, channel.rate) for i in paths
        ]
        self.paths.sort(key=lambda x: -x.time)

    def __len__(self):
        return sum(len(i) for i in self.paths)

    def pop(self):
        if not len(self.paths):
            return None
        value = self.paths[0].pop()
        new = [self.paths[0]]
        for i in self.paths[1:]:
            if value in i:
                t = i.splitRemove(value)
                if len(t):
                    new.append(t)
            if len(i):
                new.append(i)
        self.paths = new
        self.paths.sort(key=lambda x: -x.time)
        return value
