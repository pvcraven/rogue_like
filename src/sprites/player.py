import arcade

from sprites.animated_sprite import AnimatedSprite, load_100x100_textures

ANIMATION_STATE_IDLE_RIGHT = 0
ANIMATION_STATE_WALK_RIGHT = 1
ANIMATION_STATE_ATTACK_1_RIGHT = 2
ANIMATION_STATE_ATTACK_2_RIGHT = 3
ANIMATION_STATE_ATTACK_3_RIGHT = 4

ANIMATION_STATE_IDLE_LEFT = 5
ANIMATION_STATE_WALK_LEFT = 6
ANIMATION_STATE_ATTACK_1_LEFT = 7
ANIMATION_STATE_ATTACK_2_LEFT = 8
ANIMATION_STATE_ATTACK_3_LEFT = 9


class PlayerSprite(AnimatedSprite):
    _sprite_file = "sprites/soldier.png"

    def __init__(self):
        super().__init__()
        self.is_facing_right = True
        self.attack_animation = 0

        sprite_sheet = arcade.SpriteSheet(self._sprite_file)

        # - Face Right
        # Idle, Walk, attack 1, attack 2, attack 3
        sprite_count = [6, 8, 6, 6, 9]
        for i in range(len(sprite_count)):
            self.texture_sets.append(
                load_100x100_textures(sprite_sheet, row=i, count=sprite_count[i])
            )

        # - Face Left
        sprite_sheet.flip_left_right()
        for i in range(len(sprite_count)):
            self.texture_sets.append(
                load_100x100_textures(
                    sprite_sheet, row=i, count=sprite_count[i], from_right=True
                )
            )

        self.animation_state = ANIMATION_STATE_IDLE_RIGHT


    def attack_1(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 1
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_1_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_1_LEFT

    def get_attack_hit_box(self):
        # attack_texture = self.texture_sets[ANIMATION_STATE_ATTACK_1_LEFT][3]
        # return arcade.hitbox.HitBox(attack_texture.hit_box_points)
        # print(self.texture_sets[ANIMATION_STATE_ATTACK_1_LEFT][3].hit_box_points)
        if self.is_facing_right:
            hitbox_points = (0, 25), (0, -25), (40, -30), (40, 30)
        else:
            hitbox_points = (0, 25), (0, -25), (-40, -30), (-40, 30)
        return arcade.hitbox.HitBox(points=hitbox_points, position=self.position)

    def get_attack_damage(self):
        return 1
    
    def attack_2(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 2
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_2_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_2_LEFT

    def attack_3(self):
        """Attack 3 animation."""
        if self.attack_animation > 0:
            return
        self.attack_animation = 3
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_3_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_3_LEFT

    def update(self, delta_time):
        super().update(delta_time)

        if self.attack_animation > 0:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.attack_animation = 0

        elif self.change_x < 0:
            self.is_facing_right = False
            self.animation_state = ANIMATION_STATE_WALK_LEFT

        elif self.change_x > 0:
            self.is_facing_right = True
            self.animation_state = ANIMATION_STATE_WALK_RIGHT

        elif self.change_y != 0:
            if self.is_facing_right:
                self.animation_state = ANIMATION_STATE_WALK_RIGHT
            else:
                self.animation_state = ANIMATION_STATE_WALK_LEFT
        else:
            if self.is_facing_right:
                self.animation_state = ANIMATION_STATE_IDLE_RIGHT
            else:
                self.animation_state = ANIMATION_STATE_IDLE_LEFT
