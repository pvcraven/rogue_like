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
BRICK_WALL_TOP_NS_COLUMN       = arcade.LBWH(3*32, 0*32, 32, 32)
BRICK_WALL_MIDDLE_NS_COLUMN    = arcade.LBWH(3*32, 1*32, 32, 32)
BRICK_WALL_BOTTOM_NS_COLUMN    = arcade.LBWH(3*32, 2*32, 32, 32)
BRICK_WALL_LEFT_EW_COLUMN      = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_MIDDLE_EW_COLUMN    = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_RIGHT_EW_COLUMN     = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_TOP_BOTTOM_EDGE     = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_ONLY_LEFT           = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_ONLY_RIGHT          = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_CORNER_1            = arcade.LBWH(4*32, 0*32, 32, 32)
BRICK_WALL_CORNER_2            = arcade.LBWH(5*32, 0*32, 32, 32)
BRICK_WALL_CORNER_3            = arcade.LBWH(4*32, 1*32, 32, 32)
BRICK_WALL_CORNER_4            = arcade.LBWH(5*32, 1*32, 32, 32)
BRICK_WALL_CORNER_5            = arcade.LBWH(6*32, 0*32, 32, 32)
BRICK_WALL_SOLO                = arcade.LBWH(3*32, 3*32, 32, 32)
COLUMN_TURN_1                  = arcade.LBWH(4*32, 2*32, 32, 32)
COLUMN_TURN_2                  = arcade.LBWH(5*32, 2*32, 32, 32)
COLUMN_TURN_3                  = arcade.LBWH(6*32, 2*32, 32, 32)
COLUMN_TURN_4                  = arcade.LBWH(4*32, 3*32, 32, 32)
COLUMN_TURN_5                  = arcade.LBWH(5*32, 3*32, 32, 32)
COLUMN_TURN_6                  = arcade.LBWH(6*32, 3*32, 32, 32)
COLUMN_TURN_7                  = arcade.LBWH(4*32, 4*32, 32, 32)
COLUMN_TURN_8                  = arcade.LBWH(5*32, 4*32, 32, 32)
COLUMN_TURN_9                  = arcade.LBWH(6*32, 4*32, 32, 32)
EW_CORNER_1                    = arcade.LBWH(0*32, 4*32, 32, 32)
EW_CORNER_2                    = arcade.LBWH(1*32, 4*32, 32, 32)
EW_CORNER_3                    = arcade.LBWH(0*32, 5*32, 32, 32)
EW_CORNER_4                    = arcade.LBWH(1*32, 5*32, 32, 32)
NS_CORNER_1                    = arcade.LBWH(2*32, 4*32, 32, 32)
NS_CORNER_2                    = arcade.LBWH(3*32, 4*32, 32, 32)
NS_CORNER_3                    = arcade.LBWH(2*32, 5*32, 32, 32)
NS_CORNER_4                    = arcade.LBWH(3*32, 5*32, 32, 32)
CORNERS_NE_SE                  = arcade.LBWH(4*32, 5*32, 32, 32)
CORNERS_NW_SW                  = arcade.LBWH(5*32, 5*32, 32, 32)
CORNERS_NW_NE                  = arcade.LBWH(8*32, 2*32, 32, 32)
CORNERS_SW_SE                  = arcade.LBWH(8*32, 1*32, 32, 32)
CORNERS_NE_SE_SW               = arcade.LBWH(8*32, 4*32, 32, 32)
CORNERS_NW_SE                  = arcade.LBWH(7*32, 4*32, 32, 32)
UNKNOWN                        = arcade.LBWH(7*32, 2*32, 32, 32)
FLOOR_TILE_1                   = arcade.LBWH(8*32, 0*32, 32, 32)
FLOOR_TILE_2                   = arcade.LBWH(6*32, 4*32, 32, 32)

