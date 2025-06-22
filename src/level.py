"""
Sprites for a dungeon level
"""

import arcade
from constants import GRID_SIZE, SPRITE_SCALE
from dungeon_map import DungeonMap

BRICK_WALL                     = arcade.LBWH(1*32, 1*32, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE    = arcade.LBWH(1*32, 5*32, 32, 32)
BRICK_WALL_WITH_LEFT_EDGE      = arcade.LBWH(0*32, 1*32, 32, 32)
BRICK_WALL_WITH_RIGHT_EDGE     = arcade.LBWH(2*32, 1*32, 32, 32)
BRICK_WALL_WITH_TOP_EDGE       = arcade.LBWH(1*32, 0*32, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE    = arcade.LBWH(1*32, 2*32, 32, 32)
BRICK_WALL_TOP_LEFT_CORNER     = arcade.LBWH(0*32, 0*32, 32, 32)
BRICK_WALL_TOP_RIGHT_CORNER    = arcade.LBWH(2*32, 0*32, 32, 32)
BRICK_WALL_BOTTOM_RIGHT_CORNER = arcade.LBWH(2*32, 2*32, 32, 32)
BRICK_WALL_TOP_COLUMN          = arcade.LBWH(3*32, 0*32, 32, 32)
BRICK_WALL_MIDDLE_COLUMN       = arcade.LBWH(3*32, 1*32, 32, 32)
BRICK_WALL_BOTTOM_COLUMN       = arcade.LBWH(3*32, 2*32, 32, 32)
BRICK_WALL_TOP_BOTTOM_EDGE     = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_ONLY_LEFT           = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_ONLY_RIGHT          = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_CORNER_1            = arcade.LBWH(4*32, 0*32, 32, 32)
BRICK_WALL_CORNER_2            = arcade.LBWH(5*32, 0*32, 32, 32)
BRICK_WALL_CORNER_3            = arcade.LBWH(4*32, 1*32, 32, 32)
BRICK_WALL_CORNER_4            = arcade.LBWH(5*32, 1*32, 32, 32)

class Level:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
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
                tile_up = self.dungeon_map.tiles[row - 1][column] if row > 0 else None
                tile_left = self.dungeon_map.tiles[row][column - 1] if column > 0 else None
                tile_down = self.dungeon_map.tiles[row + 1][column] if row < self.dungeon_map.map_height - 1 else None
                tile_right = self.dungeon_map.tiles[row][column + 1] if column < self.dungeon_map.map_width - 1 else None
                # Diagonal neighbors
                tile_up_left = (
                    self.dungeon_map.tiles[row - 1][column - 1]
                    if row > 0 and column > 0 else None
                )
                tile_up_right = (
                    self.dungeon_map.tiles[row - 1][column + 1]
                    if row > 0 and column < self.dungeon_map.map_width - 1 else None
                )
                tile_down_left = (
                    self.dungeon_map.tiles[row + 1][column - 1]
                    if row < self.dungeon_map.map_height - 1 and column > 0 else None
                )
                tile_down_right = (
                    self.dungeon_map.tiles[row + 1][column + 1]
                    if row < self.dungeon_map.map_height - 1 and column < self.dungeon_map.map_width - 1 else None
                )

                is_empty_up = tile_up and not (tile_up.cell == 0 or tile_up.perimeter)
                is_empty_left = tile_left and not (tile_left.cell == 0 or tile_left.perimeter)
                is_empty_down = tile_down and not (tile_down.cell == 0 or tile_down.perimeter)
                is_empty_right = tile_right and not (tile_right.cell == 0 or tile_right.perimeter)

                is_empty_up_left = tile_up_left and not (tile_up_left.cell == 0 or tile_up_left.perimeter)
                is_empty_up_right = tile_up_right and not (tile_up_right.cell == 0 or tile_up_right.perimeter)
                is_empty_down_left = tile_down_left and not (tile_down_left.cell == 0 or tile_down_left.perimeter)
                is_empty_down_right = tile_down_right and not (tile_down_right.cell == 0 or tile_down_right.perimeter)

                if tile.cell == 0 or tile.perimeter:
                    if is_empty_down_left and not (is_empty_up or is_empty_left or is_empty_down or is_empty_right or is_empty_up_left or is_empty_up_right or is_empty_down_right):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_CORNER_2)
                    elif is_empty_down_right and not (
                        is_empty_up or is_empty_left or is_empty_down or is_empty_right or
                        is_empty_up_left or is_empty_up_right or is_empty_down_left
                    ):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_CORNER_1)
                    elif is_empty_up_left and not (is_empty_up or is_empty_left or is_empty_down or is_empty_right or is_empty_down_left or is_empty_down_right or is_empty_up_right):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_CORNER_4)
                    elif is_empty_up_right and not (is_empty_up or is_empty_left or is_empty_down or is_empty_right or is_empty_down_left or is_empty_down_right or is_empty_up_left):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_CORNER_3)
                    elif is_empty_up and is_empty_down and not is_empty_left and not is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_TOP_BOTTOM_EDGE)
                    elif is_empty_up and is_empty_down and not is_empty_left and is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_ONLY_LEFT)
                    elif is_empty_up and is_empty_down and is_empty_left and not is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_ONLY_RIGHT)
                    elif is_empty_down and is_empty_left and is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_BOTTOM_COLUMN)
                    elif is_empty_up and is_empty_left and is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_TOP_COLUMN)
                    elif is_empty_left and is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_MIDDLE_COLUMN)
                    elif is_empty_up and is_empty_left:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_TOP_LEFT_CORNER)
                    elif is_empty_down and is_empty_right and not is_empty_up and not is_empty_left:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_BOTTOM_RIGHT_CORNER)
                    elif is_empty_up and is_empty_right and not is_empty_down and not is_empty_right:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_TOP_RIGHT_CORNER)
                    elif is_empty_up:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_WITH_TOP_EDGE)
                    elif tile_left and not (tile_left.cell == 0 or tile_left.perimeter):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_WITH_LEFT_EDGE)
                    elif tile_right and not (tile_right.cell == 0 or tile_right.perimeter):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_WITH_RIGHT_EDGE)
                    elif tile_down and not (tile_down.cell == 0 or tile_down.perimeter):
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL_WITH_BOTTOM_EDGE)
                    else:
                        texture = self.sprite_sheet_1.get_texture(rect=BRICK_WALL)
                    sprite = arcade.Sprite(texture, scale=SPRITE_SCALE)

                    sprite.left = x
                    sprite.bottom = y
                    self.wall_list.append(sprite)

                if tile.door:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("sprites/door-ns.png")
                    else:
                        sprite = arcade.Sprite("sprites/door-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.locked:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("sprites/door-locked-ns.png")
                    else:
                        sprite = arcade.Sprite("sprites/door-locked-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.trapped:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("sprites/door-trapped-ns.png")
                    else:
                        sprite = arcade.Sprite("sprites/door-trapped-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.secret:
                    left_tile = tile = self.dungeon_map.tiles[row][column - 1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("sprites/door-secret-ns.png")
                    else:
                        sprite = arcade.Sprite("sprites/door-secret-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.stair_up:
                    sprite = arcade.Sprite("sprites/stair-up.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.stair_down:
                    sprite = arcade.Sprite("sprites/stair-down.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                # if tile.label:
                #     sprite = arcade.SpriteSolidColor(
                #         width=GRID_SIZE, height=GRID_SIZE, color=arcade.color.LIGHT_GRAY
                #     )
                #     sprite.left = x
                #     sprite.bottom = y
                #     self.background_list.append(sprite)
