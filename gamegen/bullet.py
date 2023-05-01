import arcade


class Bullet(arcade.SpriteSolidColor):        
    def __init__(self, x, y, width, height, color):
        super().__init__(width, height, color)
        self.center_x = x
        self.center_y = y
        
    def on_update():
        self.center_x += self.change_x
        self.center_y += self.change_y
        