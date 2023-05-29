import arcade
import numpy as np
from params import *
from PIL import Image
from tile import *

class World:
    def __init__(self):
        self.wall_list = None
        self.tile_map = None
        
    def reset(self):
        
        np.random.seed(34)
        
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.object_list = arcade.SpriteList(use_spatial_hash=True)
        self.level = np.zeros((WORLD_WIDTH, WORLD_HEIGHT), dtype=np.uint8)
        self.fill_walls()
        # self.place_walls()
        self.place_coins()
        self.level[2, 7] = 2
        self.level[17, 7] = 3
            
        sprite_locations = np.where(self.level > 0)

        for x,y in zip(*sprite_locations):
            tile_type = self.level[x, y]
            tile_sprite = Tile(x, y, TILE_WIDTH, TILE_HEIGHT, 1, tile_type)
            
            if tile_type == 1:
                self.wall_list.append(tile_sprite)
            else:
                self.object_list.append(tile_sprite)
                    
        self.world_pixel_height = WORLD_HEIGHT * TILE_HEIGHT
        self.world_pixel_width = WORLD_WIDTH * TILE_WIDTH
        
        self.goal_x, self.goal_y = self.find_goal_position()
        
        
    def fill_walls(self):
        self.level[0, :] = 1
        self.level[-1, :] = 1
        self.level[:, 0] = 1
        self.level[:, -1] = 1
        
    def place_walls(self):
        walls = np.random.choice([0,1], size=(WORLD_WIDTH, WORLD_HEIGHT), p=[0.98, 0.02])
        self.level[(walls == 1) & (self.level == 0)] = 1
    
    def place_coins(self):
        coins = np.random.choice([0,1], size=(WORLD_WIDTH, WORLD_HEIGHT), p=[0.9, 0.1])
        self.level[(coins == 1) & (self.level == 0)] = 4
        #self.level[3:-3, 7] = 4
        
    def find_starting_position(self):
        starting_position = np.where(self.level == 2)
        if starting_position:
            x, y = (starting_position[0][0] + 0.5) * TILE_WIDTH, (starting_position[1][0] + 0.5) * TILE_HEIGHT
        else:
            x, y = 100, 100
        return x, y
    
    def find_goal_position(self):
        goal_position = np.where(self.level == 2)
        if goal_position:
            x, y = (goal_position[0][0] + 0.5) * TILE_WIDTH, (goal_position[1][0] + 0.5) * TILE_HEIGHT
        else:
            x, y = 100, 100
        return x, y
        
    def clamp_camera(self, x, y, width, height):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.world_pixel_width - width:
            x = self.world_pixel_width - width
        if y > self.world_pixel_height - height:
            y = self.world_pixel_height - height
        return x, y
        
    def draw(self):
        self.wall_list.draw()
        self.object_list.draw()