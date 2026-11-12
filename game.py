
import tkinter as tk

from settings import CELL, TICK, MAZE_MAP, GHOST_COLORS, BACKGROUND
from maze import Maze
from player import Player
from ghost import Ghost
from fast_ghost import FastGhost


class Game:
    def __init__(self, root):
        self.root = root
        root.title("PACMAN - URBAN NEON")
        root.resizable(False, False)
        root.configure(bg=BACKGROUND)

        self.info = tk.Label(
            root,
            font=("Arial", 12, "bold"),
            bg=BACKGROUND,
            fg="#00e5ff",
            padx=8,
            pady=8
        )
        self.info.pack(fill="x")

        self.canvas = tk.Canvas(
            root,
            width=len(MAZE_MAP[0]) * CELL,
            height=len(MAZE_MAP) * CELL,
            bg=BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack()

        root.bind("<Key>", self.on_key)

        self.new_game()
        self.tick()

    def new_game(self):
        self.maze = Maze(MAZE_MAP)
        self.player = Player(*self.maze.player_start)

        self.ghosts = [
            Ghost(x, y, GHOST_COLORS[i % len(GHOST_COLORS)])
            for i, (x, y) in enumerate(self.maze.ghost_starts)
        ]

        self.fast_ghosts = [
            FastGhost(x, y)
            for x, y in self.maze.fast_ghost_starts
        ]

        self.objects = self.maze.objects
        self.objects.append(self.player)
        self.objects.extend(self.ghosts)
        self.objects.extend(self.fast_ghosts)

        self.score = 0
        self.coins_collected = 0
        self.lives = 3
        self.ticks = 0
        self.power_ticks = 0
        self.state = "play"

    def all_ghosts(self):
        return self.ghosts + self.fast_ghosts

    def on_key(self, event):
        keys = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        if event.keysym in keys and self.state == "play":
            self.player.set_direction(*keys[event.keysym])

        elif event.keysym.lower() == "r":
            self.new_game()
            self.draw()

    def check_collision(self, ghost):
        p = self.player

        if (ghost.x, ghost.y) == (p.x, p.y):
            return True

        return (
            (ghost.x, ghost.y) == (p.px, p.py)
            and (p.x, p.y) == (ghost.px, ghost.py)
        )

    def lose_life(self):
        self.lives -= 1

        if self.lives <= 0:
            self.state = "lost"
        else:
            self.player.reset()
            for ghost in self.all_ghosts():
                ghost.reset()
            self.power_ticks = 0

    def collect_items(self):
        x, y = self.player.x, self.player.y

        if self.maze.eat_dot(x, y):
            self.score += 10

        if self.maze.collect_coin(x, y):
            self.score += 50
            self.coins_collected += 1

        if self.maze.collect_power(x, y):
            self.power_ticks = 40

    def handle_collisions(self):
        for ghost in self.all_ghosts():
            if self.check_collision(ghost):
                if self.power_ticks > 0:
                    self.score += 200
                    ghost.reset()
                else:
                    self.lose_life()
                    return

    def tick(self):
        if self.state == "play":
            self.ticks += 1

            if self.power_ticks > 0:
                self.power_ticks -= 1

            for obj in self.objects:
                obj.update(self)

            self.collect_items()
            self.handle_collisions()

            if self.state == "play" and self.player.reached_exit(self.maze):
                self.state = "won"

        self.draw()
        self.root.after(TICK, self.tick)

    def draw(self):
        self.canvas.delete("all")

        for obj in self.objects:
            obj.draw(self.canvas)

        hint = (
            "EXIT OPEN!"
            if self.maze.exit.is_open()
            else f"DOTS: {len(self.maze.dots)}"
        )

        power = (
            f"POWER: {self.power_ticks * TICK // 1000}s"
            if self.power_ticks > 0 else ""
        )

        self.info.config(
            text=(
                f"SCORE: {self.score}   "
                f"LIVES: {self.lives}   "
                f"COINS: {self.coins_collected}   "
                f"{hint}   {power}"
            )
        )

        if self.state in ("won", "lost"):
            title = "YOU WIN!" if self.state == "won" else "GAME OVER"
            color = "#00ff80" if self.state == "won" else "#ff315a"

            w = self.maze.cols * CELL
            h = self.maze.rows * CELL

            self.canvas.create_rectangle(
                w//2-160, h//2-55,
                w//2+160, h//2+55,
                fill="#10102b", outline=color, width=3
            )

            self.canvas.create_text(
                w//2, h//2-15,
                text=title,
                fill=color,
                font=("Arial", 24, "bold")
            )

            self.canvas.create_text(
                w//2, h//2+25,
                text="Press R to restart",
                fill="white",
                font=("Arial", 12)
            )
