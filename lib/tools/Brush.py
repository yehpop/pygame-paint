import pygame


class ToolBrush:
    def __init__(self, paletteColor, opacity, brushSize):
        # yapf: disable
        self.option_data = {
            'palette_color':pygame.Color(paletteColor.r, paletteColor.g, paletteColor.b, 255),
            'opacity': opacity,
            'brush_size': brushSize
        } #yapf: enable

        self._brushArea = 4
        self.centerPos = (0,0)
        self.painting = False

        self.image = None

        self._refresh_brush()

    def set_option(self, optionID, value):
        if optionID in self.option_data:
            self.option_data[optionID] = value
            self._refresh_brush()

    def _refresh_brush(self):
        padding = 8
        self.image = pygame.Surface((self.option_data['brush_size'] + padding,
                                     self.option_data['brush_size'] + padding),
                                    flags=pygame.SRCALPHA,
                                    depth=32)
        _brushSize = self.option_data['brush_size'] * self._brushArea
        _padding = padding * self._brushArea
        _surface = pygame.Surface((_brushSize + _padding, _brushSize + _padding), flags=pygame.SRCALPHA, depth=32)
        _surface.fill(pygame.Color(self.option_data['palette_color'].r,
                                     self.option_data['palette_color'].g,
                                     self.option_data['palette_color'].b, 0))
        pygame.draw.circle(_surface,
                           pygame.Color(self.option_data['palette_color'].r,
                                        self.option_data['palette_color'].g,
                                        self.option_data['palette_color'].b, 85),
                           (int((_brushSize + _padding) / 2),
                            int((_brushSize + _padding) / 2)),
                           int(_brushSize / 2) + int(self._brushArea * 0.5))
        pygame.draw.circle(_surface,
                           pygame.Color(self.option_data['palette_color'].r,
                                        self.option_data['palette_color'].g,
                                        self.option_data['palette_color'].b, 175),
                           (int((_brushSize + _padding) / 2),
                            int((_brushSize + _padding) / 2)),
                           int(_brushSize / 2))
        pygame.draw.circle(_surface,
                           pygame.Color(self.option_data['palette_color'].r,
                                        self.option_data['palette_color'].g,
                                        self.option_data['palette_color'].b, 255),
                           (int((_brushSize + _padding) / 2),
                            int((_brushSize + _padding) / 2)),
                           int(_brushSize / 2) - int(self._brushArea * 0.5))
