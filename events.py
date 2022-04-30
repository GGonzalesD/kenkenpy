
import pygame, sys
import pygame.locals as lcs

class EventCtrl:
    def __init__(self):
        self.keys = {}
        self.buttons = {}
        self.number = ""
        self.text = ""
    
    def reset(self):
        self.number = ""
        self.text = ""

    def key_down(self, key):
        return key in self.keys and self.keys[key] == 0
    def key_press(self, key):
        return key in self.keys and self.keys[key] >= 0
    def mouse_down(self, btn):
        return btn in self.buttons and self.buttons[btn] == 0
    def mouse_press(self, btn):
        return btn in self.buttons and self.buttons[btn] >= 0
    def mouse_up(self, btn):
        return btn in self.buttons and self.buttons[btn] == -1

    def update_logs(self):
        for i in list(self.buttons.keys()):
            if self.buttons[i] == -1:
                self.buttons.pop(i)
            else:
                self.buttons[i] += 1
        for i in list(self.keys.keys()):
            if self.keys[i] == -1:
                self.keys.pop(i)
            else:
                self.keys[i] += 1

    def onkey(self, key:chr):
        if key < 0x110000 and chr(key).isprintable():
            self.text += chr(key)
        if key >= 48 and key <= 57:
            self.number += chr(key)
        if key == 8:
            self.number = self.number[:-1]
            self.text = self.text[:-1]

    def update(self, events):
        self.update_logs()
        for event in events:
            event:pygame.event.Event
            if event.type == lcs.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == lcs.KEYDOWN:
                if not event.key in self.keys:
                    self.keys[event.key] = 0
                    self.onkey(event.key)
            if event.type == lcs.KEYUP:
                self.keys[event.key] = -1

            if event.type == lcs.MOUSEBUTTONDOWN:
                if not event.button in self.keys:
                    self.buttons[event.button] = 0
            if event.type == lcs.MOUSEBUTTONUP:
                self.buttons[event.button] = -1
            