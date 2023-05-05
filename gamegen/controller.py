import arcade
import abc
from enum import Enum, auto

class Controller(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int,
                 **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)
        
        self.action_down = False
        self.action_up = False
        self.action_right = False
        self.action_left = False
        
        self.fire = False
        
        self.target_x = 0
        self.target_y = 0
        
        self.exit = False
        
    
class HumanController(Controller):
    def __init__(self, left: int, bottom: int, width: int, height: int,
                 **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

    def on_key_press(self, key, modifiers):
        print (f'key was pressed!, {key}', self.right)
        if key == arcade.key.A:
            self.action_left = True
        elif key == arcade.key.D:
            self.action_right = True
        elif key == arcade.key.W:
            self.action_up = True
        elif key == arcade.key.S:
            self.action_down = True
        elif key == arcade.key.ESCAPE:
            self.exit = True

    def on_key_release(self, key, modifiers):
        print ('key was released!')
        if key == arcade.key.A:
            self.action_left = False
        elif key == arcade.key.D:
            self.action_right = False
        elif key == arcade.key.W:
            self.action_up = False
        elif key == arcade.key.S:
            self.action_down = False
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.target_x = x
        self.target_y = y
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.fire = True
    
