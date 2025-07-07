import pygame



class Player(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('sprites/player_tmp.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100, 200))
        

    def input(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.rect.move_ip(0, -10)
            if keys[pygame.K_DOWN]:
                self.rect.move_ip(0, 10)
            if keys[pygame.K_LEFT]:
                self.rect.move_ip(-10,0)
            if keys[pygame.K_RIGHT]:
                 self.rect.move_ip(10, 0)
    
    def update(self):
         self.input()