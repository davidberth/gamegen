import arcade
import world
import ship
import bullet
from params import *
import hud
import controller
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class Game(arcade.Window, gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}
    def __init__(self, width, height, window_title, controller_type, render_mode, **kwargs):
        super().__init__(width, height, window_title, **kwargs)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.ship = None
        self.target_world_x = 0
        self.target_world_y = 0
        
        self.world = None
        self.gui = None
        self.physics_engine = None
        self.world_camera = None
        
        self.game_height = self.height - GUI_HEIGHT
        self.game_width = self.width
    
        self.game_half_width = self.game_width / 2
        self.game_half_height = self.game_height / 2
        
        self.bullets = None
        self.mouse = arcade.SpriteSolidColor(10, 10, arcade.color.YELLOW)
        self.bullet_force_x = 0.0
        self.bullet_force_y = 0.0
        
        self.hud = hud.HUD(self.width, self.height, GUI_HEIGHT)
        self.human_controller = controller.HumanController(0, 0, self.width, self.height)
        self.nn_controller = controller.NNController(0, 0, self.width, self.height)

        if controller_type == 'human':
            self.controller = self.human_controller
        elif controller_type == 'nn':
            self.controller = self.nn_controller
        self.set_mouse_visible(False)
        
        self.observation_space = spaces.Dict(
        {
            "agent": spaces.Box(np.array([0.0, 0.0]), 
                                np.array([WORLD_WIDTH*TILE_WIDTH, WORLD_HEIGHT*TILE_HEIGHT]), 
                                shape=(2,), dtype=float),
            "target": spaces.Box(np.array([0.0, 0.0]), 
                                np.array([WORLD_WIDTH*TILE_WIDTH, WORLD_HEIGHT*TILE_HEIGHT]), 
                                shape=(2,), dtype=float)
        })
        self.action_space = spaces.Discrete(4)
    
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        return {"ship": (self.ship.center_x, self.ship.center_y), "target": self.world}
  
    def _get_info(self):
        return {self.hud.score}
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
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
        
        observation= self._get_obs()
        info = self._get_info()
        return observation, info
        
        
    def draw(self):
        self.clear()
        self.world_camera.use()
        self.world.draw()
        self.ship.draw()
        self.bullets.draw()
        self.mouse.draw()
        self.hud.draw()
                        
    def step(self, action):
        
        self.dispatch_events()  
        
        self.controller.action_left = False
        self.controller.action_right = False
        self.controller.action_up = False
        self.controller.action_down = False
        self.controller.fire = False
        
        if action == 0:
            self.controller.action_left = True
        if action == 1:
            self.controller.action_right = True
        if action == 2:
            self.controller.action_up = True
        if action == 3:
            self.controller.action_down = True
        
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
            
        self.hud.score-=0.000001
        
        self.mouse.center_x = self.target_world_x
        self.mouse.center_y = self.target_world_y
        
        if self.render_mode == 'human':
     
            self.draw()
            self.flip()
     
            
        observation= self._get_obs()
        info = self._get_info()
        
        return observation, info
        
        