# состояние игры
#
#

import pygame
from base import BaseState
from player import Player
from cameraGroup import CameraGroup
from tile import Tile
from setting import *
from weapon import Weapon
from ui import UI
from enemy import Enemy
from background import BackGround

from levelGenerator import get_matrix_of_level

class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pygame.Rect((0, 0), (80, 80))
        self.rect.center = self.screen_rect.center
        self.next_state_posible = {pygame.K_ESCAPE: "GAME_OVER", pygame.K_m: "MENU"}
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()

        self.start_pos_x = 0
        self.start_pos_y = 0

        self.create_map()
        surface = pygame.image.load('sprites/background.png')
        self.visible_sprites.load_bg(surface)
        self.ui = UI()

        self.current_attack = 0
        
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.next_state = self.next_state_posible[pygame.K_m]
                self.done = True
            if event.key == pygame.K_ESCAPE:
                self.next_state = self.next_state_posible[pygame.K_ESCAPE]
                self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.visible_sprites.custom_drawn(self.player, self.start_pos_x, self.start_pos_y)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

    def create_map(self):
        size_x = 0
        size_y = 0
        for row_index, row in enumerate(get_matrix_of_level()[0]): # WORLD_MAP -- это карта уровня
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE # размер одного тайла
                y = row_index * TILESIZE
                size_x = max(x, size_x)
                size_y = max(y, size_y)
                if col == '#':
                    surface=pygame.image.load('sprites/wall.png')
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], sprite_type='visible', surface=surface)
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack) # добавление персонажа
                    surface = pygame.image.load('sprites/floor.png')
                    if self.start_pos_x == 0:
                        self.start_pos_y = y
                        self.start_pos_x = x
                    BackGround((x, y), [self.background_sprites], surface)
                if col == 'm':
                    if self.start_pos_x == 0:
                        self.start_pos_x = x
                        self.start_pos_y = y
                    Enemy('spirit', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.damage_player, self.add_exp)
                    surface = pygame.image.load('sprites/floor.png')
                    BackGround((x, y), [self.background_sprites], surface)
                if col == '*':
                    if self.start_pos_x == 0:
                        self.start_pos_x = x
                        self.start_pos_y = y
                    surface = pygame.image.load('sprites/floor.png')
                    BackGround((x, y), [self.background_sprites], surface)
        com_surf = pygame.Surface((size_x, size_y))
        self.background_sprites.draw(com_surf)
        pygame.image.save(com_surf, 'sprites/background.png')
                    


    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
    
    def add_exp(self, amount):
        self.player.exp += amount

