
from character import Character
from settings import CELL


class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.want_dx = 0
        self.want_dy = 0
        self.face = 0
        self.mouth = True

    def set_direction(self, dx, dy):
        self.want_dx = dx
        self.want_dy = dy

    def reset(self):
        super().reset()
        self.want_dx = 0
        self.want_dy = 0

    def update(self, game):
        self.remember()

        if (self.want_dx, self.want_dy) != (0, 0):
            if self.can_move(self.want_dx, self.want_dy, game.maze):
                self.dx = self.want_dx
                self.dy = self.want_dy

        if (self.dx, self.dy) != (0, 0):
            if self.can_move(self.dx, self.dy, game.maze):
                self.x += self.dx
                self.y += self.dy
                self.mouth = not self.mouth

                angles = {
                    (1, 0): 0,
                    (0, -1): 90,
                    (-1, 0): 180,
                    (0, 1): 270
                }
                self.face = angles[(self.dx, self.dy)]

    def reached_exit(self, maze):
        return maze.exit.is_open() and maze.is_exit(self.x, self.y)

    def draw(self, canvas):
        half = 45 if self.mouth else 12
        canvas.create_arc(
            self.x * CELL + 3,
            self.y * CELL + 3,
            (self.x + 1) * CELL - 3,
            (self.y + 1) * CELL - 3,
            start=self.face + half,
            extent=360 - 2 * half,
            fill="#ffe600",
            outline="#ffe600"
        )
