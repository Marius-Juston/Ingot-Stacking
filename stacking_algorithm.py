from abc import ABC, abstractmethod

from matplotlib.patches import Rectangle


# Index 0 is the bottom most shelve

class Stacker(ABC):
    def __init__(self, shelves: list, gap_width: float):
        self.shelves = shelves
        self.gap_width = gap_width

    def setup(self, ingots: list):
        pass

    @abstractmethod
    def place(self, item: Rectangle) -> tuple:
        pass


class SimpleStacking(Stacker):
    def __init__(self, shelves: list, gap_width: float):
        super().__init__(shelves, gap_width)

    def place(self, item: Rectangle) -> tuple:
        item_width = item.get_width() + self.gap_width

        for shelve in self.shelves:
            w, x, y, ingots = shelve
            if item_width <= w:
                shelve[0] -= item_width
                to = (x, y)
                shelve[1] += item_width

                ingots.append(item)

                return to

        return None


class AllKnowing(Stacker):
    def __init__(self, shelves: list, gap_width: float):
        super().__init__(shelves, gap_width)

    def setup(self, ingots: list):
        super().setup(ingots)

    def place(self, item: Rectangle) -> tuple:
        item_width = (item.get_width() + self.gap_width)

        for i in range(len(self.shelves)):
            pass

        return ()
