import pygame
from support import *
from setting import *

from entity import Entity

class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites, create_atack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.obstacle_sprites = obstacle_sprites
        self.rect = self.image.get_rect(topleft=pos)
        
        
        self.stats = {'health': 100, 'attack': 10, 'speed': 3}
        self.max_stats = {'health': 300, 'attack': 20, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'attack': 100, 'speed': 300}
        self.hitbox = self.rect.inflate(-10, -20)
        self.attacking = False
        self.attack_coldown = 500
        self.attack_time = 0
        self.create_atack = create_atack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]   

        self.healing = False
        self.healing_coldown = 400
        self.healing_time = 0

        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        self.health = self.stats['health']
        self.exp = 500
        self.speed = self.stats['speed']


        self.vulnerable = True
        self.hurt_time = None
        self.invicibility_duration = 500


        

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left' 
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_atack()
        
        if keys[pygame.K_LCTRL] and not self.healing:
            print('heal')
            self.healing_time = pygame.time.get_ticks()
            self.healing = True

    def coldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_coldown + weapon_data[self.weapon]['coldown']:
             self.attacking = False
             self.destroy_attack()
        if current_time - self.healing_time >= self.healing_coldown:
             self.healing = False
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invicibility_duration:
                self.vulnerable = True

    def import_player_assets(self): # функция для импорта анимаций персонажа
        character_path = "./sprites/player/"
        self.animation = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': []
        }
        for animation in self.animation.keys():
            full_path = character_path + animation
            self.animation[animation] = import_folder(full_path)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and '_idle' not in self.status and not 'attack' in self.status:
            self.status = self.status + '_idle'
        
        if self.attacking:
             self.direction.x = 0
             self.direction.y = 0
             if 'attack' not in self.status:
                self.status = self.status.rstrip('_idle')
                self.status = self.status + '_attack'
        else:
            self.status = self.status.replace('_attack', '')
    
    def get_full_weapon_damage(self):
        return self.stats['attack'] + weapon_data[self.weapon]['damage']    

    def update(self):
        self.input()
        self.coldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

    def animate(self):
        animation = self.animation[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
        else:
            alpha = 255
        self.image.set_alpha(alpha)
    
    def get_value_by_index(self, index):
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]
        
    

        



         