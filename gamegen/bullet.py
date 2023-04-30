import arcade

class Bullet(arcade.Sprite):        
    def __init__(self, texture):
        super().__init__(texture=texture)
        
    def on_update():
        self.center_x += self.change_x
        self.center_y += self.change_y
        