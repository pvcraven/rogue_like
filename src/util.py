from constants import GRID_SIZE, SPRITE_SCALE


def grid_to_pixel(grid_x, grid_y, map_height):
    """Convert grid coordinates to pixel coordinates."""
    pixel_x = grid_x * GRID_SIZE * SPRITE_SCALE + (GRID_SIZE * SPRITE_SCALE) // 2
    pixel_y = (map_height - grid_y) * GRID_SIZE * SPRITE_SCALE + (
        GRID_SIZE * SPRITE_SCALE
    ) // 2
    return pixel_x, pixel_y


def pixel_to_grid(pixel_x, pixel_y, map_height):
    """Convert pixel coordinates to grid coordinates."""
    column = int(pixel_x // GRID_SIZE)
    row = int(map_height - (pixel_y // GRID_SIZE))
    return column, row
