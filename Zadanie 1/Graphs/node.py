from typing import List, Tuple


class Node:
    def __init__(
        self,
        label: str or Tuple[str, str],
        neigbours: List[Tuple[str, str]]
    ):
        if type(label) == tuple:
            self.label, self.idx = label
        else:
            self.label = label
            self.idx = label
        self.neigbours = neigbours.copy()

    def __str__(self):
        return f'{self.label} - {self.idx}: {self.neigbours}'
