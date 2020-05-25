from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(init=False)
class Channel:
    name: str
    cost: int
    rate: int
    availableProcs: Iterable[bool]

    def __init__(self, name: str, cost: int, rate: int, *procs: Iterable[int]):
        self.name = name
        self.cost = cost
        self.rate = rate
        self.availableProcs = np.array([bool(i) for i in procs])

    @classmethod
    def createMany(cls, data: str):
        out = []
        for i in data.strip().splitlines():
            name, *values = i.split()
            values = [int(i) for i in values]
            out.append(cls(name, *values))
        return out
