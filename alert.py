import pygame
from button import Button


class Alert(Button):
    def __init__(self, surface, x, y, width, height, name, subtext, color=(230, 230, 230)):
        super().__init__(surface, x, y, width, height, name, color)
        self.subtext = subtext

