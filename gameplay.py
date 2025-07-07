# состояние игры
#
#

import pygame
from base import BaseState
from player import Player
from cameraGroup import CameraGroup
from tile import Tile
from setting import *

import levelGenerator

class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pygame.Rect((0, 0), (80, 80))
        self.rect.center = self.screen_rect.center
        self.next_state = "GAME_OVER"
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()
        self.create_map()
        
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.visible_sprites.custom_drawn(self.player)
        self.visible_sprites.update()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP): # WORLD_MAP -- это карта уровня
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE # размер одного тайла
                y = row_index * TILESIZE
                if col == '#':
                    surface=pygame.image.load('sprites/wall.png')
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], sprite_type='visible', surface=surface)
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites) # добавление персонажа



    # def create_map(self):
    #     layouts = {
    #         'boundary': generat(),

    #     }
    #     for style, layout in layouts.items():
    #         for row_index, row in enumerate(layout): # WORLD_MAP -- это карта уровня
    #             for col_index, col in enumerate(row):
    #                 x = col_index * TILESIZE
    #                 y = row_index * TILESIZE
    #                 if style == 'boundary':
    #                     Tile((x,y), [self.visible_sprites, self.obstacles_sprites], sprite_type='visable', surface='sprites/wall.png')
    #                 # if col == '#':
    #                 #     Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
    #                 # if col == 'p':
    #                 #     self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites) # добавление персонажа
    # когда-нибудь можна доделать графику