import pyglet
from pyglet.gl import *
import numpy as np

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400

window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game Agent')
glClearColor(0.1, 0.1, 0.1, 1.0)

class World:
    def __init__(self, width, height, tile_width, tile_height, margin=1):
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.margin = margin
        self.level = np.random.choice([0, 1], size=(width, height), p=[0.9, 0.1])
        self.level[:, 0] = 1
    
    def generate(self):
        
        marg = self.margin
        tw = self.tile_width
        th = self.tile_height
        quad = np.array([[marg, marg], [marg + tw - 2, marg], [marg + tw - 2, marg + th - 2], [marg, marg + th - 2]])
        walls = np.array(np.where(self.level == 1)).T
        num_walls = walls.shape[0]
        vertices = np.zeros((num_walls, 4, 2), dtype=np.float32)
        walls[:, 0] = walls[:, 0] * tw
        walls[:, 1] = walls[:, 1] * th
        
        for vt in range(4):
            vertices[:, vt, :] = quad[vt, :] + walls
        print (vertices.shape)
        
        colors = np.zeros((num_walls, 4, 3), dtype=np.uint8)
        colors[:, :, :] = 128
        print (colors.shape)
        
        vertices = vertices.flatten()
        colors = colors.flatten()
        
        print (vertices)
        print (colors)
        print (len(vertices))
        print (len(colors))
        
        self.vertex_list = pyglet.graphics.vertex_list(num_walls * 4,
            ('v2f', vertices),
            ('c3B', colors))
        
    def draw(self):
        self.vertex_list.draw(GL_QUADS)        
        
world = World(SCREEN_WIDTH // 20, SCREEN_HEIGHT // 20, 20, 20)
world.generate()
    
@window.event
def on_draw():
    window.clear()
    world.draw()


pyglet.app.run()
