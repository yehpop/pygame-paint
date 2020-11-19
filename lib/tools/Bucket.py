import pygame


class ToolBucket:
    def __init__(self, paletteColor, opacity):
        # yapf: disable
        self.option_data = {
            'palette_color': pygame.Color(paletteColor.r, paletteColor.g, paletteColor.b, 255),
            'opacity': opacity
        }  # yapf: enables


    def set_option(self, optionID, value):
        if optionID in self.option_data:
            self.option_data[optionID] = value

    def process_canvas(self, event, canvas, mousePos):
        pass

    def update(self, timeDelta, canvasSurface, canvasPos, canvas):
        pass

    def process_event(self, event):
        pass