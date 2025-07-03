"""
Sprites for a dungeon level
"""

import arcade

from constants import GRID_SIZE, SPRITE_SCALE
from dungeon_map import DungeonMap
from sprites.entity import Entity

BRICK_WALL = arcade.LBWH(1 * 32, 4 * 32 + 16, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE = arcade.LBWH(1 * 32, 5 * 32, 32, 32)
BRICK_WALL_WITH_LEFT_EDGE = arcade.LBWH(3 * 32 + 16, 2 * 32 + 16, 32, 32)
BRICK_WALL_WITH_RIGHT_EDGE = arcade.LBWH(4 * 32 + 16, 2 * 32 + 16, 32, 32)
BRICK_WALL_WITH_TOP_EDGE = arcade.LBWH(8 * 32, 2 * 32, 32, 32)


class Level:
    def __init__(self):
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.background_list = arcade.SpriteList(use_spatial_hash=True)
        self.dungeon_map = DungeonMap()
        self.sprite_sheet_1 = arcade.SpriteSheet("sprites/FDR_Dungeon.png")

    def load(self, filename):

        # Load the map
        self.dungeon_map.load(filename)

        for row in range(self.dungeon_map.map_height):
            for column in range(self.dungeon_map.map_width):
                x = column * GRID_SIZE
                y = (self.dungeon_map.map_height * GRID_SIZE) - (row * GRID_SIZE)

                tile = self.dungeon_map.tiles[row][column]
                tile_up = self.dungeon_map.tiles[row - 1][column] if row > 0 else None
                tile_left = (
                    self.dungeon_map.tiles[row][column - 1] if column > 0 else None
                )
                tile_down = (
                    self.dungeon_map.tiles[row + 1][column]
                    if row < self.dungeon_map.map_height - 1
                    else None
                )
                tile_right = (
                    self.dungeon_map.tiles[row][column + 1]
                    if column < self.dungeon_map.map_width - 1
                    else None
                )
                sprite = None

                if tile.cell == 0 or tile.perimeter:
                    if tile_up and not (tile_up.cell == 0 or tile_up.perimeter):
                        texture = self.sprite_sheet_1.get_texture(
                            rect=BRICK_WALL_WITH_TOP_EDGE
                        )
                    elif tile_left and not (tile_left.cell == 0 or tile_left.perimeter):
                        texture = self.sprite_sheet_1.get_texture(
                            rect=BRICK_WALL_WITH_LEFT_EDGE
                        )
                    elif tile_right and not (
                        tile_right.cell == 0 or tile_right.perimeter
                    ):
                        texture = self.sprite_sheet_1.get_texture(
                            rect=BRICK_WALL_WITH_RIGHT_EDGE
                        )
                    else:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL)
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    self.wall_list.append(sprite)

                if tile.door:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = Entity("sprites/door-ns.png")
                    else:
                        sprite = Entity("sprites/door-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.locked:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = Entity("sprites/door-locked-ns.png")
                    else:
                        sprite = Entity("sprites/door-locked-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.trapped:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = Entity("sprites/door-trapped-ns.png")
                    else:
                        sprite = Entity("sprites/door-trapped-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.secret:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = Entity("sprites/door-secret-ns.png")
                    else:
                        sprite = Entity("sprites/door-secret-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.stair_up:
                    sprite = Entity("sprites/stair-up.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.stair_down:
                    sprite = Entity("sprites/stair-down.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if sprite:
                    sprite.color = sprite.not_visible_color

                # if tile.label:
                #     sprite = arcade.SpriteSolidColor(
                #         width=GRID_SIZE, height=GRID_SIZE, color=arcade.color.LIGHT_GRAY
                #     )
                #     sprite.left = x
                #     sprite.bottom = y
                #     self.background_list.append(sprite)
