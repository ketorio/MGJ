import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Mad girl journey"

class TitleScreen(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        #self.texture = arcade.load_texture("images/1.jpg")

    def setup(self):
        self.x = 600
        self.y = 0

    def on_draw(self):
        self.clear()
        #arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_text(
            "Mad",
            self.x - 200, self.y,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            font_name="castellar")
        arcade.draw_text(
            "girl",
            self.x - 40, SCREEN_HEIGHT - self.y,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            font_name="castellar")
        arcade.draw_text(
            "journey",
            self.x + 190, self.y,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            font_name="castellar")

    def on_update(self, delta_time):
        self.y += 5
        if self.y >= 400:
            self.y = 400


def main():
    game = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()