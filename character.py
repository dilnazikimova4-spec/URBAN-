
from game_object import GameObject


class Character(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_x = x
        self.start_y = y
        self.px = x
        self.py = y
        self.dx = 0
        self.dy = 0

    def can_move(self, dx, dy, maze):
        return not maze.is_wall(self.x + dx, self.y + dy)

    def remember(self):
        self.px = self.x
        self.py = self.y

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.px = self.x
        self.py = self.y
        self.dx = 0
        self.dy = 0

    def update(self, game):
        pass

    def draw(self, canvas):
        pass

