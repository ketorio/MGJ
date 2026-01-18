import arcade
global cur_volume


cur_volume = 0.5

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"
VOLUME_MIN = 0
VOLUME_MAX = 100
DEFAULT_VOLUME = 50
color2 = arcade.color.ARSENIC
color1 = arcade.color.BYZANTINE
color3 = arcade.color.FLIRT
PLAYING = False


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        sound = arcade.load_sound("music/mainbg.m4a")
        global PLAYING
        if not PLAYING:
            self.player = arcade.play_sound(
                sound,
                volume=cur_volume,
                pan=-1.0,
                loop=True,
                speed=1.0,
            )
            PLAYING = True
        else:
            self.player = None
        self.last_volume = cur_volume
        self.titles = ["settings", "play", "extras"]
        self.selected_index = 1
        self.texture = arcade.load_texture("bg/menu.jpg")

    def update_volume(self, new_volume):
        """Обновляет громкость текущего звука"""
        if self.player:
            self.player.volume = new_volume

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
            if self.selected_index == 0:
                settings_view = Settings(self)
                self.window.show_view(settings_view)

class VolumeSlider:
    def __init__(self, center_x, center_y, width=550, height=30, min_value=0, max_value=100):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = DEFAULT_VOLUME

        self.left = center_x - width // 2
        self.right = center_x + width // 2
        self.top = center_y + height // 2
        self.bottom = center_y - height // 2

        self.thumb_radius = 20
        self.thumb_x = self.value_to_x(self.value)
        self.thumb_y = center_y

        self.track_color = arcade.color.GRAY
        self.fill_color = arcade.color.GREEN
        self.thumb_color = arcade.color.ASH_GREY  # COOL_GREY
        self.thumb_border_color = arcade.color.JAPANESE_INDIGO

    def value_to_x(self, value):
        normalized = (value - self.min_value) / (self.max_value - self.min_value)
        return self.left + normalized * self.width

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))
        self.thumb_x = self.value_to_x(self.value)
        return self.value

    def draw(self):
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH // 2,
                                             SCREEN_HEIGHT // 2,
                                             550, 11),
                                 arcade.color.JAPANESE_INDIGO,
                                 3)  # BATTLESHIP_GREY


        arcade.draw_circle_filled(
            self.thumb_x, self.thumb_y,
            self.thumb_radius,
            self.thumb_color
        )
        arcade.draw_circle_outline(
            self.thumb_x, self.thumb_y,
            self.thumb_radius,
            self.thumb_border_color,
            2.5
        )


class Settings(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.m = menu_view
        self.texture = arcade.load_texture("bg/setting.png")
        self.slider = VolumeSlider(
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )

        self.volume = int(cur_volume*100)
        self.slider.set_value(self.volume)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.slider.draw()
        volume_x = SCREEN_WIDTH // 2
        volume_y = SCREEN_HEIGHT // 2 - 100

        arcade.draw_text(
            str(self.volume),
            volume_x,
            volume_y + 10,
            arcade.color.JAPANESE_INDIGO,
            36,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            "%",
            volume_x + 35,
            volume_y,
            arcade.color.JAPANESE_INDIGO,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            'Нажмите Backspace, чтобы вернуться в меню',
            10,
            10,
            arcade.color.WHITE,
            12,
            font_name="Lucida Calligraphy"
        )

    def on_key_press(self, key, modifiers):
        global cur_volume
        if key == arcade.key.UP:
            self.volume = self.slider.set_value(self.volume + 5)
            cur_volume = self.volume / 100.0
            self.m.update_volume(cur_volume)

        elif key == arcade.key.DOWN:
            self.volume = self.slider.set_value(self.volume - 5)
            cur_volume = self.volume / 100.0
            self.m.update_volume(cur_volume)

        elif key == arcade.key.BACKSPACE:
            menu_view = Menu()
            self.window.show_view(menu_view)


