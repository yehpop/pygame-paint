import json
import pygame
import pygame_gui as gui

from lib import CanvasWindow, MenuBar, ToolBar
from MenuBarEvents import MenuBarEvents


class PygamePaint:
    def __init__(self):
        pygame.init()
        # the main window stuff
        pygame.display.set_caption("Paint")
        self.dimensionA = (800, 600)
        titleIcon = pygame.image.load("res\\paint_icon.png")
        pygame.display.set_icon(titleIcon)
        self.mainWindow = pygame.display.set_mode(self.dimensionA)
        self.background = pygame.Surface(self.dimensionA)
        self.background.fill(pygame.Color("#3d3a3a"))

        self.newTheme = None
        theme = self.read_json('res\\default_theme.json')
        self.write_to(theme)
        self.themePath = "res\\theme.json"
        self.manager = gui.UIManager((self.dimensionA),
                                     theme_path=self.themePath,
                                     enable_live_theme_updates=True)
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
                    '#theme': {
                        'display_name': 'Theme'
                    },
                    '#workspace': {
                        'display_name': 'Window...'
                    },
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

        rectMB = pygame.Rect((0, 0), (800, 25))
        self.menuBar = MenuBar(rectMB, menuData, self.manager)

        rectTB = pygame.Rect((0, 75), (200, 475))
        self.toolBar = ToolBar(rectTB, self.manager)

        self.eventHandler = MenuBarEvents(self.mainWindow, self.manager)

        self.clock = pygame.time.Clock()
        self.isRunning = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

        self.eventHandler.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == 'theme_changed':
            self.change_theme(event)

        if event.type == pygame.USEREVENT and event.user_type == 'canvas_window_created':
            pass

    def change_theme(self, event):
        if self.newTheme is not None:
            self.newTheme.clear()
        self.newTheme = self.read_json(event.theme_path)
        self.write_to(self.newTheme)
        if event.theme_path == 'res\\light_theme.json':
            self.background.fill(pygame.Color("#D3D3D3"))
        elif event.theme_path == 'res\\default_theme.json':
            self.background.fill(pygame.Color('#3d3a3a'))
        else:
            self.background.fill(pygame.Color("#301934"))
        print("theme change attempted...")

    def start(self):  # loop
        while self.isRunning:
            timeDelta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                self.on_event(event)  # to make it look cleaner ig

                self.manager.process_events(event)

            self.manager.update(timeDelta)

            self.mainWindow.blit(self.background, (0, 0))

            self.manager.draw_ui(self.mainWindow)

            pygame.display.update()

    @staticmethod
    def read_json(path="res\\theme.json"):
        with open(path) as file:
            read = json.load(file)
        return read

    @staticmethod
    def write_to(obj, path="res\\theme.json"):
        try:
            with open(path, "w+") as file:
                json.dump(obj, file, indent=4)
        except:
            print("İşlem başarısız...")
            return False
        return True
