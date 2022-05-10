import pygame

from game import SnakeGame

if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    
    running=True
    while running:
        running = game.play_step()