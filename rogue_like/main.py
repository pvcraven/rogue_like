"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling
"""

import arcade
from pyglet.math import Vec2
from level import Level

SPRITE_SCALING = 0.125

DEFAULT_SCREEN_WIDTH = 1550
DEFAULT_SCREEN_HEIGHT = 865
SCREEN_TITLE = "Sprite Move with Scrolling Screen Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 4

GRID_SIZE = 32


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.player_list = None

        # Set up the player
        self.player_sprite = None

        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        self.level = Level()
        self.room_details = arcade.Text(
            "Fonts:",
            0,
            0,
            arcade.color.WHITE,
            24,
            bold=True,
            width=self.width,
            multiline=True
        )

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.SpriteSolidColor(width=GRID_SIZE // 2, height=GRID_SIZE // 2, color=arcade.color.GREEN)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        self.level.load("levels/level_01.json")

        # Set the background color
        arcade.set_background_color(arcade.color.GRAY)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.level.wall_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.level.wall_list.draw()
        self.level.background_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        grid_column = int(self.player_sprite.center_x // GRID_SIZE)
        grid_row = int(self.level.dungeon_map.map_height - (self.player_sprite.center_y // GRID_SIZE))
        cur_tile = self.level.dungeon_map.tiles[grid_row][grid_column]
        # print(cur_tile)

        # Draw the GUI
        arcade.draw_rect_filled(arcade.rect.XYWH(self.width // 2, 40, self.width, 80), arcade.color.ALMOND)
        info = ""
        if cur_tile.room_id:
            info = f"Room {cur_tile.room_id}. "
            room = self.level.dungeon_map.get_room(cur_tile.room_id)
            if room and room.room_features:
                info += room.room_features

        if cur_tile.corridor:
            info += "You are in a corridor."

        arcade.draw_text(info, 10, 45, arcade.color.BLACK_BEAN, 20, multiline=True, width=self.width)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        l = self.camera_sprites.position[0]
        b = self.camera_sprites.position[1]
        adjusted_x = l + x
        adjusted_y = b + y
        column = int(adjusted_x // GRID_SIZE)
        row = int(self.level.dungeon_map.map_height - (adjusted_y // GRID_SIZE))
        tile = self.level.dungeon_map.tiles[row][column]
        print()
        print(f"{row=} {column=}")
        self.level.dungeon_map.print_cell(tile.cell)


    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired
        position. Anything between 0 and 1 will have the camera move to the
        location with a smoother pan.
        """

        position = (self.player_sprite.center_x, self.player_sprite.center_y)
        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position, position, CAMERA_SPEED,
        )

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window()


def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
