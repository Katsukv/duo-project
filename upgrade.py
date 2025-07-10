import pygame

from setting import *


class Upgrade():

    def __init__(self, player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True

    
    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def coldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 300:
            self.can_move = True

    def display(self):
        self.input()
        self.coldown()

        for index, item in enumerate(self.items_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

    def create_items(self):
        self.items_list = []

        for index, item in enumerate(range(self.attribute_nr)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr 
            left = (item * increment) + (increment - self.width) // 2
            top = HEIGHT * 0.1
            item = Item(left, top, self.width, self.height, index, self.font)
            self.items_list.append(item)




class Item:

    def __init__(self, l, t, w, h, index, font):
        
        self.rect = pygame.Rect(l, t, w, h)
        self.inidex = index
        self.font = font

    
    def display(self, surface, selection_number, name, value, max_value, cost):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)

