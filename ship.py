"""
Holds all the ship needs.
"""
from kivy.graphics import Color, Triangle

def draw_ship(self):
        """
        Makes the triangle that represents the player space ship.
        """
        with self.canvas:
            Color(0,0,0,1)

            self.ship = Triangle()

def update_ship(self):
    """
    Draws and updates the ship.
    """
    # Updates the coordinates of the three points of the ship.
    self.ship_coordinates[0] = (self.width/2 - self.ship_width/2 * self.width, self.height* self.ship_base)
    self.ship_coordinates[1] = (self.width/2, self.ship_height* self.height + self.height* self.ship_base)
    self.ship_coordinates[2] = (self.width/2 + self.ship_width/2 * self.width, self.height* self.ship_base)
    
    # A triangle takes 6 coordinates / 3 points. The "*" before the self.ship_coordinates indicates that it is a tuple and it will give both variables stored inside.
    x1, y1 = self.transform(*self.ship_coordinates[0]) # Left point.
    x2, y2 = self.transform(*self.ship_coordinates[1])  # Middle point.
    x3, y3 = self.transform(*self.ship_coordinates[2]) # Right point.

    self.ship.points = [x1,y1,x2,y2,x3,y3]

def check_ship_collision(self):
    for i in range(0, len(self.tiles_coordinates)):
        ti_x, ti_y = self.tiles_coordinates[i]

        if ti_y > self.current_y_loop + 2: # TODO Don't quite understand why it work perfectly with +2 but not with +1 after the initial straight track.
            return False
        if self.detect_collision(ti_x, ti_y):
            return True
    
    return False