from sprites.animated_sprite import AnimatedSprite, load_100x100_textures

ANIMATION_STATE_IDLE_RIGHT = 0

class Creature(AnimatedSprite):

    def __init__(self):
        super().__init__()
        self.is_facing_right = True
        self.attack_animation = 0
        self.level = None
        self.attack_triggered = False 
        self.animation_state = ANIMATION_STATE_IDLE_RIGHT

    def _load_textures(self, sprite_sheet, sprite_count):
        """
        Load textures for the creature.
        This method should be overridden by subclasses to load specific textures.
        """
        for i, count in enumerate(sprite_count):
            self.texture_sets.append(
                load_100x100_textures(sprite_sheet, row=i, count=count)
            )

        # - Face Left
        sprite_sheet.flip_left_right()
        for i, count in enumerate(sprite_count):
            self.texture_sets.append(
                load_100x100_textures(
                    sprite_sheet, row=i, count=count, from_right=True
                )
            )