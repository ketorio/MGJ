import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Target shooting"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.batch = Batch()

    def setup(self):
        self.score = 0
        self.end = False

        self.hero = arcade.Sprite('images/hero.png', 0.6)
        self.hero.center_x = SCREEN_WIDTH // 2
        self.hero.center_y = 100
        self.hero_list = arcade.SpriteList()
        self.hero_list.append(self.hero)

        self.arrow = arcade.Sprite('images/coin.png', 0.08)
        self.arrow.center_x = SCREEN_WIDTH // 2
        self.arrow.center_y = 130
        self.arrow.change_y = 0
        self.arrow_list = arcade.SpriteList()
        self.arrow_list.append(self.arrow)

        self.target = arcade.Sprite('images/coin.png', 0.4)
        self.target.center_x = SCREEN_WIDTH // 2
        self.target.center_y = SCREEN_HEIGHT - 80
        self.target.change_x = 3
        self.target_list = arcade.SpriteList()
        self.target_list.append(self.target)

    def on_draw(self):
        self.clear()
        if self.end:
            arcade.draw_text(
                f"Victory!",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                color=arcade.color.BUFF,
                font_size=45,
                anchor_x='center',
                anchor_y='center',
                font_name='Garamond')
        self.batch.draw()
        self.arrow_list.draw()
        self.hero_list.draw()
        self.target_list.draw()

    def on_update(self, delta_time):
        if self.score == 3:
            self.target.center_x = SCREEN_WIDTH // 2
            self.target.change_x = 0
            self.target.update()
            self.end = True
            return

        if arcade.check_for_collision(self.arrow, self.target):
            self.score += 1
            self.target.change_x *= 2
            self.arrow.change_y = 0
            self.arrow.center_y = 130

        self.text = arcade.Text(
            f"score: {self.score}",
            10, SCREEN_HEIGHT - 50,
            color=arcade.color.BLACK,
            font_size=24,
            font_name='Garamond',
            batch=self.batch
        )
        if self.target.center_x <= 40 or self.target.center_x >= SCREEN_WIDTH - 40:
            self.target.change_x *= -1

        self.arrow.update()
        self.target.update()

        if self.arrow.center_y >= SCREEN_HEIGHT:
            self.arrow.change_y = 0
            self.arrow.center_y = 130

    def on_key_press(self, key, modifiers):
        if self.end:
            if key == arcade.key.ENTER:
                self.setup()
            return
        if key == arcade.key.UP:
            self.arrow.change_y = 9


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
