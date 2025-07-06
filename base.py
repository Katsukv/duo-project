# Базовый класс состояния. От него наследуются все остальные состояния
# Здесь инициализируються базовые поля
# + Скорее всего здесь загружаются текстуры

import pygame

class BaseState(object):
    
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)
    
    def startup(self, persistant):
        self.persistant = persistant

    def update(self, dt):
        pass    

    def draw(self, surface):
        pass

    def get_event(self, event):
        pass
    