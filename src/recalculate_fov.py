"""
Calculate Field Of Vision (FOV)
"""

import math
from typing import List

import arcade

from constants import *
from sprites.entity import Entity
from util import grid_to_pixel


def recalculate_fov(
    char_x: int,
    char_y: int,
    radius: int,
    map_height,
    sprite_lists: List[arcade.SpriteList],
):
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.is_visible = False
                sprite.color = sprite.not_visible_color
                if len(sprite.color) == 4:
                    sprite.alpha = sprite.not_visible_color[3]

    resolution = 8  # Lowered from 25 for fewer rays
    circumference = 2 * math.pi * radius

    radians_per_point = 2 * math.pi / (circumference * resolution)
    point_count = int(round(circumference)) * resolution
    for i in range(point_count):
        radians = i * radians_per_point

        x = math.sin(radians) * radius + char_x
        y = math.cos(radians) * radius + char_y

        raychecks = radius
        for j in range(raychecks):
            v1 = char_x, char_y
            v2 = x, y
            x2, y2 = arcade.math.lerp_2d(v1, v2, j / raychecks)
            x2 = round(x2)
            y2 = round(y2)

            pixel_point = grid_to_pixel(x2, y2, map_height=map_height)

            blocks = False
            for sprite_list in sprite_lists:
                sprites_at_point = arcade.get_sprites_at_exact_point(
                    pixel_point, sprite_list
                )
                for sprite in sprites_at_point:
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

    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.color = sprite.visible_color
                if len(sprite.color) == 4:
                    sprite.alpha = sprite.visible_color[3]
