import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Solid Color Sprite Example"

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.sprite = None

    def setup(self):
        self.sprite = arcade.SpriteSolidColor(100, 100, arcade.color.BLUE)
        self.sprite.left = 50
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.sprite)

    def on_draw(self):
        arcade.start_render()
        self.sprite_list()

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()