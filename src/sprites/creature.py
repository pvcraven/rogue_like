from sprites.animated_sprite import AnimatedSprite, load_100x100_textures


# Base animation state constants
class AnimationStates:
    """Base class for animation state constants"""

    IDLE_RIGHT = 0
    WALK_RIGHT = 1
    ATTACK_1_RIGHT = 2
    ATTACK_2_RIGHT = 3

    IDLE_LEFT = None  # Will be set by subclasses
    WALK_LEFT = None
    ATTACK_1_LEFT = None
    ATTACK_2_LEFT = None


class Creature(AnimatedSprite):

    def __init__(self):
        super().__init__()
        self.is_facing_right = True
        self.attack_animation = 0
        self.level = None
        self.attack_triggered = False
        # Use the class's animation constants
        self.animation_state = self.get_animation_states().IDLE_RIGHT

    def get_animation_states(self):
        """
        Return the animation states class for this creature.
        Should be overridden by subclasses to return their specific animation states.
        """
        return AnimationStates

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
                load_100x100_textures(sprite_sheet, row=i, count=count, from_right=True)
            )

    def get_attack_damage(self):
        return 1

    def take_damage(self, damage):
        """Handle taking damage."""
        # Implement damage handling logic here
        print(f"{self.name} took {damage} damage.")
        # For example, you could reduce health or trigger a death animation
        self.health -= damage

        anim = self.get_animation_states()
        self.texture_clock = 0
        if self.health > 0:
            if self.is_facing_right:
                self.animation_state = anim.HURT_RIGHT
            else:
                self.animation_state = anim.HURT_LEFT
        else:
            if self.is_facing_right:
                self.animation_state = anim.DEATH_RIGHT
            else:
                self.animation_state = anim.DEATH_LEFT
