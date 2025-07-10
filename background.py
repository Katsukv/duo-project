import pygame



class BackGround(pygame.sprite.Sprite):

    def __init__(self, pos, groups, surface):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
