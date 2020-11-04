import pygame


class ToolBrush:
    def __init__(self, palette_color, opacity, brush_size):
        # yapf: disable
        self.option_data = {
            'palette_color':pygame.Color(palette_color.r, palette_color.g, palette_color.b, 255),
            'opacity': opacity,
            'brush_size': brush_size
        } #yapf: enable
