from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class Process:
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
            taskCount: int,
            dataProc: str,
            dataTimes: str,
            dataCosts: str
    ) -> Iterable[Process]:
        procHeader, dataProc = dataProc.split('\n', 1)
        procs = np.fromstring(dataProc, dtype=int, sep=' ')
        # procCount = procs.shape[0] // 3
        tmp = procHeader.split(' ')

        if not (len(tmp) == 2 and tmp[1].isdigit()):
            raise ValueError("Number of processes must be given in the "
                             "header.")

        procCount = int(tmp[1])

        if procCount != (procs.shape[0] // 3):
            raise ValueError("Incorrect number of processes.")

        procs = procs.reshape(procCount, 3)
        for proc in procs:
            proc[1] = proc[1] if proc[1] > 0 else 99999

        times = np.fromstring(dataTimes.split('\n', 1)[1], dtype=int, sep=' ')
        costs = np.fromstring(dataCosts.split('\n', 1)[1], dtype=int, sep=' ')

        tpCount = taskCount * procCount

        if tpCount != times.shape[0]:
            raise ValueError("Incorrect size of the 'times' section.")
        if tpCount != costs.shape[0]:
            raise ValueError("Incorrect size of the 'cost' section.")

        times = times.reshape(taskCount, procCount).T
        costs = costs.reshape(taskCount, procCount).T

        return [cls(*i) for i in zip(procs, times, costs)]

    def __getitem__(self, index) -> np.ndarray:
        return np.array(
            [self.procs[index], self.times[index], self.costs[index]]
        )
