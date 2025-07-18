import arcade

SPRITE_SCALE = 2
GRID_SIZE = 32 * SPRITE_SCALE

DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 400

HORIZONTAL_BOUNDARY = DEFAULT_WINDOW_WIDTH / 2.0 - VIEWPORT_MARGIN
VERTICAL_BOUNDARY = DEFAULT_WINDOW_HEIGHT / 2.0 - VIEWPORT_MARGIN

# If the player moves further than this boundary away from the camera we use a
# constraint to move the camera
CAMERA_BOUNDARY = arcade.LRBT(
    -HORIZONTAL_BOUNDARY,
    HORIZONTAL_BOUNDARY,
    -VERTICAL_BOUNDARY,
    VERTICAL_BOUNDARY,
)

FOV_RADIUS = 8

# Files holding each level's map data
LEVEL_FILE_NAMES = [
    "maps/level_01.json",
    "maps/level_02.json",
    "maps/level_03.json"
]

