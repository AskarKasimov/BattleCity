import pygame as pg


class Button:
    def __init__(self, surface, x, y, width, height, name, activated=False, color=(230, 230, 230)):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.checkbox_obj = pg.Rect(self.x, self.y, self.width, self.height)
        self.checkbox_outline = self.checkbox_obj.copy()
        self.checked = activated
        self.click = False
        self.name = name

    def render(self):
        if self.checked:
            font = pg.font.Font(None, 24)
            text = font.render(self.name, True, (0, 0, 0))
            text_x = self.x
            text_y = self.y
            text_w = text.get_width()
            text_h = text.get_height()
            pg.draw.rect(self.surface, (255, 0, 0), (text_x - 7, text_y - 7,
                                                    text_w + 16, text_h + 12), 0)
            print("!!")
        else:
            font = pg.font.Font(None, 24)
            text = font.render(self.name, True, (0, 0, 0))
            text_x = self.x
            text_y = self.y
            text_w = text.get_width()
            text_h = text.get_height()
            pg.draw.rect(self.surface, self.color, (text_x - 7, text_y - 7,
                                                    text_w + 16, text_h + 12), 0)
            # print(pg.draw.rect(self.surface, self.color, (text_x - 7, text_y - 7,
            #                                               text_w + 16, text_h + 12), 0).width,
            #       pg.draw.rect(self.surface, self.color, (text_x - 7, text_y - 7,
            #                                               text_w + 16, text_h + 12), 0).height)
            self.surface.blit(text, (text_x, text_y))

    def update(self, event_object, others=None):
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
                    if others:
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
