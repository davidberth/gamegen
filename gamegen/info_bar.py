import arcade

class InfoBar(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)
        self.font_size = 16
        self.score = 0
        self.previous_score = 0
        self.max_score = 0
        self.camera = arcade.Camera(self.window.width, self.window.height)
        
        
    def on_draw(self):
        score_text = f"Score: {self.score}   Previous Score: {self.previous_score}  Max Score: {self.max_score}"
        self.camera.use()
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top,
                                          self.bottom, (0, 14, 0))
        arcade.draw_text(score_text, self.left + 5, self.bottom + 5, arcade.color.WHITE, self.font_size)

        