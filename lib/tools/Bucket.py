import pygame


class ToolBucket:
    # yapf: disable
    def __init__(self, paletteColor, opacity):
        self.option_data = {
            'palette_color': pygame.Color(paletteColor.r, paletteColor.g, paletteColor.b, 255),
            'opacity': opacity
        } # yapf: enable
