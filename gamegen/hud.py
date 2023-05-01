import arcade


class HUD():
    def __init__(self, window_width, window_height, gui_height):
        self.font_size = 14
        self.score = 0
        self.previous_score = 0
        self.max_score = 0
        self.dx = 0.0
        self.dy = 0.0
        self.window_width = window_width
        self.window_height = window_height
        self.gui_height = gui_height
        self.camera = arcade.Camera(window_width, window_height)

    def draw(self):
        score_text = f"Score: {self.score:.1f}   Previous Score: {self.previous_score} " \
                f"Max Score: {self.max_score}  dx: {self.dx:.2f}  dy: {self.dy:.2f}"
        self.camera.use()
       
        arcade.draw_text(score_text, 5, self.window_height - self.gui_height + 5,
                         arcade.color.WHITE, self.font_size)
