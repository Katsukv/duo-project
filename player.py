import pygame



class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/32x32.png').convert_alpha()
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