from kivy.uix.relativelayout import RelativeLayout

class GameOver(RelativeLayout):
    def on_touch_down(self, touch):
        """
        Deactivates the buttons from the menu when the opacity is 0 to not be able to click on play or quit when a game over state happens.
        """
        if self.opacity == 0:
            return True
        
        return super(RelativeLayout, self).on_touch_down(touch)