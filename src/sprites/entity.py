import arcade


class Entity(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_visible = False
        self.block_sight = True
        self.visible_color = 255, 255, 255, 255
        self.not_visible_color = 255, 255, 255, 0
        self.seen_color = 255, 255, 255, 128
        self.tile = None
        self.color = self.not_visible_color
