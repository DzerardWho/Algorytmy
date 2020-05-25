from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class Proc:
    cost: int
    limit: int
    universal: bool
    times: Iterable[int]
    costs: Iterable[int]

    def __init__(
        self,
        proc: Iterable[int],
        times: Iterable[int],
        costs: Iterable[int]
    ):
        self.cost, self.limit, universal = proc
        self.universal = bool(universal)
        self.times = times
        self.costs = costs

    @classmethod
    def createMany(
        cls,
        dataProc: str,
        dataTimes: str,
        dataCosts: str
    ) -> Iterable[Proc]:
        procs = np.fromstring(dataProc, dtype=int, sep=' ')
        procCount = procs.shape[0] // 3
        procs = procs.reshape(procCount, 3)

        times = np.fromstring(dataTimes, dtype=int, sep=' ')
        taskCount = times.shape[0] // procCount
        times = times.reshape(taskCount, procCount).T

        costs = np.fromstring(dataTimes, dtype=int, sep=' ')\
            .reshape(taskCount, procCount).T

        return [cls(*i) for i in zip(procs, times, costs)]
