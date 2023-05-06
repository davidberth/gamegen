import arcade
import world
import ship
import bullet
from params import *
import hud
import math
import controller

class Game(arcade.View):
    def __init__(self, controller_type):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        self.ship = None
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False
        self.target_world_x = 0
        self.target_world_y = 0
        
        self.world = None
        self.gui = None
        self.physics_engine = None
        self.world_camera = None
        
        self.game_height = self.window.height - GUI_HEIGHT
        self.game_width = self.window.width
    
        self.game_half_width = self.game_width / 2
        self.game_half_height = self.game_height / 2
        
        self.bullets = None
        self.mouse = arcade.SpriteSolidColor(10, 10, arcade.color.YELLOW)
        self.bullet_force_x = 0.0
        self.bullet_force_y = 0.0
        
        self.hud = hud.HUD(self.window.width, self.window.height, GUI_HEIGHT)
        self.human_controller = controller.HumanController(0, 0, self.window.width, self.window.height)
        self.nn_controller = controller.NNController(0, 0, self.window.width, self.window.height)
        
        if controller_type == 'human':
            self.controller = self.human_controller
        elif controller_type == 'nn':
            self.controller = self.nn_controller
        self.section_manager.clear_sections()
        self.add_section(self.controller)
        self.window.set_mouse_visible(False)
        
        
    def reset(self):
        self.ship = ship.Ship(22, 25)
        self.world = world.World()
        self.world.reset()
        
        start_x, start_y = self.world.find_starting_position()        
        self.ship.center_x = start_x
        self.ship.center_y = start_y
        self.ship.angle = 0
        self.ship.change_x = 0
        self.ship.change_y = 0
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.ship, self.world.wall_list)
        self.world_camera = arcade.Camera(self.game_width, self.game_height)        
        self.bullets = arcade.SpriteList()
        
        
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.world.draw()
        self.ship.draw()
        self.bullets.draw()
        self.mouse.draw()
        self.hud.draw()
                        
    def on_update(self, delta_time):
        x_force = 0.0
        y_force = 0.0
        if self.controller.action_left:
            x_force-=PLAYER_MOVEMENT_FORCE
        if self.controller.action_right:
            x_force+=PLAYER_MOVEMENT_FORCE
        if self.controller.action_up:
            y_force+=PLAYER_MOVEMENT_FORCE
        if self.controller.action_down:
            y_force-=PLAYER_MOVEMENT_FORCE
            
        if self.controller.fire:
            self.target_world_x = self.world_camera.position[0] + self.controller.target_x
            self.target_world_y = self.world_camera.position[1] + self.controller.target_y
            
            bul = bullet.Bullet(self.ship.center_x, self.ship.center_y, 
                                10, 10, arcade.color.RED)
            
            bul.angle = self.ship.turret_angle
            bul.change_x = math.cos(math.radians(bul.angle)) * BULLET_SPEED
            bul.change_y = math.sin(math.radians(bul.angle)) * BULLET_SPEED
            self.bullet_force_x = -bul.change_x * BULLET_FORCE
            self.bullet_force_y = -bul.change_y * BULLET_FORCE
            self.bullets.append(bul)
            
                
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
        
        self.target_world_x = self.controller.target_x + self.world_camera.position[0]
        self.target_world_y = self.controller.target_y + self.world_camera.position[1]   

        self.ship.update(self.target_world_x, self.target_world_y)
        self.ship.change_x *= SHIP_FRICTION
        self.ship.change_y *= SHIP_FRICTION

        self.bullet_force_x*=0.93
        self.bullet_force_y*=0.93

        self.physics_engine.update()
        
        camera_x = self.ship.center_x - self.game_half_width
        camera_y = self.ship.center_y - self.game_half_height
        
        camera_x, camera_y = self.world.clamp_camera(camera_x, camera_y, 
                        self.game_width, self.game_height)
        
        results = self.ship.collides_with_list(self.world.object_list)
        if results:
            if results[0].tile_type == 4:
                self.hud.score+=3
                results[0].remove_from_sprite_lists()
            elif results[0].tile_type == 3:
                self.hud.score+=10
                self.hud.previous_score = int(self.hud.score)
                if self.hud.max_score < self.hud.score:
                    self.hud.max_score = int(self.hud.score)
                self.hud.score = 0.0
                self.hud.episode+=1
                self.reset()
                
        self.world_camera.move_to((camera_x, camera_y))
        
        for bul in self.bullets:
            bul.update()
            if bul.center_x < 0 or bul.center_x > self.world.world_pixel_width or \
                        bul.center_y < 0 or bul.center_y > self.world.world_pixel_height:
                bul.remove_from_sprite_lists()
            results = bul.collides_with_list(self.world.wall_list)
            if results:
                bul.remove_from_sprite_lists()
                results[0].color = arcade.color.DARK_BLUE_GRAY
            
        self.hud.score-=delta_time
        
        self.mouse.center_x = self.target_world_x
        self.mouse.center_y = self.target_world_y