import arcade
import math
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
    HURT_LEFT = 10
    DEATH_LEFT = 11


class Slime(Creature):
    """
    Represents a monster entity with specific attributes and behaviors.
    Inherits from the Entity class.
    """

    def __init__(self, level=None):
        super().__init__(level=level)
        self.name = "Slime"
        self.is_facing_right = True
        self.attack_animation = 0
        self.visible_color = 255, 255, 255, 255
        self.not_visible_color = 255, 255, 255, 0
        self.seen_color = 255, 255, 255, 0
        self.health = 2
        self.texture_clock = 0
        self.animation_state = self.get_animation_states().WALK_LEFT
        self.speed = 0.2

        sprite_sheet = SpriteSheet("sprites/Slime.png")

        # - Face Right
        # Idle, Walk, attack 1, attack 2, hurt, death
        sprite_count = [6, 6, 6, 6, 4, 4]
        self._load_textures(sprite_sheet, sprite_count)
        self.physics_engine = arcade.PhysicsEngineSimple(self, self.level.wall_list)

    def get_animation_states(self):
        """Return the animation states class for the Slime"""
        return SlimeAnimationStates

    def update(self, delta_time):
        super().update(delta_time)

        anim = self.get_animation_states()

        if self.attack_animation > 0:
            animation_length = len(self.texture_sets[self.animation_state]) / 10
            halfway_point = animation_length / 2

            # Trigger attack at halfway point if not already triggered
            if (
                not self.attack_triggered
                and self.texture_clock >= halfway_point
                and self.level
            ):
                self.attack_triggered = True
                self.level.attack(self, self.level.player_list)

            if self.texture_clock >= animation_length:
                self.attack_animation = 0
                self.attack_triggered = False

        elif self.animation_state == anim.DEATH_LEFT:
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

        for player in self.level.player_list:
            has_line_of_sight = arcade.has_line_of_sight(
                observer=self.position,
                target=player.position,
                walls=self.level.wall_list,
                max_distance=200,
                check_resolution=8,
            )
            if has_line_of_sight:
                if player.center_x < self.center_x:
                    self.is_facing_right = False
                else:
                    self.is_facing_right = True

                # Calculate angle to player
                angle = arcade.math.get_angle_radians(
                    self.center_x, self.center_y, player.center_x, player.center_y
                )
                self.change_x = self.speed * math.sin(angle)
                self.change_y = self.speed * math.cos(angle)
                self.physics_engine.update()

                distance = arcade.get_distance_between_sprites(self, player)
                if (
                    distance < 100
                    and not self.attack_animation
                    and self.animation_state
                    not in (
                        anim.DEATH_LEFT,
                        anim.DEATH_RIGHT,
                        anim.HURT_LEFT,
                        anim.HURT_RIGHT,
                    )
                ):
                    self.animation_state = (
                        anim.ATTACK_1_RIGHT
                        if self.is_facing_right
                        else anim.ATTACK_1_LEFT
                    )
                    self.attack_1()
