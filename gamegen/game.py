import arcade
import world
import ship
from params import *

class Game(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)
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
        self.gui = None
        self.physics_engine = None
        self.world_camera = None
      
        
        self.screen_half_width = self.width / 2
        self.screen_half_height = self.height / 2
        
        self.score = 0
        
    def setup(self):
        self.ship = ship.Ship(22, 25)
        self.world = world.World()
        self.world.setup()
        
        start_x, start_y = self.world.find_starting_position()        
        self.ship.center_x = start_x
        self.ship.center_y = start_y
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.ship, self.world.wall_list)
        self.world_camera = arcade.Camera(self.width, self.height)        
        
        
    def on_draw(self):

        #self.clear()
        self.world_camera.use()
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
        
        self.mouse_world_x = self.mouse_x + self.world_camera.position[0]
        self.mouse_world_y = self.mouse_y + self.world_camera.position[1]   

        self.ship.update(self.mouse_world_x, self.mouse_world_y)
        self.ship.change_x *= SHIP_FRICTION
        self.ship.change_y *= SHIP_FRICTION

        self.physics_engine.update()
        
        camera_x = self.ship.center_x - self.screen_half_width
        camera_y = self.ship.center_y - self.screen_half_height
        
        camera_x, camera_y = self.world.clamp_camera(camera_x, camera_y, 
                        self.width, self.height)
        
        #results = self.ship.collides_with_list(self.world.object_list)
        #if results:
        #    print (results[0].tile_type)
        
        self.world_camera.move_to((camera_x, camera_y))
        
        self.score-=delta_time