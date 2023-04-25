import arcade
import numpy as np
from params import *
from PIL import Image

class World:
    def __init__(self):
        self.wall_list = None
        self.tile_map = None
        
    def setup(self):
        
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.level = np.random.choice([0,1], size=(WORLD_WIDTH, WORLD_HEIGHT), p=[0.9, 0.1])
        
        wall_array = np.zeros((TILE_WIDTH, TILE_HEIGHT, 4), dtype=np.uint8)
        wall_array[:, :, 3] = 255
        wall_array[:, :, :3] = 128
        wall_array[0, :, :3] = 0
        wall_array[-1, :, :3] = 0
        wall_array[:, 0, :3] = 0
        wall_array[:, -1, :3] = 0
        wall_texture = arcade.Texture(name = "wall", image = Image.fromarray(wall_array))
                
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                if self.level[x, y] > 0:
                    wall = arcade.Sprite(texture = wall_texture)
                    wall.center_x = x * TILE_WIDTH + TILE_WIDTH//2
                    wall.center_y = y * TILE_HEIGHT + TILE_HEIGHT//2
                    self.wall_list.append(wall)
                    
        self.world_pixel_height = WORLD_HEIGHT * TILE_HEIGHT
        self.world_pixel_width = WORLD_WIDTH * TILE_WIDTH
        
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