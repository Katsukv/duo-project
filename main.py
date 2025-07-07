# main он и в C++ main. Здесь запуск класса Game
# и какая-то начальная инициализация
#


import sys
import pygame

from menu import Menu
from splash import Splash
from gameplay import Gameplay
from game_over import GameOver

from setting import *

from game import Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

states = {
    "MENU":Menu(),
    "SPLASH":Splash(),
    "GAMEPLAY":Gameplay(),
    "GAME_OVER":GameOver(),
}

game = Game(screen, states, "SPLASH")
game.run()


pygame.quit()
sys.exit()