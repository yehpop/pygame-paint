import pygame


class ToolBucket:
    # yapf: disable
    def __init__(self, palette_color, opacity):
        self.option_data = {
            'palette_color': pygame.Color(palette_color.r, palette_color.g, palette_color.b, 255),
            'opacity': opacity
        } # yapf: enable
