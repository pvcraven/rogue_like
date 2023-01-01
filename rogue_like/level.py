import arcade

from dungeon_map import DungeonMap
from constants import GRID_SIZE

class Level:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.dungeon_map = DungeonMap()

    def load(self, filename):

        self.dungeon_map.load(filename)

        # Opening JSON file

        for row in range(self.dungeon_map.map_height):
            for column in range(self.dungeon_map.map_width):
                x = column * GRID_SIZE
                y = (self.dungeon_map.map_height * GRID_SIZE) - (row * GRID_SIZE)

                tile = self.dungeon_map.tiles[row][column]
                if tile.cell == 0 or tile.perimeter:
                    sprite = arcade.SpriteSolidColor(GRID_SIZE, GRID_SIZE, arcade.color.BLACK)
                    sprite.left = x
                    sprite.bottom = y
                    self.wall_list.append(sprite)

                if tile.door:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.locked:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-locked-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-locked-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.trapped:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-trapped-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-trapped-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.secret:
                    left_tile = tile = self.dungeon_map.tiles[row][column-1]
                    if left_tile.cell == 0 or left_tile.perimeter:
                        sprite = arcade.Sprite("../sprites/door-secret-ns.png")
                    else:
                        sprite = arcade.Sprite("../sprites/door-secret-ew.png")
                    sprite.scale = GRID_SIZE / sprite.width

                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)

                if tile.label:
                    sprite = arcade.SpriteSolidColor(GRID_SIZE, GRID_SIZE, arcade.color.LIGHT_GRAY)
                    sprite.left = x
                    sprite.bottom = y
                    self.background_list.append(sprite)
