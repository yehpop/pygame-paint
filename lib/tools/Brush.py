import pygame
from lib.tools.UndoRecord import UndoRecord


class ToolBrush:
    """
    Object of this class is a brush. And this class has very complicated coding that even I don't get lol.
    But, the way the painting thing works is it uses an algorithm to draw lines instead of just painting
    a circle around the cursor whenever you press the mouse button. And well it changes the size, color, etc.
    in the _refresh_brush method..
    
    :param paletteColor: color of brush
    :param opacity: opacity of brush
    :param brushSize: size of brush
    """
    def __init__(self, paletteColor, opacity, brushSize):
        # yapf: disable
        self.option_data = {
            'palette_color':pygame.Color(paletteColor.r, paletteColor.g, paletteColor.b, 255),
            'opacity': opacity,
            'brush_size': brushSize
        } #yapf: enable

        self._brushArea = 4
        self.centerPos = (0,0)
        self.startPainting = False
        self.painting = False
        self.paintedArea = None
        self.reltPaintedArea = None
        self.newRectsToBlit = []

        self.preSurface = None
        self.tempSurface = None
        self.opacitySurface = None

        self.image = None

        self.activeCanvas = None

        self._refresh_brush()

    def set_option(self, optionID, value):
        if optionID in self.option_data:
            self.option_data[optionID] = value
            self._refresh_brush()

    def _refresh_brush(self):
        """
        refresh the brush to match the new values of its options
        """
        padding = 8  # I actually don't know what it does but, padding i guess..?
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
        pygame.transform.smoothscale(_surface,
                                     (self.option_data['brush_size']+padding,
                                      self.option_data['brush_size']+padding),
                                     self.image)

    def process_canvas(self, event, canvas, mousePos):
        eventConsumed = False
        xPos = mousePos[0]
        yPos = mousePos[1]

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if canvas.hover_point(xPos, yPos):
                if not self.painting:
                    self.startPainting = True
                    eventConsumed = True
        return eventConsumed

    def process_event(self, event):
        eventConsumed = False
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if self.painting:
                self.painting = False

                if self.activeCanvas is not None:
                    undoSurf = pygame.Surface(self.reltPaintedArea.size,
                                               flags=pygame.SRCALPHA)
                    undoSurf.blit(self.preSurface,
                                   (0, 0), self.reltPaintedArea)
                    self.activeCanvas.undoStack.append(UndoRecord(undoSurf,
                                                                    self.reltPaintedArea))
                    self.activeCanvas.redoStack.clear()
                    if len(self.activeCanvas.undoStack) > 25:
                        self.activeCanvas.undoStack.pop(0)

                self.reltPaintedArea = None
                self.opacitySurface = None
                self.preSurface = None
                self.paintedArea = None
                self.tempSurface = None

        return eventConsumed

    def update(self, timeDelta, canvasSurface, canvasPos, canvas):
        # frick this is gonna be long
        newPos = pygame.mouse.get_pos()

        if self.startPainting:
            self.startPainting = False
            self.centerPos = newPos
            self.preSurface = canvasSurface.copy()

            self.paintedArea = pygame.Rect((0,0), self.image.get_size())
            self.paintedArea.center = newPos

            self.newRectsToBlit.append(self.paintedArea.copy())
            self.painting = True
        # this part is veryyy long
        if self.painting:
            point = ToolBrush._line(self.centerPos, newPos)
            point.add(newPos)
            if len(point) > 0:
                if self.centerPos in point:
                    point.remove(self.centerPos)
                for p in point:
                    if canvas.hover_point(p[0], p[1]):
                        newRect = pygame.Rect((0,0), self.image.get_size())
                        newRect.center = p
                        self.newRectsToBlit.append(newRect)
                newPaintedAreaRect = self.paintedArea.unionall(self.newRectsToBlit)
            else:
                newPaintedAreaRect = self.paintedArea

            newTempSurface = pygame.Surface(newPaintedAreaRect.size,
                                                       flags=pygame.SRCALPHA,
                                                       depth=32)
            newTempSurface.fill(pygame.Color(self.option_data['palette_color'].r,
                                                        self.option_data['palette_color'].g,
                                                        self.option_data['palette_color'].b,
                                                        0))
            if self.tempSurface is not None:
                newTempSurface.blit(self.tempSurface,
                                               (self.paintedArea.left - newPaintedAreaRect.left,
                                                self.paintedArea.top - newPaintedAreaRect.top))
            self.paintedArea = newPaintedAreaRect
            self.tempSurface = newTempSurface

            self.opacitySurface = pygame.Surface(self.paintedArea.size,
                                                  flags=pygame.SRCALPHA,
                                                  depth=32)
            self.opacitySurface.fill(pygame.Color(255,255,255, self.option_data['opacity']))

            for blitRect in self.newRectsToBlit:
                blitRect.left -= self.paintedArea.left
                blitRect.top -= self.paintedArea.top
                self.tempSurface.blit(self.image, blitRect)

            self.newRectsToBlit = []

            canvasSurface.blit(self.preSurface, (0,0))
            preBlend = self.tempSurface.copy()
            preBlend.blit(self.opacitySurface, (0, 0),
                           special_flags=pygame.BLEND_RGBA_MULT)

            self.reltPaintedArea = self.paintedArea.copy()
            self.reltPaintedArea.topleft = (self.paintedArea.left - canvasPos[0],
                                            self.paintedArea.top - canvasPos[1])
            canvasSurface.blit(preBlend, self.reltPaintedArea)
            canvas.set_image(canvasSurface)

        self.centerPos = newPos

    # first time making static methods
    @staticmethod
    def _line(point1, point2):
        x0, x1 = point1[0], point2[0]
        y0, y1 = point1[1], point2[1]
        if abs(x1 - x0) > abs(y1 - y0):
            if x0 > x1:
                _points = ToolBrush._line_low(x1, y1, x0, y0)
            else:
                _points = ToolBrush._line_low(x0, y0, x1, y1)
        else:
            if y0 > y1:
                _points = ToolBrush._line_high(x1, y1, x0, y0)
            else:
                _points = ToolBrush._line_high(x0, y0, x1, y1)
        return _points


    @staticmethod
    def _line_low(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        d = 2 * dy - dx
        y = y0

        _points = set()
        for x in range(x0, x1):
            _points.add((x, y))
            if 0 < d:
                y = y + yi
                d = d - 2 * dx
            d = d + 2 * dy
        return _points

    @staticmethod
    def _line_high(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        d = 2 * dx - dy
        x = x0

        _points = set()
        for y in range(y0, y1):
            _points.add((x, y))
            if 0 < d:
                x = x + xi
                d = d - 2 * dy
            d = d + 2 * dx
        return _points