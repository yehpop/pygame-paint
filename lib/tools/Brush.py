import pygame


class ToolBrush:
    def __init__(self, paletteColor, opacity, brushSize):
        # yapf: disable
        self.option_data = {
            'palette_color':pygame.Color(paletteColor.r, paletteColor.g, paletteColor.b, 255),
            'opacity': opacity,
            'brush_size': brushSize
        } #yapf: enable
