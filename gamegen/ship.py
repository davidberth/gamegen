import arcade
import math

class Ship(arcade.SpriteSolidColor):

    def __init__(self, width, height):
        super().__init__(width, height, arcade.color.ASH_GREY)

        self.sprite_list = arcade.SpriteList()
        # Set up the base of the ship as a simple square
        self.sprite_list.append(self)

        # Set up the turret of the ship as a rectangle on top of the base
        self.turret_sprite = arcade.SpriteSolidColor(width=8, height=20, color=arcade.color.WHITE)
        self.turret_sprite.center_x = self.center_x
        self.turret_sprite.center_y = self.center_y
        self.sprite_list.append(self.turret_sprite)

        # Set up the turret angle
        self.turret_angle = 0

    def update(self, mouse_x, mouse_y):
        # Update the position and angle of the turret based on the mouse position
        dx, dy = mouse_x - self.center_x, mouse_y - self.center_y
        self.turret_angle = math.degrees(math.atan2(dy, dx))
        self.turret_sprite.angle = self.turret_angle + 90.0
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) + 90.0

    def draw(self):
        # Draw the ship using the Arcade sprite list
        self.turret_sprite.center_x = self.center_x + math.cos(math.radians(self.turret_angle)) * 12.0
        self.turret_sprite.center_y = self.center_y + math.sin(math.radians(self.turret_angle)) * 12.0
        self.sprite_list.draw()
