import arcade

from constants import (
    CAMERA_SPEED,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    FOV_RADIUS,
    GRID_SIZE,
    LEVEL_FILE_NAMES,
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

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.last_player_position = (-10, -10)

        # Set up the physics engine
        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Cameras
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        # Level info
        self.level: Level = Level(player_list=self.player_list)
        self.cur_level = 0
        self.levels: list[Level] = []

        self.room_details = arcade.Text(
            "Fonts:",
            10,
            50,
            arcade.color.BLACK_BEAN,
            24,
            width=self.width,
            multiline=True,
        )

    def set_player_position_to_stairs(self, stairs_up: bool) -> None:
        """Set the player position to the first set of stairs up."""
        if stairs_up:
            stairs = self.level.get_stairs_up()
        else:
            stairs = self.level.get_stairs_down()
        if len(stairs) == 0:
            raise ValueError(
                "No stairs up found in the level. Please check the map data."
            )

        self.player_sprite.position = stairs[0].position
        self.scroll_to_player(camera_speed=1.0)

    def setup(self):
        """Set up the game and initialize the variables."""

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = PlayerSprite()
        self.player_sprite.color = self.player_sprite.visible_color
        self.player_list.append(self.player_sprite)

        # Load the dungeon map
        for level_file_name in LEVEL_FILE_NAMES:
            level = Level(player_list=self.player_list)
            level.load(level_file_name)
            level.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, [level.wall_list, level.monster_list]
            )
            self.levels.append(level)

        self.level = self.levels[self.cur_level]

        # Set the player's level reference
        self.player_sprite.level = self.level

        # Set player position to the first set of stairs
        self.set_player_position_to_stairs(stairs_up=True)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def get_grid_position(self, x: float, y: float) -> tuple[int, int]:
        """Convert pixel coordinates to grid coordinates."""
        grid_column = int(x // GRID_SIZE)
        grid_row = int(self.level.dungeon_map.map_height - y // GRID_SIZE)
        return grid_column, grid_row

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.camera_sprites.use()

        # Draw all the sprites.
        self.level.background_list.draw(pixelated=True)
        self.level.wall_list.draw(pixelated=True)
        self.level.door_list.draw(pixelated=True)
        self.level.monster_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.player_list.draw_hit_boxes()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Player position in grid coordinates
        grid_column, grid_row = self.get_grid_position(
            self.player_sprite.center_x, self.player_sprite.center_y
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
        info = (
            f"Level {self.cur_level + 1}, Player Position: {grid_column}, {grid_row}. "
        )
        if cur_tile and cur_tile.room_id:
            info += f"Room {cur_tile.room_id}. "
            room = self.level.dungeon_map.get_room(str(cur_tile.room_id))
            if room and room.room_features:
                info += room.room_features

        if cur_tile and cur_tile.corridor:
            info += "You are in a corridor."

        self.room_details.text = info
        self.room_details.draw()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""

        if symbol == arcade.key.W:
            self.up_pressed = True
        elif symbol == arcade.key.S:
            self.down_pressed = True
        elif symbol == arcade.key.A:
            self.left_pressed = True
        elif symbol == arcade.key.D:
            self.right_pressed = True
        elif symbol == arcade.key.E:
            grid_column, grid_row = self.get_grid_position(
                self.player_sprite.center_x, self.player_sprite.center_y
            )
            cur_tile = self.level.dungeon_map.tiles[grid_row][grid_column]
            if cur_tile.stair_down:
                print("DOWN STAIRS")
                if self.cur_level < len(self.levels):
                    self.cur_level += 1
                    self.level = self.levels[self.cur_level]
                    self.player_sprite.level = self.level
                    self.set_player_position_to_stairs(stairs_up=True)
            elif cur_tile.stair_up:
                print("UP STAIRS")
                if self.cur_level > 0:
                    self.cur_level -= 1
                    self.level = self.levels[self.cur_level]
                    self.player_sprite.level = self.level
                    self.set_player_position_to_stairs(stairs_up=False)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """Handle mouse wheel scroll events."""
        # Zoom the camera in/out with the mouse wheel
        zoom_factor = 1.1
        if scroll_y > 0:
            self.camera_sprites.zoom *= zoom_factor
        elif scroll_y < 0:
            self.camera_sprites.zoom /= zoom_factor

    def on_key_release(self, symbol, modifiers):
        """Called when the user releases a key."""

        if symbol == arcade.key.W:
            self.up_pressed = False
        elif symbol == arcade.key.S:
            self.down_pressed = False
        elif symbol == arcade.key.A:
            self.left_pressed = False
        elif symbol == arcade.key.D:
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
        self.level.monster_list.update(delta_time)

        self.level.physics_engine.update()

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
                self.level.door_list,
                self.level.background_list,
                self.level.monster_list,
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

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle mouse press events to trigger player attacks.

        Args:
            x (float): X-coordinate of the mouse click.
            y (float): Y-coordinate of the mouse click.
            button (int): Mouse button pressed.
            modifiers (int): Modifier keys pressed (e.g., Shift, Ctrl).
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.attack_1()
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.attack_2()
        elif button == arcade.MOUSE_BUTTON_MIDDLE:
            self.player_sprite.attack_3()

    def scroll_to_player(self, camera_speed: float = CAMERA_SPEED):
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
            camera_speed,
        )

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window()

    def get_clipboard_text(self):
        """Return the current clipboard text."""
        # You can use arcade's default clipboard or return an empty string
        return ""

    def set_clipboard_text(self, text: str):
        """Set the clipboard text."""
        # You can implement clipboard functionality or just pass for now
        # pass


def main():
    """Main function"""
    window = MyGame(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
