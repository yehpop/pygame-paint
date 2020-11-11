import pygame


class ToolBucket:
    def __init__(self, paletteColor, opacity):
        # yapf: disable
        self.option_data = {
            'palette_color': pygame.Color(paletteColor.r, paletteColor.g, paletteColor.b, 255),
            'opacity': opacity
        }  # yapf: enables
