import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Bird"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        ...

    def setup(self):
        self.hero = arcade.load_animated_gif('images/hero_animated.gif')
        self.hero.scale = 0.3
        self.hero.center_y = 200
        self.hero.center_x = 500
        self.hero_list = arcade.SpriteList()
        self.hero_list.append(self.hero)

        self.column = arcade.Sprite('images/column.png')
        self.column.center_x = 200
        self.column.center_y = 200
        self.column_list = arcade.SpriteList()
        self.column_list.append(self.column)

    def on_draw(self):
        self.clear()
        self.hero_list.draw()

        self.column_list.draw()
    def on_update(self, delta_time):
        self.hero_list.update_animation()

    def on_key_press(self, key, modifiers):
        ...


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
