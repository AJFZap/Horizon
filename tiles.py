"""
Holds every data corresponding to the tile generation.
"""
from kivy.graphics import Color, Quad
from random import randint
def draw_tiles(self):
    """
    Draws the tiles that will serve as the track in the game. And stores them in the tiles array.
    """
    with self.canvas:
        Color(1,1,1,1)

        for i in range(0, self.amount_of_tiles):
            self.tiles.append(Quad()) # A quad has 4 different coordinates, that is why I use it for this game that has a fading point perspective.

def get_tile_coordinate(self, ti_x, ti_y): # ti means Tile Index.
        """
        Returns the coordinates of the tile.
        """
        ti_y -= self.current_y_loop
        x = self.get_x_index(ti_x)
        y = self.get_y_index(ti_y)

        return x, y

def generate_tile_coordinates(self):
    """
    Generates coordinates for each needed tile and stores them in the tiles_coordinates array.
    """
    last_y = 0 # This variables will store the next tile number to be created, needed to make the infinite track.
    last_x = 0

    start_index =-int(self.amount_vertical_lines)/2 + 1
    end_index = start_index + self.amount_vertical_lines - 1

    # Removes the coordinates of the tiles that are outside of the screen.
    for i in range(len(self.tiles_coordinates)-1, -1, -1): # Minus 1 so it doesn't step out of range.
        if self.tiles_coordinates[i][1] < self.current_y_loop:
            del self.tiles_coordinates[i]

    if len(self.tiles_coordinates) > 0:
        last_coordinate = self.tiles_coordinates[-1] # Gets the last coordinate stored in the tiles coordinate.
        last_x = last_coordinate[0]  # We keep the same X, so is not needed to add a plus 1.
        last_y = last_coordinate[1] + 1 # Takes the value of Y of the last coordinate and gives it a plus 1 to know wich is next.

    for i in range(len(self.tiles_coordinates), self.amount_of_tiles): # We range from the length of the tiles_coordinates cause we want to create just enough tiles to fill it.
            
            rand = randint(0, 2) # Random generation of tiles.
            
            self.tiles_coordinates.append((last_x, last_y))

            # Start face, just a straight line
            while last_y < 15:
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1

            # Executes only once at the end of the start straight fase.
            if last_y == 16:
                self.tiles_coordinates.append((last_x, 16))
                self.tiles_coordinates.append((0, 15))

            # Starts the random generation of tiles.
            if rand == 0:
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y)) # Append tuples 'cause they are coordinates.
            elif rand == 1:
                last_x += 1
                if last_x > end_index - 1: # -1 Because otherway is will go outside the line by one tile.
                    last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            else:
                last_x -= 1
                if last_x < start_index:
                    last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

def update_tiles(self):
    """
    Gives the needed coordinates to the tiles.
    """
    for i in range(0, self.amount_of_tiles):
        tile = self.tiles_coordinates[i]
        xmin, ymin = self.get_tile_coordinate(tile[0], tile[1]) # Left bottom corner of the Quad.
        xmax, ymax = self.get_tile_coordinate(tile[0] +1, tile[1] +1) # Top right corner of the Quad.

        # First the bottom left, then the top left, followed by the right top and finally the bottom right.
        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4] # Give the points to the Quad.