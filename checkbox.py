import pygame as pg
import button


class Checkbox(button.Button):
    def render(self):
        if self.checked:
            pg.draw.rect(self.surface, self.color, self.checkbox_obj)
            pg.draw.rect(self.surface, (0, 0, 0), self.checkbox_outline, 1)
            pg.draw.circle(self.surface, (0, 0, 0), (self.x + 6, self.y + 6), 4)
        else:
            pg.draw.rect(self.surface, self.color, self.checkbox_obj)
            pg.draw.rect(self.surface, (0, 0, 0), self.checkbox_outline, 1)