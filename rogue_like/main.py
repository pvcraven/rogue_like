"""
Scroll around a large screen.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_scrolling
"""

import arcade
from pyglet.math import Vec2
from dungeon_map import DungeonMap

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
        self.wall_list = None
        self.background_list = None

        # Set up the player
        self.player_sprite = None

        self.physics_engine = None

        # Used in scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

        self.dungeon_map = None

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
        self.wall_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.SpriteSolidColor(GRID_SIZE // 2, GRID_SIZE // 2, arcade.color.GREEN)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        self.dungeon_map = DungeonMap("../levels/level_01.json")

        # Opening JSON file

        for row in range(self.dungeon_map.map_height):
            for column in range(self.dungeon_map.map_width):
                x = column * GRID_SIZE
                y = (self.dungeon_map.map_height * GRID_SIZE) - (row * GRID_SIZE)

                tile = self.dungeon_map.tiles[row][column]
                if tile.cell == 0 or tile.perimeter:
                    sprite = arcade.SpriteSolidColor(GRID_SIZE, GRID_SIZE, arcade.color.BLACK)
                    sprite.left = x
                    sprite.bottom = y
                    self.wall_list.append(sprite)

                if tile.door:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.locked:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-locked-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-locked-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.trapped:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-trapped-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-trapped-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.secret:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-secret-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-secret-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.label:
                    sprite = arcade.SpriteSolidColor(GRID_SIZE, GRID_SIZE, arcade.color.LIGHT_GRAY)
                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.background_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        grid_column = int(self.player_sprite.center_x // GRID_SIZE)
        grid_row = int(self.dungeon_map.map_height - (self.player_sprite.center_y // GRID_SIZE))
        cur_tile = self.dungeon_map.tiles[grid_row][grid_column]
        # print(cur_tile)

        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2, 40, self.width, 80, arcade.color.ALMOND)
        info = ""
        if cur_tile.room_id:
            info = f"Room {cur_tile.room_id}. "
            room = self.dungeon_map.get_room(cur_tile.room_id)
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
        x += self.view_left
        y += self.view_bottom
        column = int(x // GRID_SIZE)
        row = int(self.dungeon_map.map_height - (y // GRID_SIZE))
        tile = self.dungeon_map.tiles[row][column]
        print()
        print(column, row)
        self.dungeon_map.print_cell(tile.cell)

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)



def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()