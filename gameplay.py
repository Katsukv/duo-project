# состояние игры
#
#

import pygame
from base import BaseState
from player import Player


class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pygame.Rect((0, 0), (80, 80))
        self.rect.center = self.screen_rect.center
        self.next_state = "GAME_OVER"
        self.player = pygame.sprite.GroupSingle(Player())

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.player.draw(surface)
        self.player.update()
