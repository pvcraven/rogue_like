from arcade import SpriteSheet

from sprites.animated_sprite import AnimatedSprite, load_100x100_textures

ANIMATION_STATE_IDLE_RIGHT = 0
ANIMATION_STATE_WALK_RIGHT = 1
ANIMATION_STATE_ATTACK_1_RIGHT = 2
ANIMATION_STATE_ATTACK_2_RIGHT = 3
ANIMATION_HURT_RIGHT = 4
ANIMATION_DEATH_RIGHT = 5

ANIMATION_STATE_IDLE_LEFT = 6
ANIMATION_STATE_WALK_LEFT = 7
ANIMATION_STATE_ATTACK_1_LEFT = 8
ANIMATION_STATE_ATTACK_2_LEFT = 9
ANIMATION_HURT_LEFT = 9
ANIMATION_DEATH_LEFT = 10

class Slime(AnimatedSprite):
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
        self.animation_state = ANIMATION_STATE_WALK_LEFT

        sprite_sheet = SpriteSheet("sprites/Slime.png")

        # - Face Right
        # Idle, Walk, attack 1, attack 2, hurt, death
        sprite_count = [6, 6, 6, 6, 4, 4]
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

    def attack_1(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 1
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_1_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_1_LEFT

    def attack_2(self):
        if self.attack_animation > 0:
            return
        self.attack_animation = 2
        self.texture_clock = 0
        if self.is_facing_right:
            self.animation_state = ANIMATION_STATE_ATTACK_2_RIGHT
        else:
            self.animation_state = ANIMATION_STATE_ATTACK_2_LEFT

    def update(self, delta_time):
        super().update(delta_time)

        if self.attack_animation > 0:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.attack_animation = 0

        if self.animation_state == ANIMATION_DEATH_LEFT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.remove_from_sprite_lists()
                
        elif self.animation_state == ANIMATION_DEATH_RIGHT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.remove_from_sprite_lists()

        elif self.animation_state == ANIMATION_HURT_LEFT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.animation_state = ANIMATION_STATE_IDLE_LEFT
                
        elif self.animation_state == ANIMATION_HURT_RIGHT:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            if self.texture_clock >= animation_length:
                self.animation_state = ANIMATION_STATE_IDLE_RIGHT

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

    def take_damage(self, damage):
        """Handle taking damage."""
        # Implement damage handling logic here
        print(f"{self.name} took {damage} damage.")
        # For example, you could reduce health or trigger a death animation
        self.health -= damage

        self.texture_clock = 0
        if self.health > 0:
            if self.is_facing_right:
                self.animation_state = ANIMATION_HURT_RIGHT
            else:
                self.animation_state = ANIMATION_HURT_LEFT
        else:
            if self.is_facing_right:
                self.animation_state = ANIMATION_DEATH_RIGHT
            else:
                self.animation_state = ANIMATION_DEATH_LEFT