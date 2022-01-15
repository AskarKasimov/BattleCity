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

    def update(self, event_object, others=None):
        if event_object.type == pg.MOUSEBUTTONDOWN:
            x, y = event_object.pos
            px, py, w, h = self.checkbox_obj
            if px < x < px + w and py < y < py + h:
                self.click = True
            print(self.click, self.checked)
        if event_object.type == pg.MOUSEBUTTONUP:
            x, y = event_object.pos
            px, py, w, h = self.checkbox_obj
            if px < x < px + w and py < y < py + h:
                if not self.checked and self.click:
                    self.checked = True
                    if others:
                        for i in others:
                            if i != self:
                                i.checked = False
                elif self.checked:
                    self.checked = False