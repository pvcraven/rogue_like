"""
Sprites for a dungeon level
"""

import arcade

from constants import GRID_SIZE, SPRITE_SCALE
from dungeon_map import DungeonMap
from match_array import match_array
from sprites.entity import Entity

BRICK_WALL                     = arcade.LBWH(1*32, 1*32, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE    = arcade.LBWH(1*32, 5*32, 32, 32)
BRICK_WALL_WITH_LEFT_EDGE      = arcade.LBWH(0*32, 1*32, 32, 32)
BRICK_WALL_WITH_RIGHT_EDGE     = arcade.LBWH(2*32, 1*32, 32, 32)
BRICK_WALL_WITH_TOP_EDGE       = arcade.LBWH(1*32, 0*32, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE    = arcade.LBWH(1*32, 2*32, 32, 32)
BRICK_WALL_TOP_LEFT_CORNER     = arcade.LBWH(0*32, 0*32, 32, 32)
BRICK_WALL_TOP_RIGHT_CORNER    = arcade.LBWH(2*32, 0*32, 32, 32)
BRICK_WALL_BOTTOM_RIGHT_CORNER = arcade.LBWH(2*32, 2*32, 32, 32)
BRICK_WALL_BOTTOM_LEFT_CORNER  = arcade.LBWH(0*32, 2*32, 32, 32)
BRICK_WALL_TOP_NS_COLUMN          = arcade.LBWH(3*32, 0*32, 32, 32)
BRICK_WALL_MIDDLE_NS_COLUMN       = arcade.LBWH(3*32, 1*32, 32, 32)
BRICK_WALL_BOTTOM_NS_COLUMN       = arcade.LBWH(3*32, 2*32, 32, 32)
BRICK_WALL_LEFT_EW_COLUMN          = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_MIDDLE_EW_COLUMN       = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_RIGHT_EW_COLUMN       = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_TOP_BOTTOM_EDGE     = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_ONLY_LEFT           = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_ONLY_RIGHT          = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_CORNER_1            = arcade.LBWH(4*32, 0*32, 32, 32)
BRICK_WALL_CORNER_2            = arcade.LBWH(5*32, 0*32, 32, 32)
BRICK_WALL_CORNER_3            = arcade.LBWH(4*32, 1*32, 32, 32)
BRICK_WALL_CORNER_4            = arcade.LBWH(5*32, 1*32, 32, 32)
BRICK_WALL_CORNER_5            = arcade.LBWH(6*32, 0*32, 32, 32)
BRICK_WALL_SOLO                = arcade.LBWH(3*32, 3*32, 32, 32)
UNKNOWN                        = arcade.LBWH(7*32, 2*32, 32, 32)

class Level:
    def __init__(self):
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.background_list = arcade.SpriteList(use_spatial_hash=True)
        self.dungeon_map = DungeonMap()
        self.sprite_sheet_1 = arcade.SpriteSheet("sprites/walls.png")

    def load(self, filename):

        # Load the map
        self.dungeon_map.load(filename)

        for row in range(self.dungeon_map.map_height):
            for column in range(self.dungeon_map.map_width):
                x = column * GRID_SIZE
                y = (self.dungeon_map.map_height * GRID_SIZE) - (row * GRID_SIZE)

                tile = self.dungeon_map.tiles[row][column]

                # Get a nested list of the tile and its neighbors
                tiles = [
                    [
                        self.dungeon_map.tiles[row - 1][column - 1] if row > 0 and column > 0 else None,
                        self.dungeon_map.tiles[row - 1][column] if row > 0 else None,
                        self.dungeon_map.tiles[row - 1][column + 1] if row > 0 and column < self.dungeon_map.map_width - 1 else None
                    ],
                    [
                        self.dungeon_map.tiles[row][column - 1] if column > 0 else None,
                        tile,
                        self.dungeon_map.tiles[row][column + 1] if column < self.dungeon_map.map_width - 1 else None
                    ],
                    [
                        self.dungeon_map.tiles[row + 1][column - 1] if row < self.dungeon_map.map_height - 1 and column > 0 else None,
                        self.dungeon_map.tiles[row + 1][column] if row < self.dungeon_map.map_height - 1 else None,
                        self.dungeon_map.tiles[row + 1][column + 1] if row < self.dungeon_map.map_height - 1 and column < self.dungeon_map.map_width - 1 else None
                    ]
                ]

                def is_wall(tile):
                    return tile is not None and (tile.cell == 0 or tile.perimeter)

                # Create a 3x3 array of 1s and 0s based on if there is a tile
                tile_exists = [
                    [1 if is_wall(tiles[0][0]) else 0, 1 if is_wall(tiles[0][1]) else 0, 1 if is_wall(tiles[0][2]) else 0],
                    [1 if is_wall(tiles[1][0]) else 0, 1 if is_wall(tiles[1][1]) else 0, 1 if is_wall(tiles[1][2]) else 0],
                    [1 if is_wall(tiles[2][0]) else 0, 1 if is_wall(tiles[2][1]) else 0, 1 if is_wall(tiles[2][2]) else 0]
                ]

                if tile.cell == 0 or tile.perimeter:
                    # Create array of booleans to represent the current setup of the tile and its neighbors
                    result_string = match_array(tile_exists)
                    print(f"Row: {row}, Column: {column}, Setup: {tile_exists}, Result: {result_string}")
                    if result_string == "inside_wall":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL)
                    elif result_string == "top_edge":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_WITH_TOP_EDGE)
                    elif result_string == "bottom_edge":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_WITH_BOTTOM_EDGE)
                    elif result_string == "left_edge":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_WITH_LEFT_EDGE)
                    elif result_string == "right_edge":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_WITH_RIGHT_EDGE)
                    elif result_string == "top_left_corner":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_TOP_LEFT_CORNER)
                    elif result_string == "top_right_corner":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_TOP_RIGHT_CORNER)
                    elif result_string == "bottom_right_corner":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_BOTTOM_RIGHT_CORNER)
                    elif result_string == "bottom_left_corner":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_BOTTOM_LEFT_CORNER)
                    elif result_string == "top_ns_column":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_TOP_NS_COLUMN)
                    elif result_string == "middle_ns_column":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_MIDDLE_NS_COLUMN)
                    elif result_string == "bottom_ns_column":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_BOTTOM_NS_COLUMN)
                    elif result_string == "left_ew_column":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_LEFT_EW_COLUMN)
                    elif result_string == "middle_ew_column":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_MIDDLE_EW_COLUMN)
                    elif result_string == "right_ew_column":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_RIGHT_EW_COLUMN)
                    elif result_string == "corner_1":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_1)
                    elif result_string == "corner_2":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_2)
                    elif result_string == "solo":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_SOLO)
                    # elif result_string == "top_bottom_edge":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_TOP_BOTTOM_EDGE)
                    # elif result_string == "only_left":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_ONLY_LEFT)
                    # elif result_string == "only_right":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_ONLY_RIGHT)
                    # elif result_string == "corner_1":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_1)
                    # elif result_string == "corner_2":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_2)
                    # elif result_string == "corner_3":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_3)
                    # elif result_string == "corner_4":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_4)
                    # elif result_string == "solo":
                    #     texture = self.sprite_sheet_1.get_texture(BRICK_WALL_SOLO)
                    else:
                        texture = self.sprite_sheet_1.get_texture(UNKNOWN)

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
