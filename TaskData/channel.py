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
        self.availableProcs = np.array(procs, dtype=bool)

    def __getitem__(self, index: int) -> bool:
        return self.availableProcs[index]

    @classmethod
    def createMany(cls, data: str):
        out = []
        tmp = data.strip().splitlines()
        tmp1 = tmp[0].split(' ')

        if not (len(tmp1) == 2 and tmp1[1].isdigit()):
            raise ValueError("Number of channels must be given in the "
                             "header.")

        if int(tmp1[1]) != len(tmp[1:]):
            raise ValueError("Incorrect number of channels")

        for i in tmp[1:]:
            name, *values = i.split()
            values = [int(i) for i in values]
            out.append(cls(name, *values))
        return out

    def __repr__(self):
        # TODO: add repr
        return ''
