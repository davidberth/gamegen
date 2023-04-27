import arcade
import numpy as np
from params import *
from PIL import Image
from tile import *

class World:
    def __init__(self):
        self.wall_list = None
        self.tile_map = None
        
    def setup(self):
        
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.object_list = arcade.SpriteList(use_spatial_hash=True)
        #self.level = np.random.choice([0,1], size=(WORLD_WIDTH, WORLD_HEIGHT), p=[0.95, 0.05])
        self.level = np.zeros((WORLD_WIDTH, WORLD_HEIGHT), dtype=np.uint8)
        self.fill_walls()
        self.level[2, 7] = 2
        self.level[17, 7] = 3
        
        wall_array = np.zeros((TILE_WIDTH, TILE_HEIGHT, 4), dtype=np.uint8)
        wall_array[:, :, 3] = 255
        wall_array[:, :, :3] = 255
        wall_array[0, :, :3] = 0
        wall_array[-1, :, :3] = 0
        wall_array[:, 0, :3] = 0
        wall_array[:, -1, :3] = 0
        wall_texture = arcade.Texture(name = "wall", image = Image.fromarray(wall_array))
        
        sprite_locations = np.where(self.level > 0)

        for x,y in zip(*sprite_locations):
            tile_type = self.level[x, y]
            tile_sprite = Tile(wall_texture, tile_type)
            tile_sprite.center_x = x * TILE_WIDTH + TILE_WIDTH//2
            tile_sprite.center_y = y * TILE_HEIGHT + TILE_HEIGHT//2
            tile_sprite.color = tiles[tile_type][1]
            tile_sprite.alpha = tiles[tile_type][2]
            if tile_type == 1:
                self.wall_list.append(tile_sprite)
            else:
                self.object_list.append(tile_sprite)
                    
        self.world_pixel_height = WORLD_HEIGHT * TILE_HEIGHT
        self.world_pixel_width = WORLD_WIDTH * TILE_WIDTH
        
    def fill_walls(self):
        self.level[0, :] = 1
        self.level[-1, :] = 1
        self.level[:, 0] = 1
        self.level[:, -1] = 1
        
    def find_starting_position(self):
        starting_position = np.where(self.level == 2)
        if starting_position:
            x, y = (starting_position[0][0] + 0.5) * TILE_WIDTH, (starting_position[1][0] + 0.5) * TILE_HEIGHT
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