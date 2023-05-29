import arcade


class HUD():
    def __init__(self, window_width, window_height, gui_height):
        self.font_size = 13
        self.score = 0
        self.previous_score = 0
        self.max_score = 0
        self.episode = 1

        self.window_width = window_width
        self.window_height = window_height
        self.gui_height = gui_height
        self.camera = arcade.Camera(window_width, window_height)

    def draw(self):
        score_text = f"Score: {self.score:.1f}   Prev Score: {self.previous_score} " \
                f"Max Score: {self.max_score} " \
                f" Episode: {self.episode}"
        self.camera.use()
       
        arcade.draw_text(score_text, 5, self.window_height - self.gui_height + 5,
                         arcade.color.WHITE, self.font_size)
