from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from pathlib import Path

from Graph import Graph
from TaskData.channel import Channel
from TaskData.process import Process

NUM_OF_HEADERS = 5


@dataclass(init=False)
class TaskData:
    graph: Graph
    proc: Iterable[Process]
    channels: Iterable[Channel]

    def __init__(
            self,
            text: str,
    ):
        data = text.strip().split('@')[1:]
        if len(data) != NUM_OF_HEADERS:
            raise Exception('Incorrect number of headers.')

        # data = [i.split('\n', 1)[1] for i in data]
        self.graph = Graph.fromString(data[0])
        self.proc = Process.createMany(len(self.graph), *data[1:-1])
        self.channels = Channel.createMany(data[-1])
    
    def __repr__(self):
        # TODO: add repr
        return ''

    @classmethod
    def loadFromFile(cls, path: str or Path) -> TaskData:
        if type(path) is str:
            path = Path(path)

        if not path.is_file():
            raise ValueError("Given path does not point to existing file.")

        return cls(path.read_text('utf-8'))


__all__ = [TaskData, Channel, Process]
