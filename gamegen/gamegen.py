import pyglet
from pyglet.gl import *
import numpy as np
from params import *
from pyglet.window import key


window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game Agent')
glClearColor(0.1, 0.1, 0.1, 1.0)

wall_def_vert = np.array([[0.05, 0.05], [0.95, 0.05], [0.95, 0.95], [0.05, 0.95]])
wall_def_color = np.ones((4, 3), dtype=np.uint8) * 128



class World:
    def __init__(self, width, height, tile_width, tile_height, margin=1):
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.margin = margin
        self.level = np.random.choice([0, 1], size=(width, height), p=[0.4, 0.6])
        
        self.camera_x = 0
        self.camera_y = 0
    
    def update(self):
        
        sx = self.camera_x
        sy = self.camera_y
        ex = self.camera_x + SCREEN_WIDTH
        ey = self.camera_y + SCREEN_WIDTH
        
        minx = max(sx // self.tile_width, 0)
        maxx = ex // self.tile_width + 1
        miny = max(sy // self.tile_height, 0)
        maxy = ey // self.tile_height + 1
        
        tw = self.tile_width
        th = self.tile_height
        quad = wall_def_vert.copy()
        quad[:, 0] = quad[:, 0] * tw
        quad[:, 1] = quad[:, 1] * th
    
        viewable = self.level[minx:maxx, miny:maxy]
        walls = np.array(np.where(viewable > 0)).T + [minx, miny]
        num_walls = walls.shape[0]
        vertices = np.zeros((num_walls, 4, 2), dtype=np.float32)
        walls[:, 0] = walls[:, 0] * tw - self.camera_x
        walls[:, 1] = walls[:, 1] * th - self.camera_y
        
        for vt in range(4):
            vertices[:, vt, :] = quad[vt, :] + walls

        colors = np.zeros((num_walls, 4, 3), dtype=np.uint8)
        colors[:, :, :] = 128

        vertices = vertices.flatten()
        colors = colors.flatten()

        self.vertex_list = pyglet.graphics.vertex_list(num_walls * 4,
            ('v2f', vertices),
            ('c3B', colors))
        
    def draw(self):
        self.vertex_list.draw(GL_QUADS)        
        
world = World(500, 500, TILE_WIDTH, TILE_HEIGHT)
fps_display = pyglet.window.FPSDisplay(window=window)
keys = key.KeyStateHandler()
window.push_handlers(keys)

def move_camera(dt):
    
    if keys[key.LEFT]:
        world.camera_x -= 4
    if keys[key.RIGHT]:
        world.camera_x += 4
    if keys[key.UP]:
        world.camera_y += 4
    if keys[key.DOWN]:
        world.camera_y -= 4
    
    world.update()


pyglet.clock.schedule(move_camera)
world.update()
@window.event
def on_draw():

    window.clear()
    world.draw()
    fps_display.draw()


pyglet.app.run()
