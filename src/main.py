import arcade

from constants import (
    CAMERA_SPEED,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    FOV_RADIUS,
    GRID_SIZE,
    SPRITE_SCALE,
)
from level import Level
from recalculate_fov import recalculate_fov
from sprites.player import PlayerSprite
from util import pixel_to_grid

SCREEN_TITLE = "Rogue-Like Example"

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 4


class MyGame(arcade.Window):
    """Main application class."""

    def get_clipboard_text(self):
        """Return the current clipboard text."""
        # You can use arcade's default clipboard or return an empty string
        return ""

    def set_clipboard_text(self, text: str):
        """Set the clipboard text."""
        # You can implement clipboard functionality or just pass for now
        # pass

    def __init__(self, width, height, title):
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
            multiline=True,
        )
        self.last_player_position = (0, 0)

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Load the dungeon map
        self.level.load("levels/level_02.json")
        stairs_up = self.level.get_stairs_up()

        # Set up the player
        self.player_sprite = PlayerSprite()
        self.player_sprite.position = stairs_up[0].position

        self.player_list.append(self.player_sprite)

        # Set the background color
        arcade.set_background_color(arcade.color.GRAY)

        walls = self.level.wall_list
        # walls = []
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls)

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.camera_sprites.use()

        # Draw all the sprites.
        self.level.wall_list.draw(pixelated=True)
        self.level.background_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Player position in grid coordinates
        grid_column = int(self.player_sprite.center_x // (GRID_SIZE * SPRITE_SCALE))
        grid_row = int(
            self.level.dungeon_map.map_height
            - (self.player_sprite.center_y // (GRID_SIZE * SPRITE_SCALE))
        )
        try:
            # Get the tile at the player's position
            cur_tile = self.level.dungeon_map.tiles[grid_row][grid_column]
        except IndexError:
            cur_tile = None

        # Draw the GUI
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.width // 2, 40, self.width, 80), arcade.color.ALMOND
        )
        info = f"Player Position: {grid_column}, {grid_row}. "
        if cur_tile and cur_tile.room_id:
            info = f"Room {cur_tile.room_id}. "
            room = self.level.dungeon_map.get_room(cur_tile.room_id)
            if room and room.room_features:
                info += room.room_features

        if cur_tile and cur_tile.corridor:
            info += "You are in a corridor."

        arcade.draw_text(
            info, 10, 45, arcade.color.BLACK_BEAN, 20, multiline=True, width=self.width
        )

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""

        if symbol == arcade.key.UP:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, symbol, modifiers):
        """Called when the user releases a key."""

        if symbol == arcade.key.UP:
            self.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """Movement and game logic"""

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

        self.player_sprite.update(delta_time)

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Figure out our field-of-view
        pos_grid = pixel_to_grid(
            self.player_sprite.center_x,
            self.player_sprite.center_y,
            map_height=self.level.dungeon_map.map_height,
        )
        if pos_grid != self.last_player_position:
            self.last_player_position = pos_grid
            sprite_lists = [
                self.level.wall_list,
                self.level.background_list,
            ]
            recalculate_fov(
                char_x=pos_grid[0],
                char_y=pos_grid[1],
                radius=FOV_RADIUS,
                map_height=self.level.dungeon_map.map_height,
                sprite_lists=sprite_lists,
            )

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
            self.camera_sprites.position,
            position,
            CAMERA_SPEED,
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
    """Main function"""
    window = MyGame(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
