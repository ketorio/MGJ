import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"

cur_volume = 0.5

class Level1(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("bg/level1scene1.png")
        self.time_elapsed = 0.0
        self.black_screen_duration = 3.0
        self.player = None

        try:
            sound = arcade.load_sound("music/level1.m4a")
            print(f"Звук загружен: {sound}")
            self.player = arcade.play_sound(
                sound,
                volume=1.0,
                pan=-1.0,
                loop=True,
                speed=1.0,
            )
            print(f"Музыка запущена: {self.player}")
        except Exception as e:
            print(f"Ошибка при загрузке музыки: {e}")

    def on_draw(self):
        self.clear()
        
        if self.time_elapsed < self.black_screen_duration:
            pass
        else:
            arcade.draw_texture_rect(self.texture,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2,
                                                      SCREEN_WIDTH,
                                                      SCREEN_HEIGHT))

    def on_update(self, delta_time):
        self.time_elapsed += delta_time
        


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = Level1()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()