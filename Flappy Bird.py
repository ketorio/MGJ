import arcade
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Bird"
BIRD_SCALE = 0.3
SPIKE_SCALE = 0.8
SPIKE_GAP = 300
SCROLL_SPEED = 4


class FlappyBird(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)
        self.bird = Bird("sprites/bird_wings_up.png", BIRD_SCALE)
        self.spike = arcade.Sprite("sprites/spike.png")
        self.score = 0
        self.scroll_x = 0
        self.game_over = False

    def setup(self):
        self.bird.center_x = 150
        self.bird.center_y = SCREEN_HEIGHT // 2
        self.bird.change_y = 0
        self.bird.current_texture = 0
        self.bird2 = arcade.SpriteList()
        self.bird2.append(self.bird)

        self.spikes = arcade.SpriteList()
        self.score = 0
        self.game_over = False

        for _ in range(2):
            self.generate_SPIKE_top()
            self.generate_SPIKE_bottom()

    def generate_SPIKE_bottom(self):
        spike = arcade.Sprite("sprites/spike.png", SPIKE_SCALE, angle=180)
        spike.center_x = SCREEN_WIDTH + random.randint(50, 300)
        spike.center_y = random.randint(500, 800)
        self.spikes.append(spike)

    def generate_SPIKE_top(self):
        spike = arcade.Sprite("sprites/spike.png", SPIKE_SCALE)
        spike.center_x = SCREEN_WIDTH + random.randint(50, 300)
        spike.center_y = random.randint(-200, 100)
        self.spikes.append(spike)

    def on_update(self, delta_time):
        if not self.game_over:
            self.bird.change_y -= 0.2
            self.bird.center_y += self.bird.change_y

            for spike in self.spikes:
                spike.center_x -= SCROLL_SPEED

                if spike.center_x < -50:
                    spike.remove_from_sprite_lists()
                    self.generate_SPIKE_bottom()
                    self.generate_SPIKE_top()
                    self.score += 1

                if arcade.check_for_collision(self.bird, spike):
                    self.game_over = True

        if self.bird.center_y <= 25:
            self.bird.center_y = 25
        self.bird.change_texture()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.UP:
            self.bird.change_y = 4
        if key == arcade.key.R and self.game_over:
            self.setup()

    def on_draw(self):
        self.clear()
        self.spikes.draw()
        self.bird2.draw()

        if self.game_over:
            arcade.draw_text("Fail", SCREEN_WIDTH // 2 - 180,
                             SCREEN_HEIGHT // 2, arcade.color.RED, 24, anchor_x="center")


class Bird(arcade.Sprite):
    def __init__(self, image_file, scale):
        super().__init__(image_file, scale)
        self.wing_up_texture = arcade.load_texture("sprites/bird_wings_up.png")
        self.wing_down_texture = arcade.load_texture("sprites/bird_wings_down.png")
        self.current_texture = 0

    def change_texture(self):
        if self.change_y > 0:
            self.texture = self.wing_down_texture
        else:  
            self.texture = self.wing_up_texture


def main():
    game = FlappyBird(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

