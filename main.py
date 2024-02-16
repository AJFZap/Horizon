from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.lang.builder import Builder

from kivy import platform
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, Clock, ObjectProperty
from kivy.graphics import Line, Color
from kivy.core.window import Window

Builder.load_file("menu.kv")
Builder.load_file("gameover.kv")

class HorizonGame(RelativeLayout):
    from transform import transform, transform_2D, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    from tiles import draw_tiles, get_tile_coordinate, update_tiles, generate_tile_coordinates
    from ship import draw_ship, check_ship_collision, update_ship
    from audio import init_audio
    
    # Two variables to store the perspective points that can be used in the Kivy file.
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    # Creates a list of vertical lines and the space between them.
    amount_vertical_lines = 10
    space_between_vertical_lines = .25 # Percentage of the window width (10%).
    vertical_lines = []
    current_offset_x = 0
    speed_x = 0 

    # Creates a list of horizontal lines and the space between them.
    amount_horizontal_lines = 11
    space_between_horizontal_lines = .3 # Percentage of the window width (20%).
    horizontal_lines = []
    current_offset_y = 0 # This one makes the horizontal lines make de ilusion of moving towards the player possible.
    speed = 2 # Speed at wich the horizontal lines go towards the camera.

    # Creates the tiles that will serve as the games track.
    amount_of_tiles = 20
    tiles = []
    tiles_coordinates = []
    current_y_loop = 1

    # Creates the player space ship.
    ship = None
    ship_width = 0.1       # Percentages for both the width and height of the ship depending of the screen measures.
    ship_height = 0.035      
    ship_base = 0.04       # Distance between the bottom of the tile and the base of the ship.
    ship_coordinates = [(0,0), (0,0), (0,0)] # Holds the coordinates of the three points the triangle, needed to detect collision.

    # To know if the game should start and when it ends.
    game_start = False
    game_over = False
    score = 0

    # Audio and Music:
    begin_audio = None
    collision_audio = None
    gameover_audio = None
    restart_audio = None
    music_audio = None
    horizon_audio = None
    menu_music = None

    def __init__(self, **kwargs):
        super(HorizonGame, self).__init__(**kwargs)
        self.init_audio()
        self.draw_lines(self.vertical_lines, self.amount_vertical_lines)
        self.draw_lines(self.horizontal_lines, self.amount_horizontal_lines)
        self.draw_tiles()
        self.generate_tile_coordinates()
        self.draw_ship()
        self.horizon_audio.play()
        self.menu_music.play()
        self.menu_music.loop = True
        # To check if we are playing on desktop to use the keyboard, and not display the keyboard on the screen if it's being played on mobile.
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def is_desktop(self):
        """
        Checks if the app is running on desktop or mobile.
        """
        if platform in ('linux', 'win', 'macosx'):
            return True
        else:
            return False

    def on_size(self, *args):
        """
        When the window size changes this function automatically redraws the lines.
        """
        #print('x: ' + str(self.width))
        #print('y: ' + str(self.height))

        self.update_lines(self.vertical_lines)
        self.update_lines(self.horizontal_lines)

    def draw_lines(self, list_of_lines, amount_of_lines):
        """
        Creates the lines needed to draw the track and stores them in the given list of lines.
        """
        with self.canvas:
            Color(1,1,1,1)
            for i in range(0, amount_of_lines):
                list_of_lines.append(Line()) # Creates the needed amount of lines with empty points and store them on the list.

    def update_lines(self, list_of_lines):
        """
        Draw the lines in the horizontal and vertical axis.
        """
        # The minus and plus ot each variable called index is to go through all the items and not go out of index.
        start_index =-int(len(list_of_lines)/2) + 1
        end_index = start_index + len(list_of_lines) - 1

        offset = -int(len(list_of_lines)/2) + 0.5 # 0.5 so the middle of the screen is in the middle of the center track.
        xmin = self.get_x_index(start_index)
        xmax = self.get_x_index(end_index-1) # I've put a minus one here so the lines on the x don't go through the last vertical line, quite weird behavior.

        # To draw the vertical lines.
        if len(list_of_lines) == 10:
            for i in range(start_index,start_index+len(list_of_lines)):
                line_x = self.get_x_index(i)
                x1, y1 = self.transform(line_x, 0)
                x2, y2 = self.transform(line_x, self.height)

                list_of_lines[i].points = [x1, y1, x2, y2]
                offset += 1
        
        # To draw the horizontal lines.
        else:
            for i in range(start_index, self.amount_horizontal_lines):
                line_y = self.get_y_index(i)
                x1, y1 = self.transform(xmin, line_y)
                x2, y2 = self.transform(xmax, line_y)

                list_of_lines[i].points = [x1, y1, x2, y2]

    def get_x_index(self, index):
        """
        Returns the x coordinate of the tiles the player will move on.
        """
        center_x = self.perspective_point_x
        space = self.width * self.space_between_vertical_lines
        offset = index -0.5
        line_x = center_x + offset * space + self.current_offset_x
        return line_x

    def get_y_index(self, index):
        """
        Returns the y coordinate of the tiles the player will move on.
        """
        space_y = self.height * self.space_between_horizontal_lines
        line_y = index*space_y - self.current_offset_y
        return line_y

    def update(self, dt):
        """
        Updates the track constantly to not run out of track when the game starts.
        """
        time_factor = dt * 60
        self.update_lines(self.vertical_lines)
        self.update_lines(self.horizontal_lines)
        self.update_tiles()
        self.update_ship()

        if not self.game_over and self.game_start:
            current_speed_y = self.speed * self.height / 100 # So the speed is constant regardless of the screen height and width.
            current_speed_x = self.speed_x * self.width / 100
            
            self.current_offset_y += current_speed_y * time_factor
            self.current_offset_x += current_speed_x * time_factor

            # Makes an infinite loop of horizontal lines going towards the camera.

            space_y = self.height * self.space_between_horizontal_lines 

            while self.current_offset_y > space_y:
                self.current_offset_y -= space_y
                self.current_y_loop += 1
                self.score = self.current_y_loop * 100
                self.ids["score"].text = "Score: " + str(self.score)
                self.generate_tile_coordinates() # Needs to be called each time we update to keep the track going indefinetly.

        if not self.check_ship_collision() and not self.game_over:
            self.collision_audio.play()
            self.music_audio.stop()
            self.game_over = True
            self.ids["over_menu"].opacity = 0.8
            self.gameover_audio.play()

    def detect_collision(self, ti_x, ti_y):
        """
        Detects if the ship is still on the track or not, in case it isn't is displays a game over.
        """
        xmin, ymin = self.get_tile_coordinate(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinate(ti_x + 1, ti_y + 1)

        # TODO this clearly needs some work, at this point the WHOLE ship has to be offtracks to count as game over.

        for i in range(0, len(self.ship_coordinates)):
            px, py = self.ship_coordinates[i]

            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        
        return False

    def on_press_play(self):
        self.ids["menu_layout"].opacity = 0
        self.game_start = True
        self.begin_audio.play()
        self.music_audio.play()
        self.music_audio.loop = True
        self.menu_music.stop()
    
    def retry_game(self):
        """
        When in the game over screen the player presses the retry button.
        """
        self.ids["over_menu"].opacity = 0
        self.current_y_loop = 1
        self.current_offset_x = 0
        self.speed_x = 0
        self.current_offset_y = 0
        self.speed = 2
        self.tiles_coordinates = []
        self.generate_tile_coordinates() 
        self.score = 0
        self.ids["score"].text = ''
        self.game_over = False
        self.game_start = True
        self.restart_audio.play()
        self.music_audio.play()
        self.music_audio.loop = True
    
    def main_menu(self):
        """
        When the player clicks the main menu button on the game over screen.
        """
        self.score = 0
        self.ids["score"].text = ''
        self.ids["over_menu"].opacity = 0
        self.ids["menu_layout"].opacity = 0.8
        self.current_y_loop = 1
        self.current_offset_x = 0
        self.speed_x = 0
        self.current_offset_y = 0
        self.speed = 2
        self.tiles_coordinates = []
        self.generate_tile_coordinates()
        self.game_start = False
        self.game_over = False
        self.menu_music.play()
        self.menu_music.loop = True

class HorizonApp(App):
    pass

if __name__ == '__main__':
    HorizonApp().run()
