
import random
from character import Character
from settings import CELL, DIRS


class Ghost(Character):
    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.color = color
        self.move_interval = 3
        self.scared = False

    def can_move(self, dx, dy, maze):
        nx = self.x + dx
        ny = self.y + dy
        return not maze.is_wall(nx, ny) and not maze.is_exit(nx, ny)

    def update(self, game):
        self.remember()
        self.scared = game.power_ticks > 0

        if game.ticks % self.move_interval != 0:
            return

        options = [
            d for d in DIRS
            if self.can_move(d[0], d[1], game.maze)
        ]

        if not options:
            return

        if len(options) > 1:
            back = (-self.dx, -self.dy)
            options = [d for d in options if d != back] or options

        if self.scared:
            best = max(
                options,
                key=lambda d: abs(self.x+d[0]-game.player.x)
                + abs(self.y+d[1]-game.player.y)
            )
        elif random.random() < 0.6:
            best = min(
                options,
                key=lambda d: abs(self.x+d[0]-game.player.x)
                + abs(self.y+d[1]-game.player.y)
            )
        else:
            best = random.choice(options)

        self.dx, self.dy = best
        self.x += self.dx
        self.y += self.dy

    def draw(self, canvas):
        x0 = self.x * CELL + 3
        y0 = self.y * CELL + 3
        x1 = (self.x + 1) * CELL - 3
        y1 = (self.y + 1) * CELL - 3

        color = "#00d9ff" if self.scared else self.color

        canvas.create_oval(
            x0, y0, x1, y1,
            fill=color, outline="white"
        )

        canvas.create_rectangle(
            x0, (y0+y1)/2, x1, y1,
            fill=color, outline=""
        )

        for ex in (x0+8, x1-8):
            canvas.create_oval(
                ex-4, y0+8, ex+4, y0+16,
                fill="white", outline=""
            )
