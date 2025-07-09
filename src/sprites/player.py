import arcade

from sprites.creature import Creature, AnimationStates

class PlayerAnimationStates(AnimationStates):
    """Animation states specific to the Player"""
    IDLE_RIGHT = 0
    WALK_RIGHT = 1
    ATTACK_1_RIGHT = 2
    ATTACK_2_RIGHT = 3
    ATTACK_3_RIGHT = 4

    IDLE_LEFT = 5
    WALK_LEFT = 6
    ATTACK_1_LEFT = 7
    ATTACK_2_LEFT = 8
    ATTACK_3_LEFT = 9


class PlayerSprite(Creature):
    _sprite_file = "sprites/soldier.png"

    def __init__(self):
        super().__init__()

        sprite_sheet = arcade.SpriteSheet(self._sprite_file)

        # - Face Right
        # Idle, Walk, attack 1, attack 2, attack 3
        sprite_count = [6, 8, 6, 6, 9]
        self._load_textures(sprite_sheet, sprite_count)

    def get_animation_states(self):
        """Return the animation states class for the Player"""
        return PlayerAnimationStates

    def get_attack_hit_box(self):
        # attack_texture = self.texture_sets[ANIMATION_STATE_ATTACK_1_LEFT][3]
        # return arcade.hitbox.HitBox(attack_texture.hit_box_points)
        # print(self.texture_sets[ANIMATION_STATE_ATTACK_1_LEFT][3].hit_box_points)
        if self.is_facing_right:
            hitbox_points = (0, 25), (0, -25), (40, -30), (40, 30)
        else:
            hitbox_points = (0, 25), (0, -25), (-40, -30), (-40, 30)
        return arcade.hitbox.HitBox(points=hitbox_points, position=self.position)

    def attack_1(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 1
        self.texture_clock = 0
        self.attack_triggered = False
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
        self.attack_triggered = False
        anim = self.get_animation_states()
        if self.is_facing_right:
            self.animation_state = anim.ATTACK_2_RIGHT
        else:
            self.animation_state = anim.ATTACK_2_LEFT

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
