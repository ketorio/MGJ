import arcade
from menu import Menu

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"


class TitleScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.x = 600
        self.y = 0
        self.schedule = False

    def on_draw(self):
        self.clear()
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
        if not self.schedule:
            self.y += 4
        if self.y >= 360 and not self.schedule:
            self.schedule = True
            arcade.schedule(self.transition, 0.5)

    def transition(self, time):
        menu_view = Menu()
        self.window.show_view(menu_view)
        arcade.unschedule(self.transition)
