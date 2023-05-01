import arcade
import world
import ship
import bullet
from params import *
import numpy as np
from PIL import Image
import math

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
        self.previous_score = 0
        self.max_score = 0
        self.goal_reached = False
        self.bullets = None
        self.bullet_texture = None
        self.mouse = arcade.SpriteSolidColor(10, 10, arcade.color.YELLOW)
        self.bullet_force_x = 0.0
        self.bullet_force_y = 0.0
                
        
    def reset(self):
        self.ship = ship.Ship(22, 25)
        self.world = world.World()
        self.world.reset()
        
        start_x, start_y = self.world.find_starting_position()        
        self.ship.center_x = start_x
        self.ship.center_y = start_y
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.ship, self.world.wall_list)
        self.world_camera = arcade.Camera(self.width, self.height)        
        self.bullets = arcade.SpriteList()
        self.window.set_mouse_visible(False)
        
        
    def on_draw(self):
        self.world_camera.use()
        self.world.draw()
        self.ship.draw()
        self.bullets.draw()
        self.mouse.draw()
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_x = x
        self.mouse_y = y
        self.mouse_world_x = self.world_camera.position[0] + x
        self.mouse_world_y = self.world_camera.position[1] + y
        
        bul = bullet.Bullet(self.ship.center_x, self.ship.center_y, 
                            10, 10, arcade.color.RED)
        
        bul.angle = self.ship.turret_angle
        bul.change_x = math.cos(math.radians(bul.angle)) * BULLET_SPEED
        bul.change_y = math.sin(math.radians(bul.angle)) * BULLET_SPEED
        self.bullet_force_x = -bul.change_x * BULLET_FORCE
        self.bullet_force_y = -bul.change_y * BULLET_FORCE
        self.bullets.append(bul)
        
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
            
        self.ship.change_x+=self.bullet_force_x
        self.ship.change_y+=self.bullet_force_y
        
        self.mouse_world_x = self.mouse_x + self.world_camera.position[0]
        self.mouse_world_y = self.mouse_y + self.world_camera.position[1]   

        self.ship.update(self.mouse_world_x, self.mouse_world_y)
        self.ship.change_x *= SHIP_FRICTION
        self.ship.change_y *= SHIP_FRICTION

        self.bullet_force_x*=0.93
        self.bullet_force_y*=0.93

        self.physics_engine.update()
        
        camera_x = self.ship.center_x - self.screen_half_width
        camera_y = self.ship.center_y - self.screen_half_height
        
        camera_x, camera_y = self.world.clamp_camera(camera_x, camera_y, 
                        self.width, self.height)
        
        results = self.ship.collides_with_list(self.world.object_list)
        if results:
            if results[0].tile_type == 4:
                self.score+=3
                results[0].remove_from_sprite_lists()
            elif results[0].tile_type == 3:
                self.score+=10
                self.goal_reached = True
                
        self.world_camera.move_to((camera_x, camera_y))
        
        for bul in self.bullets:
            bul.update()
            if bul.center_x < 0 or bul.center_x > self.world.world_pixel_width or \
                        bul.center_y < 0 or bul.center_y > self.world.world_pixel_height:
                bul.remove_from_sprite_lists()
            
        self.score-=delta_time
        
        self.mouse.center_x = self.mouse_world_x
        self.mouse.center_y = self.mouse_world_y