class Level:
    def __init__(self):
        self.dungeon_map = DungeonMap()

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.background_list = arcade.SpriteList(use_spatial_hash=True)
        self.door_list = arcade.SpriteList(use_spatial_hash=True)

        self.sprite_sheet_1 = arcade.SpriteSheet("sprites/walls.png")
        self.sprite_sheet_doors = arcade.SpriteSheet("sprites/doors.png")
        self.sprite_sheet_stairs = arcade.SpriteSheet("sprites/stairs.png")

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
                    # print(f"Row: {row}, Column: {column}, Setup: {tile_exists}, Result: {result_string}")
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
                    elif result_string == "corner_3":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_3)
                    elif result_string == "corner_4":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_CORNER_4)
                    elif result_string == "column_turn_1":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_1)
                    elif result_string == "column_turn_2":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_2)
                    elif result_string == "column_turn_3":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_3)
                    elif result_string == "column_turn_4":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_4)
                    elif result_string == "column_turn_5":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_5)
                    elif result_string == "column_turn_6":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_6)
                    elif result_string == "column_turn_7":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_7)
                    elif result_string == "column_turn_8":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_8)
                    elif result_string == "column_turn_9":
                        texture = self.sprite_sheet_1.get_texture(COLUMN_TURN_9)
                    elif result_string == "ew_corner_1":
                        texture = self.sprite_sheet_1.get_texture(EW_CORNER_1)
                    elif result_string == "ew_corner_2":
                        texture = self.sprite_sheet_1.get_texture(EW_CORNER_2)
                    elif result_string == "ew_corner_3":
                        texture = self.sprite_sheet_1.get_texture(EW_CORNER_3)
                    elif result_string == "ew_corner_4":
                        texture = self.sprite_sheet_1.get_texture(EW_CORNER_4)
                    elif result_string == "ns_corner_1":
                        texture = self.sprite_sheet_1.get_texture(NS_CORNER_1)
                    elif result_string == "ns_corner_2":
                        texture = self.sprite_sheet_1.get_texture(NS_CORNER_2)
                    elif result_string == "ns_corner_3":
                        texture = self.sprite_sheet_1.get_texture(NS_CORNER_3)
                    elif result_string == "ns_corner_4":
                        texture = self.sprite_sheet_1.get_texture(NS_CORNER_4)
                    elif result_string == "corners_ne_se":
                        texture = self.sprite_sheet_1.get_texture(CORNERS_NE_SE)
                    elif result_string == "corners_nw_sw":
                        texture = self.sprite_sheet_1.get_texture(CORNERS_NW_SW)
                    elif result_string == "corners_nw_ne":
                        texture = self.sprite_sheet_1.get_texture(CORNERS_NW_NE)
                    elif result_string == "corners_sw_se":
                        texture = self.sprite_sheet_1.get_texture(CORNERS_SW_SE)
                    elif result_string == "corners_ne_se_sw":
                        texture = self.sprite_sheet_1.get_texture(CORNERS_NE_SE_SW)
                    elif result_string == "corners_nw_se":
                        texture = self.sprite_sheet_1.get_texture(CORNERS_NW_SE)
                    elif result_string == "solo":
                        texture = self.sprite_sheet_1.get_texture(BRICK_WALL_SOLO)
                    else:
                        print("Unknown tile setup:", result_string)
                        for tile_row in tile_exists:
                            print(tile_row)
                        print()
                        texture = self.sprite_sheet_1.get_texture(UNKNOWN)

                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    self.wall_list.append(sprite)

                if tile.door or tile.locked or tile.trapped or tile.secret:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        texture = self.sprite_sheet_doors.get_texture(arcade.LBWH(0*32, 0*32, 32, 32))
                    else:
                        texture = self.sprite_sheet_doors.get_texture(arcade.LBWH(0*32, 0*32, 32, 32))
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y

                    self.door_list.append(sprite)

                if tile.stair_up:
                    texture = self.sprite_sheet_stairs.get_texture(arcade.LBWH(0*32, 0*32, 32, 32))
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    sprite.block_sight = False
                    self.door_list.append(sprite)

                if tile.stair_down:
                    texture = self.sprite_sheet_stairs.get_texture(arcade.LBWH(1*32, 0*32, 32, 32))
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    sprite.block_sight = False
                    self.door_list.append(sprite)

                if sprite:
                    sprite.color = sprite.not_visible_color
                    sprite.tile = tile

                if tile.corridor:
                    texture = self.sprite_sheet_1.get_texture(FLOOR_TILE_1)
                    sprite = Entity(texture, scale=SPRITE_SCALE)
                    sprite.color = sprite.not_visible_color
                    sprite.block_sight = False
                    sprite.tile = tile
                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if not tile.corridor and not is_wall(tile):
                    texture = self.sprite_sheet_1.get_texture(FLOOR_TILE_1)
                    sprite = Entity(texture, scale=SPRITE_SCALE)
                    sprite.color = sprite.not_visible_color
                    sprite.block_sight = False
                    sprite.tile = tile
                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)


    def get_stairs_up(self):
        """
        Get a list of stair up sprites
        """
        return [sprite for sprite in self.background_list if sprite.tile.stair_up]

    def get_stairs_down(self):
        """
        Get a list of stair down sprites
        """
        return [sprite for sprite in self.background_list if sprite.tile.stair_down]