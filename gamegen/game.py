import arcade
import ship
import world
from params import *

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=False, vsync=True, center_window=True)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.ship = None
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_world_x = 0
        self.mouse_world_y = 0
        
        self.world = None
        
        self.physics_engine = None
        
        self.camera = None
        
        self.screen_half_width = SCREEN_WIDTH / 2
        self.screen_half_height = SCREEN_HEIGHT / 2
        
    def setup(self):
        self.ship = ship.Ship(22, 25)
        self.ship.center_x = self.screen_half_width
        self.ship.center_y = self.screen_half_height
        self.world = world.World()
        self.world.setup()
        self.physics_engine = arcade.PhysicsEngineSimple(self.ship, self.world.wall_list)
        self.camera = arcade.Camera()        
        
    def on_draw(self):

        self.clear()
        self.camera.use()
        self.world.draw()
        self.ship.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x 
        self.mouse_y = y                
    
    def on_key_press(self, key, modifiers):
           
        if key == arcade.key.A:
            self.key_left = True
        elif key == arcade.key.D:
            self.key_right = True
        elif key == arcade.key.W:
            self.key_up = True
        elif key == arcade.key.S:
            self.key_down = True
                
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.A:
            self.key_left = False
        elif key == arcade.key.D:
            self.key_right = False
        elif key == arcade.key.W:
            self.key_up = False
        elif key == arcade.key.S:
            self.key_down = False     
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
                
    def on_update(self, delta_time):
        x_force = 0.0
        y_force = 0.0
        if self.key_left:
            x_force-=PLAYER_MOVEMENT_FORCE
        if self.key_right:
            x_force+=PLAYER_MOVEMENT_FORCE
        if self.key_up:
            y_force+=PLAYER_MOVEMENT_FORCE
        if self.key_down:
            y_force-=PLAYER_MOVEMENT_FORCE
                
        self.ship.change_x+= x_force   
        self.ship.change_y+= y_force
        if self.ship.change_x > PLAYER_MOVEMENT_SPEED:
            self.ship.change_x = PLAYER_MOVEMENT_SPEED
        if self.ship.change_x < -PLAYER_MOVEMENT_SPEED:
            self.ship.change_x = -PLAYER_MOVEMENT_SPEED
        if self.ship.change_y > PLAYER_MOVEMENT_SPEED:
            self.ship.change_y = PLAYER_MOVEMENT_SPEED
        if self.ship.change_y < -PLAYER_MOVEMENT_SPEED:
            self.ship.change_y = -PLAYER_MOVEMENT_SPEED
        
        self.mouse_world_x = self.mouse_x + self.camera.position[0]
        self.mouse_world_y = self.mouse_y + self.camera.position[1]   

        self.ship.update(self.mouse_world_x, self.mouse_world_y)
        self.ship.change_x *= SHIP_FRICTION
        self.ship.change_y *= SHIP_FRICTION
        
            
        self.physics_engine.update()
        camera_x = self.ship.center_x - self.screen_half_width
        camera_y = self.ship.center_y - self.screen_half_height
        
        camera_x, camera_y = self.world.clamp_camera(camera_x, camera_y, 
                        SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.camera.move_to((camera_x, camera_y))
         
def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    window.setup()
    arcade.run()
    
if __name__ == "__main__":
    main()