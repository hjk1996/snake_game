from collections import namedtuple
from random import randint

import pygame

from direction import Direction

Coords = namedtuple("Coords", ["X", "Y"])

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class SnakeGame:
    BLOCK_SIZE = 20
    SPEED = 20

    def __init__(self, width: int = 640, height: int = 800):
        # display
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        # clock
        self.clock = pygame.time.Clock()

        # font
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 30, True, False)

        # snake
        self.head = Coords(self.width // 2, self.height // 2)
        self.body = [self.head]
        self.history = [self.head]
        self.length = 1
        self.direction = None

        # fruit
        self._make_fruit()

    def play_step(self):
        running = True
                
        self.display.fill(BLACK)

        for event in pygame.event.get():
            self._handle_event(event)

        self._move_snake()

        self._handle_fruit()

        running = not self._is_dead()
        
        if not running:
            return running
        else:
            self._update_display()
            self.clock.tick(self.SPEED)
            return running

    def _make_fruit(self):
        x = (
            randint(0, (self.width - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            * self.BLOCK_SIZE
        )
        y = (
            randint(0, (self.height - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            * self.BLOCK_SIZE
        )
        fruit = Coords(x, y)

        if fruit not in self.body:
            self.fruit = fruit
        else:
            self._make_fruit()

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.direction = Direction.DOWN
            elif event.key == pygame.K_LEFT:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = Direction.RIGHT

    def _move_snake(self):
        if self.direction == None:
            return

        if self.direction == Direction.UP:
            self.head = Coords(self.head.X, self.head.Y - self.BLOCK_SIZE)
        elif self.direction == Direction.DOWN:
            self.head = Coords(self.head.X, self.head.Y + self.BLOCK_SIZE)
        elif self.direction == Direction.LEFT:
            self.head = Coords(self.head.X - self.BLOCK_SIZE, self.head.Y)
        elif self.direction == Direction.RIGHT:
            self.head = Coords(self.head.X + self.BLOCK_SIZE, self.head.Y)

        self.history.insert(0, self.head)
        self.body = self.history[: self.length]

    def _handle_fruit(self):
        if self.fruit == self.head:
            self.length += 1
            self.history.insert(0, self.head)
            self.body = self.history[: self.length]
            self._make_fruit()

    def _is_dead(self):
        # if the snake is out of the screen
        if self.head.X - self.BLOCK_SIZE > self.width or self.head.X < 0:
            return True
        elif self.head.Y - self.BLOCK_SIZE > self.height or self.head.Y < 0:
            return True

        # if the snake hit itself
        if self.head in self.body:
            return True

        return False

    def _update_display(self):
        self.display.fill(BLACK)

        text = self.font.render(f"Score: {self.length}", False, (255, 255, 255))

        for part in self.body:
            pygame.draw.rect(
                self.display, GREEN, [part.X, part.Y, self.BLOCK_SIZE, self.BLOCK_SIZE],
            )

        pygame.draw.rect(
            self.display,
            RED,
            [self.fruit.X, self.fruit.Y, self.BLOCK_SIZE, self.BLOCK_SIZE],
        )

        self.display.blit(text, (0, 0))
        pygame.display.flip()
