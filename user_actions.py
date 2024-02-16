"""
File that holds the logic of key presses and such.
"""
from kivy.uix.relativelayout import RelativeLayout

def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.speed_x = 2
    elif keycode[1] == 'right':
        self.speed_x = -2
    return True

def on_keyboard_up(self, keyboard, keycode):
    self.speed_x = 0

def on_touch_down(self, touch):
        """
        Makes the camera move on the X axis to the left or the right depending where the mouse click has been pressed.
        """
        if not self.game_over and self.game_start:
            if touch.x < self.width/2:
                self.speed_x = 2

            else:
                self.speed_x = -2
        
        return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    """
    Makes the camera stop moving in the X axis.
    """
    self.speed_x = 0