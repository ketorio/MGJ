import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"
color2 = arcade.color.ARSENIC
color1 = arcade.color.BYZANTINE
color3 = arcade.color.FLIRT


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        self.titles = ["settings", "play", "extras"]
        self.selected_index = 1
        self.texture = arcade.load_texture("images/menu.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        x = 250
        y = 70

        for i, name in enumerate(self.titles):
            is_selected = False
            x2 = x + i * 400
            if self.selected_index == i:
                is_selected = True

            font_size = 40 if is_selected else 35
            color = color1 if is_selected else color2

            arcade.draw_text(
                name,
                x2, y,
                color,
                font_size=font_size,
                anchor_x="center",
                anchor_y="center",
                font_name="Algerian",
            )

            if is_selected:
                if self.selected_index == 1:
                    arcade.draw_circle_filled(
                        x2 - 100, y, 10, color3)
                else:
                    arcade.draw_circle_filled(
                        x2 - 140, y, 10, color3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.selected_index > 0:
                self.selected_index -= 1
        elif key == arcade.key.RIGHT:
            if self.selected_index < len(self.titles) - 1:
                self.selected_index += 1
        elif key == arcade.key.ENTER:
            if self.selected_index == 1:
                pass