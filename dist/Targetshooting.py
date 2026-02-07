import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Target shooting"
ANIMATION_SPEED = 0.1


class Target(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.textures = []
        for i in range(1, 6):
            texture = arcade.load_texture(f"sprites/target{i}.png")
            self.textures.append(texture)
        self.textures_flipped = [texture.flip_horizontally() for texture in self.textures]

        self.texture = self.textures[0]
        self.center_x = x
        self.center_y = y
        self.scale = 0.38

        self.animation_frame = 0
        self.animation_timer = 0
        self.direction = 1  # кароче 1 — вправо / -1 — влево

    def update(self, delta_time, end):
        if end:
            self.texture = self.textures[4]
            return

        if self.change_x > 0:
            self.direction = 1
        else:
            self.direction = -1

        index = self.animation_frame % 4

        if self.direction == 1:
            self.texture = self.textures[index]
        else:
            self.texture = self.textures_flipped[index]

        self.animation_timer += delta_time
        if self.animation_timer > ANIMATION_SPEED:
            self.animation_timer = 0
            self.animation_frame += 1
        self.center_x += self.change_x


class TargetShooting(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.batch = Batch()
        self.time_limit = 30.0
        self.elapsed_time = 0.0
        self.game_over = False
        self.won = False
        self.parent_view = None

    def setup(self):
        self.score = 0
        self.end = False
        self.game_over = False
        self.elapsed_time = 0.0

        self.hero = arcade.Sprite('sprites/pew.png', 0.8)
        self.hero.center_x = SCREEN_WIDTH // 2
        self.hero.center_y = 100
        self.hero_list = arcade.SpriteList()
        self.hero_list.append(self.hero)

        self.arrow = arcade.Sprite('sprites/snaryad.gif', 0.25)
        self.arrow.center_x = SCREEN_WIDTH // 2
        self.arrow.center_y = 100
        self.arrow.change_y = 0
        self.arrow_list = arcade.SpriteList()
        self.arrow_list.append(self.arrow)

        self.target = Target(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
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
        self.target_list.draw()
        self.arrow_list.draw()
        self.hero_list.draw()
        if self.game_over:
            arcade.draw_texture_rect(arcade.load_texture("bg/black.jpg"),
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
            arcade.draw_text("Game Over", SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2, arcade.color.RED, 45, anchor_x="center", anchor_y="center",
                             font_name="Algerian")

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.elapsed_time += delta_time
        if self.elapsed_time >= self.time_limit and self.score < 3:
            self.game_over = True
            self.won = True
            if self.parent_view:
                self.parent_view.on_game_finished()
            return

        if self.score == 3:
            self.target.center_x = SCREEN_WIDTH // 2
            self.target.change_x = 0
            self.target.update(delta_time, True)
            self.end = True
            self.won = True
            if self.parent_view:
                self.parent_view.on_game_finished()
            return

        if arcade.check_for_collision(self.arrow, self.target):
            self.score += 1
            self.target.center_x = SCREEN_WIDTH // 2

            self.target.change_x *= 2
            self.arrow.change_y = 0
            self.arrow.center_y = 100

        self.text = arcade.Text(
            f"score: {self.score}",
            10, SCREEN_HEIGHT - 50,
            color=arcade.color.BLACK,
            font_size=24,
            font_name='Garamond',
            batch=self.batch
        )
        if self.target.center_x <= 30 or self.target.center_x >= SCREEN_WIDTH - 30:
            self.target.change_x *= -1

        self.arrow.update()
        self.target.update(delta_time, False)

        if self.arrow.center_y >= SCREEN_HEIGHT:
            self.arrow.change_y = 0
            self.arrow.center_y = 100

    def on_key_press(self, key, modifiers):
        if self.end:
            if key == arcade.key.ENTER:
                self.setup()
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            return
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.UP:
            self.arrow.change_y = 11
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = TargetShooting()
    view.setup()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
