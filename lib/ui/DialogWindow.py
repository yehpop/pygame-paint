import pygame

from pygame_gui.elements import UIWindow, UILabel, UITextEntryLine, UIButton
from pygame_gui import UI_BUTTON_PRESSED, UI_TEXT_ENTRY_FINISHED, UI_TEXT_ENTRY_CHANGED


class NewCanvasDialog(UIWindow):
    def __init__(self, rect, manager):
        super().__init__(rect,
                         manager,
                         'Create a New Canvas',
                         object_id='#new_canvas',
                         resizable=False)
        UILabel(pygame.Rect((10, 20), (80, 30)),
                'Image Size',
                self.ui_manager,
                self,
                object_id='#small_header_label')

        UILabel(pygame.Rect((20, 60), (56, 30)), 'Width:', self.ui_manager,
                self)

        UILabel(pygame.Rect((20, 100), (56, 30)), 'Height:', self.ui_manager,
                self)

        initWidth = 512
        initHeight = 512

        self.currentColor = pygame.Color(255, 255, 255)
        self.maxWidth = 4096
        self.maxHeight = 4096

        self.widthEntry = UITextEntryLine(pygame.Rect((86, 60), (50, 30)),
                                          self.ui_manager, self)
        self.widthEntry.set_allowed_characters('numbers')
        self.widthEntry.set_text(str(initWidth))
        self.widthEntry.set_text_length_limit(4)

        self.heightEntry = UITextEntryLine(pygame.Rect((86, 100), (50, 30)),
                                           self.ui_manager, self)
        self.heightEntry.set_allowed_characters('numbers')
        self.heightEntry.set_text(str(initHeight))
        self.heightEntry.set_text_length_limit(4)

        self.okButton = UIButton(pygame.Rect((-220, -40), (100, 30)),
                                 'OK',
                                 self.ui_manager,
                                 self,
                                 object_id='#ok_button',
                                 anchors={
                                     'left': 'right',
                                     'right': 'right',
                                     'top': 'bottom',
                                     'bottom': 'bottom'
                                 })

        self.cancelButton = UIButton(pygame.Rect((-110, -40), (100, 30)),
                                     'Cancel',
                                     self.ui_manager,
                                     self,
                                     object_id='#cancel_button',
                                     anchors={
                                         'left': 'right',
                                         'right': 'right',
                                         'top': 'bottom',
                                         'bottom': 'bottom'
                                     })

    def process_event(self, event: pygame.event.Event) -> bool:
        eventConsumed = super().process_event(event)
        # ↓↓↓ buttons ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_PRESSED
                and event.ui_element == self.okButton):
            # yapf: disable
            pygame.event.post(
                pygame.event.Event(
                    pygame.USEREVENT,
                    {
                        'user_type': 'canvas_window_created',
                        'ui_element': self.most_specific_combined_id,
                        'ui_object_id': self,
                        'size': (min(int(self.widthEntry.get_text()), self.maxWidth),
                                min(int(self.heightEntry.get_text()), self.maxHeight)),
                        'color': self.currentColor
                    }))
            self.kill()
            # yapf: enable
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_PRESSED
                and event.ui_element == self.cancelButton):
            self.kill()

        # ↓↓↓ text entries ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_TEXT_ENTRY_FINISHED):
            if event.ui_element == self.widthEntry:
                try:
                    intValue = int(self.widthEntry.get_text())
                except ValueError:
                    intValue = 0
                    self.widthEntry.set_text(str(intValue))

                if intValue > self.maxWidth:
                    self.widthEntry.set_text(str(self.maxWidth))
            elif event.ui_element == self.heightEntry:
                try:
                    intValue = int(self.heightEntry.get_text())
                except ValueError:
                    intValue = 0
                    self.heightEntry.set_text(str(intValue))

                if intValue > self.maxHeight:
                    self.heightEntry.set_text(str(self.maxHeight))
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_TEXT_ENTRY_CHANGED):
            try:
                int(event.ui_element.get_text())
            except ValueError:
                event.ui_element.set_text(0)

        return eventConsumed
