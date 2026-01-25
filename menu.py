import arcade
from arcade.gui import UIManager, UIBoxLayout, UISlider, UIAnchorLayout, UILabel

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"
VOLUME_MIN = 0
VOLUME_MAX = 100
DEFAULT_VOLUME = 50
color2 = arcade.color.ARSENIC
color1 = arcade.color.BYZANTINE
color3 = arcade.color.FLIRT

current_volume = 0.5
music_player = None
music_playing = False


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("bg/menu.jpg")
        self.titles = ["settings", "play", "extras"]
        self.selected_index = 1
        self._init_music()

    def _init_music(self):
        global music_player, music_playing, current_volume

        if not music_playing:
            sound = arcade.load_sound("music/mainbg.m4a")
            music_player = arcade.play_sound(
                sound,
                volume=current_volume,
                pan=-1.0,
                loop=True,
                speed=1.0,
            )
            music_playing = True

    def update_volume(self, new_volume):
        global current_volume, music_player
        current_volume = new_volume
        if music_player:
            music_player.volume = current_volume

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
            arcade.draw_text(
                'Нажмите Enter, чтобы выбрать',
                10,
                10,
                arcade.color.BLACK,
                12,
                font_name="Lucida Calligraphy"
            )

            if is_selected:
                if self.selected_index == 1:
                    arcade.draw_circle_filled(
                        x2 - 100, y, 10, color3)
                else:
                    arcade.draw_circle_filled(
                        x2 - 140, y, 10, color3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
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
            elif self.selected_index == 2:
                extra_view = Extras()
                self.window.show_view(extra_view)


class Settings(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.texture = arcade.load_texture("bg/setting.png")

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=5)
        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        self.slider = UISlider(width=550, height=40, min_value=VOLUME_MIN, max_value=VOLUME_MAX,
                               value=int(current_volume * 100))
        self.box_layout.add(self.slider)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))

        self.manager.draw()
        x = int(current_volume * 100)
        arcade.draw_text(
            f"Volume: {x}%",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 48,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            font_name="Lucida Calligraphy"
        )
        arcade.draw_text(
            'Нажмите Backspace, чтобы вернуться в меню',
            10,
            10,
            arcade.color.WHITE,
            12,
            font_name="Lucida Calligraphy"
        )

    def on_update(self, delta_time: float):
        global current_volume
        current_vol = self.slider.value / 100.0
        current_volume = current_vol
        self.menu_view.update_volume(current_volume)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        global current_volume
        if key == arcade.key.BACKSPACE:
            menu_view = Menu()
            self.window.show_view(menu_view)
        elif key == arcade.key.UP:
            x = min(self.slider.value + 5, VOLUME_MAX)
            self.slider.value = x
            self.menu_view.update_volume(self.slider.value / 100.0)
        elif key == arcade.key.DOWN:
            x = max(self.slider.value - 5, VOLUME_MIN)
            self.slider.value = x
            self.menu_view.update_volume(self.slider.value / 100.0)


class Extras(arcade.View):
    def __init__(self, menu_view=None):
        super().__init__()
        self.menu_view = menu_view
        self.texture = arcade.load_texture("bg/black_fon.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_text(
            'Mad girl journey',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.15,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            font_name="Lucida Calligraphy"
        )
        arcade.draw_text(
            '-------------------',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.28,
            arcade.color.WHITE,
            60,
            anchor_x="center",
        )
        arcade.draw_text(
            'CC BY',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.35,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )
        arcade.draw_text(
            'Разработчики: Ketori, Haru',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.53,
            arcade.color.WHITE,
            25,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            'Работа с python arcade: Ketori, Haru',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.76,
            arcade.color.WHITE,
            23,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            'Спрайты, фоны, UI: Ketori, Haru',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.95,
            arcade.color.WHITE,
            23,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            'Сделано с помощью',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2.4,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            'Python',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2.75,
            arcade.color.WHITE,
            25,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            'Arcade версия 3.3.3',

            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3.3,
            arcade.color.WHITE,
            25,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            '-------------------',

            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 4.5,
            arcade.color.WHITE,
            45,
            anchor_x="center",
            font_name="Tw Cen Mt"
        )
        arcade.draw_text(
            'Sweet baka❀ 2026',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 6.2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
            font_name="Tw Cen Mt"
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
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.BACKSPACE:
            if self.menu_view:
                self.window.show_view(self.menu_view)
            else:
                menu_view = Menu()
                self.window.show_view(menu_view)
