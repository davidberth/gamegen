import arcade
import abc
from enum import Enum, auto

class Controller(abc.ABC):
    def __init__(self, window):
        self.window = window
        
        self.down = False
        self.up = False
        self.right = False
        self.left = False
        
        self.fire = False
        
        self.target_x = 0
        self.target_y = 0
        
        self.exit = False

    
class HumanController(Controller):
    def __init__(self, window):
        super().__init__(window)

        arcade.register_event_handler(self.on_key_press)
        arcade.register_event_handler(self.on_key_release)
        arcade.register_event_handler(self.on_mouse_motion)
        arcade.register_event_handler(self.on_mouse_press)
        
        #arcade.on_key_press = self.on_key_press
        #arcade.on_key_release = self.on_key_release
        #arcade.on_mouse_motion = self.on_mouse_motion
        #arcade.on_mouse_press = self.on_mouse_press
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.left = True
        elif key == arcade.key.D:
            self.right = True
        elif key == arcade.key.W:
            self.up = True
        elif key == arcade.key.S:
            self.down = True
        elif key == arcade.key.ESCAPE:
            self.exit = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.left = False
        elif key == arcade.key.D:
            self.right = False
        elif key == arcade.key.W:
            self.up = False
        elif key == arcade.key.S:
            self.down = False
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.target_x = x
        self.target_y = y
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire = True
    
