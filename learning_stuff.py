import pygame
import pygame_gui as gui

pygame.init()

pygame.display.set_caption('Big Button')

windowSurface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#3d3a3a'))

manager = gui.UIManager((800, 600), "data\\button_theme.json")
# yapf: disable
helloButton = gui.elements.UIButton(relative_rect=pygame.Rect((300, 200), (200, 200)),
                                            text='Say Hello',
                                            manager=manager)
# yapf: enable
clock = pygame.time.Clock()
isRunning = True

while isRunning:
    timeDelta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        if event.type == pygame.USEREVENT:
            if event.user_type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == helloButton:
                    print('Hello World!')

        manager.process_events(event)
    manager.update(timeDelta)

    windowSurface.blit(background, (0, 0))
    manager.draw_ui(windowSurface)

    pygame.display.update()