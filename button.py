import pygame as pg


class Button:
    def __init__(self, surface, x, y, name, activated=False, color=(230, 230, 230)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.checkbox_obj = pg.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()
        self.checked = activated
        self.click = False
        self.name = name

    def render_checkbox(self):
        if self.checked:
            pg.draw.rect(self.surface, self.color, self.checkbox_obj)
            pg.draw.rect(self.surface, (0, 0, 0), self.checkbox_outline, 1)
        else:
            pg.draw.rect(self.surface, self.color, self.checkbox_obj)
            pg.draw.rect(self.surface, (0, 0, 0), self.checkbox_outline, 1)

    def update(self, event_object, others):
        if event_object.type == pg.MOUSEBUTTONDOWN:
            x, y = event_object.pos
            px, py, w, h = self.checkbox_obj
            if px < x < px + w and py < y < py + w:
                self.click = True
        if event_object.type == pg.MOUSEBUTTONUP:
            x, y = event_object.pos
            px, py, w, h = self.checkbox_obj
            if px < x < px + w and py < y < py + w:
                if not self.checked and self.click:
                    self.checked = True
                    for i in others:
                        if i != self:
                            i.checked = False
                elif self.checked:
                    self.checked = False

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False