from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Tuple

from channel import Channel
from Graph.graph import Graph
from proc import Proc


@dataclass(init=False)
class GraphData:
    graph: Graph
    proc: Iterable[Proc]
    channels: Iterable[Channel]

    def __init__(
        self,
        text: str,
        genIdx: Callable[[str], str] = None,
        parseEdgeData: Callable[[str], str or Tuple[str, int]] = None
    ):
        data = text.strip().split('@')[1:]
        data = [i.split('\n', 1)[1] for i in data]
        self.graph = Graph.fromString(data[0], genIdx, parseEdgeData)
        self.proc = Proc.createMany(*data[1:-1])
        self.channels = Channel.createMany(data[-1])
