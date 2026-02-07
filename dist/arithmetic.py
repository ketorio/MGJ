import arcade
import random

from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Arithmetic"


class Arithmetic(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ASH_GREY)
        try:
            self.background = arcade.load_texture("bg/arithmethic.png")
        except:
            self.background = None
        self.game_over = False
        self.won = True
        self.parent_view = None

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=30)

        self.current_example = ""
        self.correct_answer = 0
        self.score = 0
        self.answer_buttons = []

        # Таймер для задержки между примерами
        self.example_timer = 0.0
        self.waiting_for_next = False

        # Таймер для завершения игры
        self.elapsed_time = 0.0
        self.time_limit = 20.0

        self.selected_button = 0
        self.setup_ui()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.generate_example()

    def setup(self):
        """Требует lvl1.py при запуске игры"""
        pass

    def setup_ui(self):
        """Создаёт UI элементы один раз"""
        self.question_label = UILabel(
            text="",
            font_size=50,
            text_color=arcade.color.BLACK,
            width=500,
            align="center",
            font_name="Algerian"
        )
        self.box_layout.add(self.question_label)

        bt_box = UIBoxLayout(vertical=False, space_between=30)
        for i in range(4):
            button = UIFlatButton(text="", width=140, height=70)
            button.on_click = self.on_answer_click

            button.style = {
                "normal": {
                    "font_size": 20,
                    "font_color": arcade.color.LIGHT_STEEL_BLUE,
                    "bg": arcade.color.LIGHT_SLATE_GRAY,
                },
                "hover": {
                    "font_size": 24,
                    "font_color": arcade.color.WHITE,
                    "bg": arcade.color.ORANGE,
                },
                "press": {
                    "font_size": 24,
                    "font_color": arcade.color.WHITE,
                    "bg": arcade.color.DARK_ORANGE,
                }
            }

            self.answer_buttons.append(button)
            bt_box.add(button)
        self.box_layout.add(bt_box)

        self.score_label = UILabel(
            text=f"Incorrect answers: {self.score}",
            font_size=19,
            text_color=arcade.color.GRAY,
            width=200,
            align="center",
            font_name="Times New Roman"
        )
        self.box_layout.add(self.score_label)

        self.status_label = UILabel(
            text="",
            font_size=18,
            text_color=arcade.color.DARK_BLUE_GRAY,
            width=300,
            align="center"
        )
        self.box_layout.add(self.status_label)

    def generate_example(self, time=None):
        if self.game_over or self.waiting_for_next:
            return

        for button in self.answer_buttons:
            button.style = {
                "normal": {
                    "font_size": 20,
                    "font_color": arcade.color.LIGHT_STEEL_BLUE,
                    "bg": arcade.color.LIGHT_SLATE_GRAY,
                },
                "hover": {
                    "font_size": 24,
                    "font_color": arcade.color.WHITE,
                    "bg": arcade.color.ORANGE,
                },
                "press": {
                    "font_size": 24,
                    "font_color": arcade.color.WHITE,
                    "bg": arcade.color.DARK_ORANGE,
                }
            }

        a = random.randint(1, 150)
        b = random.randint(1, 150)
        op = random.choice(["+", "-"])
        if op == "+":
            self.correct_answer = a + b
            self.current_example = f"{a} + {b} = ?"
        else:
            self.correct_answer = a - b
            self.current_example = f"{a} - {b} = ?"

        options = [self.correct_answer]
        print(f"answer_buttons length: {len(self.answer_buttons)}")  # Should print 4
        print(f"options length: {len(options)}")
        while len(options) < 4:
            wrong = self.correct_answer + random.randint(-70, 100)
            if wrong != self.correct_answer and wrong not in options:
                options.append(wrong)
        random.shuffle(options)

        self.question_label.text = self.current_example

        for i, button in enumerate(self.answer_buttons):
            print(i)
            button.text = str(options[i])

        self.status_label.text = ""

    def on_answer_click(self, button):
        if self.game_over or self.waiting_for_next:
            return
        player_answer = int(button.text)

        if player_answer == self.correct_answer:
            self.status_label.text = "Верно!"
            self.status_label.text_color = arcade.color.GREEN
            button.style["normal"]["bg"] = arcade.color.GREEN_YELLOW
            button.style["hover"]["bg"] = arcade.color.GREEN_YELLOW
            button.style["normal"]["font_color"] = arcade.color.WHITE
            button.style["hover"]["font_color"] = arcade.color.WHITE
            button.style["press"]["bg"] = arcade.color.DARK_GREEN
        else:
            self.score += 1
            self.status_label.text = f"Неверно! Ответ: {self.correct_answer}"
            self.status_label.text_color = arcade.color.RED

            button.style["normal"]["bg"] = arcade.color.RUSTY_RED
            button.style["hover"]["bg"] = arcade.color.CRIMSON
            button.style["normal"]["font_color"] = arcade.color.WHITE
            button.style["hover"]["font_color"] = arcade.color.WHITE
            button.style["press"]["bg"] = arcade.color.DARK_RED

        self.score_label.text = f"incorrect answers: {self.score}"
        self.manager.add(self.anchor_layout)

        self.waiting_for_next = True
        self.example_timer = 0.0

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.manager.draw()
        if self.game_over:
            arcade.draw_texture_rect(arcade.load_texture("bg/black.jpg"),
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
            arcade.draw_text("Game Over", SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2, arcade.color.RED, 45, anchor_x="center", anchor_y="center",
                             font_name="Algerian")

        if self.answer_buttons and not self.game_over:
            btn = self.answer_buttons[self.selected_button]

            x1 = btn.position.x - 17
            y1 = btn.position.y + 30
            x = btn.position.x + 70
            y = btn.position.y + 33
            w = btn.width
            h = btn.height

            arcade.draw_circle_filled(x1, y1, 10, arcade.color.FLIRT, )
            arcade.draw_circle_outline(x1, y1, 10, arcade.color.BLACK, 2)
            arcade.draw_rect_outline(arcade.XYWH(x, y, w, h), arcade.color.FLIRT, 5)
            arcade.draw_rect_outline(arcade.XYWH(x, y, w + 2, h + 1), arcade.color.BLACK, 2)

    def on_update(self, delta_time: float):
        self.elapsed_time += delta_time

        if self.elapsed_time >= self.time_limit:
            self.won = True
            self.game_over = True
            if self.parent_view:
                self.parent_view.on_game_finished()
            return

        if self.score >= 3 and not self.game_over:
            self.won = False
            self.game_over = True
            if self.parent_view:
                self.parent_view.on_game_finished()
            return

        if self.waiting_for_next:
            self.example_timer += delta_time
            if self.example_timer >= 1.5:
                self.waiting_for_next = False
                self.example_timer = 0.0
                self.generate_example()

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            return

        if key == arcade.key.ESCAPE:
            arcade.close_window()

        if key == arcade.key.LEFT:
            self.selected_button = (self.selected_button - 1) % 4

        elif key == arcade.key.RIGHT:
            self.selected_button = (self.selected_button + 1) % 4

        elif key == arcade.key.ENTER:
            clicked_button = self.answer_buttons[self.selected_button]
            self.on_answer_click(clicked_button)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = Arithmetic()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
