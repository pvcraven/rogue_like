"""
Calculate Field Of Vision (FOV)
"""

import math
from typing import List

import arcade

from util import grid_to_pixel


def reset_fov(sprite_lists: List[arcade.SpriteList]):
    """
    Reset the visibility of all sprites in the provided sprite lists.
    This sets all sprites to not visible and applies their not_visible_color.
    """
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.is_visible = False
                sprite.color = sprite.seen_color
                if len(sprite.color) == 4:
                    sprite.alpha = sprite.seen_color[3]


def recalculate_fov(
    char_x: int,
    char_y: int,
    radius: int,
    map_height,
    sprite_lists: List[arcade.SpriteList],
):
    """ Calculate the field of vision for a character at (char_x, char_y) with a given radius. """
    reset_fov(sprite_lists)

    resolution = 8
    circumference = 2 * math.pi * radius

    radians_per_point = 2 * math.pi / (circumference * resolution)
    point_count = int(round(circumference)) * resolution

    loop_1_count = 0
    loop_2_count = 0
    loop_3_count = 0
    for i in range(point_count):
        loop_1_count += 1
        radians = i * radians_per_point

        x = math.sin(radians) * radius + char_x
        y = math.cos(radians) * radius + char_y

        raychecks = radius
        checked_points = []
        for j in range(raychecks):
            loop_2_count += 1
            # Calculate the grid coordinates
            v1 = char_x, char_y
            v2 = x, y
            x2, y2 = arcade.math.lerp_2d(v1, v2, j / raychecks)
            x2 = round(x2)
            y2 = round(y2)

            grid_point = (x2, y2)

            # Skip if the point has already been checked
            if grid_point in checked_points:
                continue
            checked_points.append(grid_point)

            # Convert grid coordinates to pixel coordinates
            pixel_point = grid_to_pixel(x2, y2, map_height=map_height)

            blocks = False
            for sprite_list in sprite_lists:

                sprites_at_point = arcade.get_sprites_at_exact_point(
                    pixel_point, sprite_list
                )
                for sprite in sprites_at_point:
                    loop_3_count += 1
                    if not sprite.is_visible:
                        sprite.is_visible = True
                        sprite.color = sprite.visible_color
                        if len(sprite.color) == 4:
                            sprite.alpha = sprite.visible_color[3]
                    if sprite.block_sight:
                        blocks = True
                        break  # Early exit on block
                if blocks:
                    break  # Early exit on block
            if blocks:
                break

    # print(
    #     f"Loop 1 count: {loop_1_count}, Loop 2 count: {loop_2_count}, Loop 3 count: {loop_3_count}"
    # )
