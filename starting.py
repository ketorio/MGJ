import arcade
from intro import TitleScreen

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mad girl journey"


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = TitleScreen()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
