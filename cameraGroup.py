import pygame


class CameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.ground_surface = pygame.image.load("sprites/Tokyo Night Abstract.png")
        self.ground_rect = self.ground_surface.get_rect(topleft=(0,0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
    
        
    def custom_drawn(self, player):

        self.center_target_camera(player) # something wrong
        # сначала надо будет рисовть фон

        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surface, ground_offset)
        print(len(self.sprites()))
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos) 
