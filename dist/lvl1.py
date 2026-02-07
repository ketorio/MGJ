import arcade
from FlappyBird import FlappyBird
from fruitninja import Fruitninja
from Targetshooting import TargetShooting
from arithmetic import Arithmetic

# 14
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"


class Level1(arcade.View):
    def __init__(self, menu_view, volume=0.5):
        super().__init__()
        self.menu_view = menu_view
        self.volume = volume
        self.scene1 = arcade.load_texture("bg/level1scene1.png")
        self.scene2 = arcade.load_texture("bg/level1scene2.png")
        self.scene3 = arcade.load_texture("bg/level1scene3.png")
        try:
            self.scene4 = arcade.load_texture("bg/level1scene4.png")
        except:
            self.scene4 = None
        self.player = None
        arcade.set_background_color(arcade.color.BLACK)
        self.time = 3.0
        self.show_image = False
        self.show_scene2 = False
        self.show_scene3 = False
        self.show_scene4 = False
        self.scene1_elapsed_time = 0
        self.scene2_elapsed_time = 0
        self.scene3_elapsed_time = 0
        self.show_gif = False
        self.gif_sprite = None
        self.gif_list = arcade.SpriteList()

        self.gif_elapsed_time = 0.0
        self.playing_second_gif = False
        self.second_gif_elapsed = 0.0
        self.second_gif_duration = 1.0
        self.show_black = False
        self.flappy_opened = False

        self.game_running = False
        self.current_game_instance = None
        self.games = [Arithmetic, FlappyBird, Fruitninja, TargetShooting]
        self.current_game_index = 0
        self.show_scene4 = False
        self.scene4_elapsed_time = 0

        self.game_over = False
        self.game_over_time = 0

        # Новая переменная для отслеживания состояния между играми
        self.showing_intergame_gif = False
        self.intergame_gif_timer = 0.0
        self.intergame_phase = 0  # 0 - нет, 1 - первая гифка, 2 - вторая гифка

        try:
            sound = arcade.load_sound("music/level1.m4a")
            print(f"Звук загружен: {sound}")
            self.player = arcade.play_sound(
                sound,
                volume=self.volume,
                pan=-1.0,
                loop=False,
                speed=1.0,
            )
            print(f"Музыка запущена: {self.player}")
        except Exception as e:
            print(f"Ошибка при загрузке музыки: {e}")

        self.gif_list = arcade.SpriteList()
        try:
            self.run_gif = arcade.load_animated_gif('sprites/ран.gif')
            self.slash_gif = arcade.load_animated_gif('sprites/slash.gif')
        except Exception as e:
            print(f"Ошибка загрузки гифок: {e}")
            self.run_gif = None
            self.slash_gif = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.schedule(self.check_time, 1.0)

    def check_time(self, delta_time):
        self.time -= delta_time
        if self.time <= 0:
            arcade.unschedule(self.check_time)
            self.show_image = True
            self.start()

    def start(self):
        pass

    def on_draw(self):
        self.clear()

        if self.show_scene4 and self.scene4:
            arcade.draw_texture_rect(self.scene4,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))

        elif self.show_gif or self.show_black:
            arcade.draw_texture_rect(arcade.load_texture("bg/black.jpg"),
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))

        elif self.show_scene3:
            arcade.draw_texture_rect(self.scene3,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        elif self.show_scene2:
            arcade.draw_texture_rect(self.scene2,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        elif self.show_image:
            arcade.draw_texture_rect(self.scene1,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.show_gif:
            self.gif_list.draw()

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.RED,
                font_size=80,
                anchor_x="center",
                anchor_y="center",
                font_name="Algerian"
            )

    def on_update(self, delta_time):
        if self.game_over:
            self.game_over_time += delta_time
            if self.game_over_time >= 5.0:
                # Останавливаем музыку перед переходом в меню
                if self.player:
                    self.player = arcade.stop_sound(self.player)
                from menu import Menu
                menu_view = Menu()
                self.window.show_view(menu_view)
            return

        if self.game_running:
            return

        if self.show_scene4:
            self.scene4_elapsed_time += delta_time
            if self.scene4_elapsed_time >= 10.0:
                if self.player:
                    self.player = arcade.stop_sound(self.player)
                from menu import Menu
                menu_view = Menu()
                self.window.show_view(menu_view)
            return

        # Обработка гифок между играми
        if self.showing_intergame_gif:
            self.intergame_gif_timer += delta_time
            
            if self.intergame_phase == 1:  # Первая гифка
                if self.intergame_gif_timer >= 4.0:
                    self.show_second_intergame_gif()
            elif self.intergame_phase == 2:  # Вторая гифка
                if self.intergame_gif_timer >= 1.0:
                    self.end_intergame_gif()
            
            # Обновление анимации гифок
            for gif_sprite in self.gif_list:
                gif_sprite.update_animation(delta_time)
            return

        # Оригинальная логика показа начальных сцен
        if self.show_image and not self.show_scene2:
            self.scene1_elapsed_time += delta_time
            if self.scene1_elapsed_time >= 7.0:
                self.show_scene2 = True
                self.show_image = False
                self.scene2_elapsed_time = 0

        elif self.show_scene2:
            self.scene2_elapsed_time += delta_time
            if self.scene2_elapsed_time >= 7.0 and not self.show_scene3:
                self.show_scene3 = True
                self.show_scene2 = False
                self.show_image = False
                self.scene3_elapsed_time = 0

        elif self.show_scene3:
            self.scene3_elapsed_time += delta_time
            if self.scene3_elapsed_time >= 5.0 and not self.show_gif:
                print("Загрузка первой гифки...")
                for s in list(self.gif_list):
                    s.remove_from_sprite_lists()
                if self.run_gif:
                    self.run_gif.center_x = SCREEN_WIDTH // 2
                    self.run_gif.center_y = SCREEN_HEIGHT // 2
                    self.run_gif.scale = 0.7
                    self.gif_list.append(self.run_gif)
                    self.show_gif = True
                    self.scene3_elapsed_time = 0
                    self.show_scene3 = False
                    self.gif_elapsed_time = 0.0
                    self.playing_second_gif = False
                    print("Первая гифка загружена.")
                else:
                    print("Ошибка: первая гифка не загружена.")

        if self.show_gif and not self.playing_second_gif:
            for gif_sprite in self.gif_list:
                gif_sprite.update_animation(delta_time)
            self.gif_elapsed_time += delta_time
            if self.gif_elapsed_time >= 4.0:
                print("Загрузка второй гифки...")
                for s in list(self.gif_list):
                    s.remove_from_sprite_lists()
                if self.slash_gif:
                    self.slash_gif.center_x = SCREEN_WIDTH // 2
                    self.slash_gif.center_y = SCREEN_HEIGHT // 2 - 50
                    self.slash_gif.scale = 0.7
                    self.gif_list.append(self.slash_gif)
                    self.playing_second_gif = True
                    self.second_gif_elapsed = 0.0
                    print("Вторая гифка загружена.")
                else:
                    print("Ошибка: вторая гифка не загружена.")

        elif self.playing_second_gif:
            for gif_sprite in self.gif_list:
                gif_sprite.update_animation(delta_time)
            self.second_gif_elapsed += delta_time
            if self.second_gif_elapsed >= self.second_gif_duration:
                for s in list(self.gif_list):
                    s.remove_from_sprite_lists()
                self.show_gif = False
                self.playing_second_gif = False
                self.show_black = True
                if not self.game_running:
                    arcade.unschedule(self.open_next_game)
                    arcade.schedule(self.open_next_game, 0.05)

    def start_intergame_gif(self):
        """Начать показ гифок между играми"""
        print("Начало показа гифок между играми...")
        
        # Сброс всех состояний
        self.showing_intergame_gif = True
        self.intergame_phase = 1  # Первая гифка
        self.intergame_gif_timer = 0.0
        
        # Очистка списка гифок
        for s in list(self.gif_list):
            s.remove_from_sprite_lists()
        
        # Показ первой гифки
        if self.run_gif:
            self.run_gif.center_x = SCREEN_WIDTH // 2
            self.run_gif.center_y = SCREEN_HEIGHT // 2
            self.run_gif.scale = 0.7
            self.gif_list.append(self.run_gif)
            self.show_gif = True
        else:
            # Если нет гифки, переходим сразу к следующей игре
            self.end_intergame_gif()

    def show_second_intergame_gif(self):
        """Показать вторую гифку между играми"""
        print("Переход ко второй гифке...")
        self.intergame_phase = 2  # Вторая гифка
        self.intergame_gif_timer = 0.0
        
        # Очистка списка гифок
        for s in list(self.gif_list):
            s.remove_from_sprite_lists()
        
        # Показ второй гифки
        if self.slash_gif:
            self.slash_gif.center_x = SCREEN_WIDTH // 2
            self.slash_gif.center_y = SCREEN_HEIGHT // 2 - 50
            self.slash_gif.scale = 0.7
            self.gif_list.append(self.slash_gif)

    def end_intergame_gif(self):
        """Завершить показ гифок между играми и начать следующую игру"""
        print("Завершение гифок между играми...")
        
        # Сброс всех состояний
        self.showing_intergame_gif = False
        self.intergame_phase = 0
        self.intergame_gif_timer = 0.0
        self.show_gif = False
        
        # Очистка списка гифок
        for s in list(self.gif_list):
            s.remove_from_sprite_lists()
        
        # Запуск следующей игры
        arcade.unschedule(self.open_next_game)
        self.open_next_game()

    def open_next_game(self, delta_time: float = 0):
        if self.current_game_index >= len(self.games):
            return

        if not self.game_running:
            self.game_running = True
            game = self.games[self.current_game_index]
            try:
                game_view = game()
                game_view.setup()
                game_view.parent_view = self
                self.window.show_view(game_view)
                self.current_game_instance = game_view
                self.current_game_index += 1

            except Exception as e:
                print(f"Ошибка {e}")
                self.game_running = False
                arcade.schedule(self.open_next_game, 0.5)

    def close_current_game(self, time):
        try:
            arcade.unschedule(self.close_current_game)
            arcade.unschedule(self.open_next_game)
        except Exception:
            pass

        self.game_running = False
        game_won = self.current_game_instance and self.current_game_instance.won if self.current_game_instance else False
        self.current_game_instance = None

        if game_won:
            if self.current_game_index >= len(self.games):
                print("Все игры завершены! Показываем финальную сцену...")
                self.show_scene4 = True
                self.show_gif = False
                self.show_image = False
                self.show_scene2 = False
                self.show_scene3 = False
                self.show_black = False
                self.scene4_elapsed_time = 0
                
                # Сброс состояния гифок
                self.showing_intergame_gif = False
                self.intergame_phase = 0
                self.intergame_gif_timer = 0.0
            else:
                print("Игрок победил! Начинаем показ гифок между играми...")
                self.start_intergame_gif()
        else:
            print("Игра окончена - игрок проиграл!")
            self.game_over = True
            self.game_over_time = 0
            
            # Сброс состояния гифок
            self.showing_intergame_gif = False
            self.intergame_phase = 0
            self.intergame_gif_timer = 0.0

    def on_game_finished(self):
        """Вызывается игрой когда завершится"""
        print("Игра завершена, возвращаемся в Level1")
        self.window.show_view(self)
        self.close_current_game(0)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.open_next_game()
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = Level1(menu_view=None)
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()