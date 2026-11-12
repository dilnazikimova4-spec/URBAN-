
from settings import MAZE_MAP
from wall import Wall
from dot import Dot
from coin import Coin
from power_pellet import PowerPellet
from exit import Exit


class Maze:
    def __init__(self, layout=None):
        layout = layout or MAZE_MAP

        self.walls = []
        self.wall_cells = set()
        self.dots = {}
        self.coins = {}
        self.power_pellets = {}

        self.exit = None
        self.player_start = (1, 1)
        self.ghost_starts = []
        self.fast_ghost_starts = []

        self.rows = len(layout)
        self.cols = len(layout[0])
        self.objects = []

        self.build(layout)

    def build(self, layout):
        for y, row in enumerate(layout):
            for x, char in enumerate(row):

                if char == "#":
                    obj = Wall(x, y)
                    self.walls.append(obj)
                    self.wall_cells.add((x, y))
                    self.objects.append(obj)

                elif char == ".":
                    obj = Dot(x, y)
                    self.dots[(x, y)] = obj
                    self.objects.append(obj)

                elif char == "C":
                    obj = Coin(x, y)
                    self.coins[(x, y)] = obj
                    self.objects.append(obj)

                elif char == "S":
                    obj = PowerPellet(x, y)
                    self.power_pellets[(x, y)] = obj
                    self.objects.append(obj)

                elif char == "P":
                    self.player_start = (x, y)

                elif char == "G":
                    self.ghost_starts.append((x, y))

                elif char == "F":
                    self.fast_ghost_starts.append((x, y))

                elif char == "E":
                    self.exit = Exit(x, y)
                    self.objects.append(self.exit)

    def is_wall(self, x, y):
        if (x, y) in self.wall_cells:
            return True

        if not self.exit.is_open() and self.is_exit(x, y):
            return True

        return False

    def is_exit(self, x, y):
        return (x, y) == (self.exit.x, self.exit.y)

    def eat_dot(self, x, y):
        obj = self.dots.pop((x, y), None)
        if obj is None:
            return False

        self.objects.remove(obj)

        if not self.dots:
            self.exit.unlock()

        return True

    def collect_coin(self, x, y):
        obj = self.coins.pop((x, y), None)
        if obj is None:
            return False
        self.objects.remove(obj)
        return True

    def collect_power(self, x, y):
        obj = self.power_pellets.pop((x, y), None)
        if obj is None:
            return False
        self.objects.remove(obj)
        return True
