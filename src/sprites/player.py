import arcade

from sprites.creature import Creature, AnimationStates

class PlayerAnimationStates(AnimationStates):
    """Animation states specific to the Player"""
    IDLE_RIGHT = 0
    WALK_RIGHT = 1
    ATTACK_1_RIGHT = 2
    ATTACK_2_RIGHT = 3
    ATTACK_3_RIGHT = 4
    HURT_RIGHT = 5
    DEATH_RIGHT = 6

    IDLE_LEFT = 7
    WALK_LEFT = 8
    ATTACK_1_LEFT = 9
    ATTACK_2_LEFT = 10
    ATTACK_3_LEFT = 11
    HURT_LEFT = 12
    DEATH_LEFT = 13


class PlayerSprite(Creature):
    _sprite_file = "sprites/soldier.png"

    def __init__(self):
        super().__init__()

        sprite_sheet = arcade.SpriteSheet(self._sprite_file)

        # - Face Right
        # Idle, Walk, attack 1, attack 2, attack 3, hurt
        sprite_count = [6, 8, 6, 6, 9, 4, 4]
        self._load_textures(sprite_sheet, sprite_count)

    def get_animation_states(self):
        """Return the animation states class for the Player"""
        return PlayerAnimationStates

    def attack_3(self):
        """Attack 3 animation."""
        if self.attack_animation > 0:
            return
        self.attack_animation = 3
        self.texture_clock = 0
        self.attack_triggered = False
        anim = self.get_animation_states()
        if self.is_facing_right:
            self.animation_state = anim.ATTACK_3_RIGHT
        else:
            self.animation_state = anim.ATTACK_3_LEFT

    def update(self, delta_time):
        super().update(delta_time)

        anim = self.get_animation_states()
        
        if self.attack_animation > 0:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            halfway_point = animation_length / 2
            
            # Trigger attack at halfway point if not already triggered
            if not self.attack_triggered and self.texture_clock >= halfway_point and self.level:
                self.attack_triggered = True
                self.level.attack(self, self.level.monster_list)
            
            if self.texture_clock >= animation_length:
                self.attack_animation = 0
                self.attack_triggered = False

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
