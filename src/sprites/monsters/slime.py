from arcade import SpriteSheet

from sprites.creature import Creature, AnimationStates


class SlimeAnimationStates(AnimationStates):
    """Animation states specific to the Slime"""

    IDLE_RIGHT = 0
    WALK_RIGHT = 1
    ATTACK_1_RIGHT = 2
    ATTACK_2_RIGHT = 3
    HURT_RIGHT = 4
    DEATH_RIGHT = 5

    IDLE_LEFT = 6
    WALK_LEFT = 7
    ATTACK_1_LEFT = 8
    ATTACK_2_LEFT = 9
    HURT_LEFT = 10  # Fixed: was 9, now 10
    DEATH_LEFT = 11  # Fixed: was 10, now 11


class Slime(Creature):
    """
    Represents a monster entity with specific attributes and behaviors.
    Inherits from the Entity class.
    """

    def __init__(self):
        super().__init__()
        self.name = "Slime"
        self.is_facing_right = True
        self.attack_animation = 0
        self.visible_color = 255, 255, 255, 255
        self.not_visible_color = 255, 255, 255, 0
        self.seen_color = 255, 255, 255, 0
        self.health = 2
        self.texture_clock = 0
        self.animation_state = self.get_animation_states().WALK_LEFT

        sprite_sheet = SpriteSheet("sprites/Slime.png")

        # - Face Right
        # Idle, Walk, attack 1, attack 2, hurt, death
        sprite_count = [6, 6, 6, 6, 4, 4]
        self._load_textures(sprite_sheet, sprite_count)

    def get_animation_states(self):
        """Return the animation states class for the Slime"""
        return SlimeAnimationStates

    def attack_1(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 1
        self.texture_clock = 0
        anim = self.get_animation_states()
        if self.is_facing_right:
            self.animation_state = anim.ATTACK_1_RIGHT
        else:
            self.animation_state = anim.ATTACK_1_LEFT

    def attack_2(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 2
        self.texture_clock = 0
        anim = self.get_animation_states()
        if self.is_facing_right:
            self.animation_state = anim.ATTACK_2_RIGHT
        else:
            self.animation_state = anim.ATTACK_2_LEFT

    def update(self, delta_time):
        super().update(delta_time)

        anim = self.get_animation_states()

        if self.attack_animation > 0:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.attack_animation = 0

        if self.animation_state == anim.DEATH_LEFT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.remove_from_sprite_lists()

        elif self.animation_state == anim.DEATH_RIGHT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.remove_from_sprite_lists()

        elif self.animation_state == anim.HURT_LEFT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.animation_state = anim.IDLE_LEFT

        elif self.animation_state == anim.HURT_RIGHT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.animation_state = anim.IDLE_RIGHT

        elif self.change_x < 0:
            self.is_facing_right = False
            self.animation_state = anim.WALK_LEFT

        elif self.change_x > 0:
            self.is_facing_right = True
            self.animation_state = anim.WALK_RIGHT

        elif self.change_y != 0:
            if self.is_facing_right:
                self.animation_state = anim.WALK_RIGHT
            else:
                self.animation_state = anim.WALK_LEFT
        else:
            if self.is_facing_right:
                self.animation_state = anim.IDLE_RIGHT
            else:
                self.animation_state = anim.IDLE_LEFT
