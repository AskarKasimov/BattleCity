import pygame
from button import Button


class Checkbox(Button):
    def __init__(self, surface, x, y, width, height, name, activated=False, color=(230, 230, 230)):
        super().__init__(surface, x, y, name, activated, color)
        self.width = width
        self.height = height
        self.checkbox_obj = pygame.Rect(self.x, self.y, self.width, self.height)
        self.checkbox_outline = self.checkbox_obj.copy()

    def render(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, (0, 0, 0), self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, (0, 0, 0), (self.x + 6, self.y + 6), 4)
        else:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, (0, 0, 0), self.checkbox_outline, 1)

    def update(self, event_object, others=None):
        if event_object.type == pygame.MOUSEBUTTONUP:
            x, y = event_object.pos
            px, py, w, h = self.checkbox_obj
            if px < x < px + w and py < y < py + h:
                if not self.checked:
                    self.checked = True
                    if others:
                        for i in others:
                            if i != self:
                                i.checked = False
                elif self.checked:
                    self.checked = False
