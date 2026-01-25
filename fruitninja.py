import random
import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = ""
DASH_TIME = 0.3
FRUIT_SCALE = 0.5
FALL_SPEED = -4


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BUFF)
        self.pomo = Frupomo("sprites/frupomo.png", 0.7)
        self.batch = Batch()

    def setup(self):
        self.pomo.center_x = SCREEN_WIDTH // 2
        self.pomo.center_y = SCREEN_HEIGHT // 6
        self.timer = 0
        self.is_dashing = False
        self.pomo_list = arcade.SpriteList()
        self.pomo_list.append(self.pomo)
        self.fruit_list = arcade.SpriteList()
        self.fruit_gif_list = arcade.SpriteList()
        self.score = 0
        self.game_over = False
        for _ in range(1):
            arcade.schedule(self.generate_fruit, 1)

    def generate_fruit(self, time):
        fruit1 = arcade.Sprite("sprites/fruit1.png", FRUIT_SCALE)
        fruit2 = arcade.Sprite("sprites/fruit2.png", FRUIT_SCALE)
        fruit1.center_x = random.randint(130, SCREEN_WIDTH - 130)
        fruit1.center_y = random.randint(SCREEN_HEIGHT + 300, SCREEN_HEIGHT + 400)
        fruit1.name = 'fr1'
        fruit2.center_x = random.randint(130, SCREEN_WIDTH - 130)
        fruit2.center_y = random.randint(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 300)
        fruit2.name = 'fr2'
        self.fruit_list.append(fruit1)
        self.fruit_list.append(fruit2)

    def on_draw(self):
        self.clear()
        self.pomo_list.draw()
        self.fruit_list.draw()
        self.fruit_gif_list.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        if not self.game_over:
            if self.score == 3:
                self.game_over = True

            for i in self.fruit_gif_list:
                i.center_y -= 7
                i.update_animation(delta_time)

            for fruit in self.fruit_list:
                fruit.center_y += FALL_SPEED
                if fruit.center_y < -50:
                    fruit.remove_from_sprite_lists()
                    self.score += 1

                if arcade.check_for_collision(self.pomo, fruit):
                    if fruit.name == 'fr1':
                        fruitdown = arcade.load_animated_gif('sprites/fruit1down.gif')
                    else:
                        fruitdown = arcade.load_animated_gif('sprites/fruit2down.gif')
                    fruitdown.center_x = fruit.center_x
                    fruitdown.center_y = fruit.center_y
                    fruitdown.scale = fruit.scale
                    self.fruit_gif_list.append(fruitdown)
                    fruit.remove_from_sprite_lists()

            if self.is_dashing:
                if self.pomo.left + self.pomo.change_x <= 0:
                    self.pomo.left = 0
                    self.pomo.change_x = 0
                    self.is_dashing = False
                    self.pomo.pomo_flipped()

                elif self.pomo.right + self.pomo.change_x >= SCREEN_WIDTH:
                    self.pomo.right = SCREEN_WIDTH
                    self.pomo.change_x = 0
                    self.is_dashing = False
                    self.pomo.pomo()

                else:
                    self.pomo.center_x += self.pomo.change_x

                self.timer -= delta_time
                if self.timer <= 0:
                    self.is_dashing = False
                    if self.pomo.change_x > 0:
                        self.pomo.pomo()
                    if self.pomo.change_x < 0:
                        self.pomo.pomo_flipped()
        self.text = arcade.Text(
            f"score: {self.score}",
            10, SCREEN_HEIGHT - 50,
            color=arcade.color.BLACK,
            font_size=24,
            font_name='Garamond',
            batch=self.batch
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.is_dashing = True
            self.timer = DASH_TIME
            self.pomo.change_x = 10
            self.pomo.pomodash()
        if key == arcade.key.LEFT:
            self.is_dashing = True
            self.timer = DASH_TIME
            self.pomo.change_x = -10
            self.pomo.pomodash_flipped()
        if key == arcade.key.ESCAPE:
            arcade.close_window()


class Frupomo(arcade.Sprite):
    def __init__(self, image_file, scale):
        super().__init__(image_file, scale)
        self.frupomo = arcade.load_texture("sprites/frupomo.png")
        self.frupomo_flipped = self.frupomo.flip_horizontally()
        self.frupomodash = arcade.load_texture("sprites/frupomodash.png")
        self.frupomodash_flipped = self.frupomodash.flip_horizontally()
        self.current_texture = 0

    def pomodash(self):
        self.texture = self.frupomodash

    def pomodash_flipped(self):
        self.texture = self.frupomodash_flipped

    def pomo(self):
        self.texture = self.frupomo

    def pomo_flipped(self):
        self.texture = self.frupomo_flipped


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
