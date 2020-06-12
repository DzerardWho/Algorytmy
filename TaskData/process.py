"""Zawiera klasy potrzebne do obsługi zasobów
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from copy import deepcopy

import numpy as np


@dataclass(init=False)
class Process:

    """Definicja zasobu
    
    Attributes:
        costs (TYPE): Koszty zadań na zasobie
        idx (TYPE): Id
        times (TYPE): Czasy zadań na zasobie
        universal (TYPE): Czy zasób uniwersalny
    """
    
    cost: int
    limit: int
    universal: bool
    times: Iterable[int]
    costs: Iterable[int]

    def __init__(
            self,
            idx: int,
            proc: Iterable[int],
            times: Iterable[int],
            costs: Iterable[int]
    ):
        """Tworzy definicje procesu.
        
        Args:
            idx (int): Id
            proc (Iterable[int]): 
            times (Iterable[int]): Lista czasów zadań
            costs (Iterable[int]): Lista kosztów zadań
        """
        self.idx = idx
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

        tmp = procHeader.split(' ')

        if not (len(tmp) == 2 and tmp[1].isdigit()):
            raise ValueError("Number of processes must be given in the "
                             "header.")

        procCount = int(tmp[1])

        if procCount != (procs.shape[0] // 3):
            raise ValueError("Incorrect number of processes.")

        procs = procs.reshape(procCount, 3)

        procs[procs[:, 1] == 0, 1] = np.iinfo(procs.dtype).max

        times = np.fromstring(dataTimes.split('\n', 1)[1], dtype=int, sep=' ')
        costs = np.fromstring(dataCosts.split('\n', 1)[1], dtype=int, sep=' ')

        tpCount = taskCount * procCount

        if tpCount != times.shape[0]:
            raise ValueError("Incorrect size of the 'times' section.")
        if tpCount != costs.shape[0]:
            raise ValueError("Incorrect size of the 'cost' section.")

        times = times.reshape(taskCount, procCount).T
        costs = costs.reshape(taskCount, procCount).T

        return np.array(
            [cls(i[0], *i[1]) for i in enumerate(zip(procs, times, costs))],
            dtype=object
        )

    def __getitem__(self, index: int) -> np.ndarray:
        return np.array(
            [self.times[index], self.costs[index]]
        )


class ProcessInstance:

    """Instancja zasobu
    
    Attributes:
        numOfAllocations (int): Ilość alokacji zasobu
        proc (TYPE): referencja do definicji
    """
    
    def __init__(self, proc: Process):
        self.proc = proc
        self.numOfAllocations = 0
        self.channels: Dict[Channel,bool] = {}

    def allocate(self) -> ProcessInstance:
        """Alokuje zasób.
        
        Returns:
            ProcessInstance: Instanca zasobu.
        """
        if not self.proc.universal and self.numOfAllocations != 0:
            out = ProcessInstance(self.proc)
            out.allocate()
            return out
        self.numOfAllocations += 1
        return self

    def deallocate(self) -> bool:
        """Dealokuje zasób.
        """
        self.numOfAllocations -= 1
        return bool(self.numOfAllocations)

    def __deepcopy__(self, memo):
        t = ProcessInstance(self.proc)
        t.numOfAllocations = self.numOfAllocations
        t.channels = deepcopy(self.channels, memo)
        return t
