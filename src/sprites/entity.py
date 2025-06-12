import arcade


class Entity(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_visible = False
        self.block_sight = True
        self.visible_color = arcade.color.WHITE
        self.not_visible_color = arcade.color.BLACK
