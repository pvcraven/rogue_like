"""
Sprites for a dungeon level.
"""

import arcade

from constants import GRID_SIZE, SPRITE_SCALE
from dungeon_map import DungeonMap
from match_array import match_array
from sprites.entity import Entity
from sprites.monsters.slime import Slime
from wall_texture_map import FLOOR_TILE_1, UNKNOWN, WALL_TEXTURE_MAP
import random
from util import grid_to_pixel

def _is_wall(tile):
    return tile is not None and (tile.cell == 0 or tile.perimeter)


class Level:
    def __init__(self):

        # Create the dungeon map
        self.dungeon_map: DungeonMap = DungeonMap()

        # Sprite lists for different types of sprites
        self.wall_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.background_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.door_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.monster_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=False)

        # Load sprite sheets
        self.sprite_sheet_1 = arcade.SpriteSheet("sprites/walls.png")
        self.sprite_sheet_doors = arcade.SpriteSheet("sprites/doors.png")
        self.sprite_sheet_stairs = arcade.SpriteSheet("sprites/stairs.png")

        self.physics_engine: arcade.PhysicsEngineSimple = arcade.PhysicsEngineSimple(None, self.wall_list)

    def _get_surrounding_tiles(self, row, column):
        """
        Get a 3x3 array of tiles surrounding the tile at (row, column).
        """
        tiles = [
            [
                self.dungeon_map.tiles[row - 1][column - 1] if row > 0 and column > 0 else None,
                self.dungeon_map.tiles[row - 1][column] if row > 0 else None,
                self.dungeon_map.tiles[row - 1][column + 1] if row > 0 and column < self.dungeon_map.map_width - 1 else None
            ],
            [
                self.dungeon_map.tiles[row][column - 1] if column > 0 else None,
                self.dungeon_map.tiles[row][column],
                self.dungeon_map.tiles[row][column + 1] if column < self.dungeon_map.map_width - 1 else None
            ],
            [
                self.dungeon_map.tiles[row + 1][column - 1] if row < self.dungeon_map.map_height - 1 and column > 0 else None,
                self.dungeon_map.tiles[row + 1][column] if row < self.dungeon_map.map_height - 1 else None,
                self.dungeon_map.tiles[row + 1][column + 1] if row < self.dungeon_map.map_height - 1 and column < self.dungeon_map.map_width - 1 else None
            ]
        ]
        return tiles

    def _get_wall_array(self, tiles):
        """
        Get a 3x3 array of 1s and 0s representing walls around the tile at (row, column).
        """
        return [
            [1 if _is_wall(tiles[0][0]) else 0, 1 if _is_wall(tiles[0][1]) else 0, 1 if _is_wall(tiles[0][2]) else 0],
            [1 if _is_wall(tiles[1][0]) else 0, 1 if _is_wall(tiles[1][1]) else 0, 1 if _is_wall(tiles[1][2]) else 0],
            [1 if _is_wall(tiles[2][0]) else 0, 1 if _is_wall(tiles[2][1]) else 0, 1 if _is_wall(tiles[2][2]) else 0]
        ]

    def load(self, filename):

        # Load the map
        self.dungeon_map.load(filename)

        # Loop through each tile in the dungeon map
        # and create sprites
        for row in range(self.dungeon_map.map_height):
            for column in range(self.dungeon_map.map_width):

                # Get the tile at the current row and column
                tile = self.dungeon_map.tiles[row][column]

                # Grab the x and y scren coordinates for the tile
                x = column * GRID_SIZE
                y = (self.dungeon_map.map_height * GRID_SIZE) - (row * GRID_SIZE)

                # Get a 2D array of the tile and its neighbors
                tiles = self._get_surrounding_tiles(row, column)

                # Create a 3x3 array of 1s and 0s based on if there is a wall or map edge
                tile_exists = self._get_wall_array(tiles)

                if tile.cell == 0 or tile.perimeter:
                    # Create array of booleans to represent the current setup of the tile and its neighbors
                    result_string = match_array(tile_exists)

                    # Look up texture from the mapping dictionary
                    texture_region = WALL_TEXTURE_MAP.get(result_string)
                    if texture_region:
                        texture = self.sprite_sheet_1.get_texture(texture_region)
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
                        texture = self.sprite_sheet_doors.get_texture(arcade.LBWH(4*32, 0*32, 32, 32))
                    else:
                        texture = self.sprite_sheet_doors.get_texture(arcade.LBWH(3*32, 0*32, 32, 32))
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.center_x = x + GRID_SIZE / 2
                    sprite.center_y = y + GRID_SIZE / 2

                    self.door_list.append(sprite)

                if tile.stair_up:
                    texture = self.sprite_sheet_stairs.get_texture(arcade.LBWH(0*32, 0*32, 32, 32))
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    sprite.block_sight = False
                    sprite.tile = tile
                    self.door_list.append(sprite)

                if tile.stair_down:
                    texture = self.sprite_sheet_stairs.get_texture(arcade.LBWH(1*32, 0*32, 32, 32))
                    sprite = Entity(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    sprite.block_sight = False
                    sprite.tile = tile
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

                if not tile.corridor and not _is_wall(tile):
                    texture = self.sprite_sheet_1.get_texture(FLOOR_TILE_1)
                    sprite = Entity(texture, scale=SPRITE_SCALE)
                    sprite.color = sprite.not_visible_color
                    sprite.block_sight = False
                    sprite.tile = tile
                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

        for room in self.dungeon_map.json['rooms']:
            if room:
                north = room['north']
                south = room['south']
                east = room['east']
                west = room['west']
                id = room['id']
                # print(f"Room {id}: North {north}, South {south}, East {east}, West {west}")
                if int(id) == 6:
                    rand_row = random.randint(north, south)
                    rand_col = random.randint(west, east)
                    x, y = grid_to_pixel(rand_col, rand_row, self.dungeon_map.map_height)
                    print(f"Random tile in room {id}: row={rand_row}, col={rand_col}")
                    monster = Slime()
                    monster.position = (x, y)
                    self.monster_list.append(monster)



    def get_stairs_up(self):
        """
        Get a list of stair up sprites
        """
        return [sprite for sprite in self.door_list if sprite.tile.stair_up]

    def get_stairs_down(self):
        """
        Get a list of stair down sprites
        """
        return [sprite for sprite in self.door_list if sprite.tile.stair_down]
