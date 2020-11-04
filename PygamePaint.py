import pygame
import pygame_gui as gui

from ui.CanvasWindow import CanvasWindow
from ui.MenuBar import MenuBar
from ui.ToolBar import ToolBar

from MenuBarEvents import MenuBarEvents


class PygamePaint:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Paint")
        dimensionA = (800, 600)
        self.mainWindow = pygame.display.set_mode(dimensionA)
        self.background = pygame.Surface(dimensionA)
        self.background.fill(pygame.Color("#3d3a3a"))

        self.manager = gui.UIManager((dimensionA),
                                     theme_path="data\\theme.json")
        menuData = {
            '#file_menu': {
                'display_name': 'File',
                'items': {
                    '#new': {
                        'display_name': 'New...'
                    },
                    '#open': {
                        'display_name': 'Open...'
                    },
                    '#save': {
                        'display_name': 'Save'
                    },
                    '#save_as': {
                        'display_name': 'Save As...'
                    }
                }
            },
            '#edit_menu': {
                'display_name': 'Edit',
                'items': {
                    '#undo': {
                        'display_name': 'Undo'
                    },
                    '#redo': {
                        'display_name': 'Redo'
                    }
                }
            },
            '#view_menu': {
                'display_name': 'View',
                'items': {
                    '#info': {
                        'display_name': 'Image info'
                    }
                }
            },
            '#help_menu': {
                'display_name': 'Help',
                'items': {
                    '#about': {
                        'display_name': 'About'
                    }
                }
            }
        }  # menu bar'daki diğer menüler için

        self.clock = pygame.time.Clock()
        self.isRunning = True

    def start(self):  # loop
        while self.isRunning:
            timeDelta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

                self.manager.process_events(event)
            self.manager.update(timeDelta)

            self.mainWindow.blit(self.background, (0, 0))
            self.manager.draw_ui(self.mainWindow)

            pygame.display.update()
