import arcade
from params import *
import numpy as np
from PIL import Image

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None        
        self.level = None
        self.camera = None
        

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        
        self.level = np.random.choice([0,1], size=(WORLD_WIDTH, WORLD_HEIGHT), p=[0.9, 0.1])
        self.level[:, 0] = 1
        
        wall_array = np.zeros((TILE_WIDTH, TILE_HEIGHT, 4), dtype=np.uint8)
        wall_array[:, :, 3] = 255
        wall_array[:, :, :3] = 128
        wall_texture = arcade.Texture(name = "wall", image = Image.fromarray(wall_array))
                
        player_array = np.zeros((28, 28, 4), dtype=np.uint8)
        player_array[:, :, 0] = 255
        player_array[:, :, 3] = 255        
        player_texture = arcade.Texture(name = "player", image = Image.fromarray(player_array))
        
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                if self.level[x, y] > 0:
                    wall = arcade.Sprite(texture = wall_texture)
                    wall.center_x = x * TILE_WIDTH + TILE_WIDTH//2
                    wall.center_y = y * TILE_HEIGHT + TILE_HEIGHT//2
                    self.wall_list.append(wall)
        
        
        self.player_sprite = arcade.Sprite(texture = player_texture)
        self.player_sprite.center_x = SCREEN_WIDTH//2
        self.player_sprite.center_y = SCREEN_HEIGHT//2
        
        self.player_list.append(self.player_sprite)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.wall_list)
        
        self.camera = arcade.Camera(self.width, self.height)
        
    def on_draw(self):
        self.camera.use()
        self.clear()
        self.wall_list.draw()
        self.player_list.draw()
    
    def on_key_press(self, key, modifiers):
    
        if key == arcade.key.UP or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        
                
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
         
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
    
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_player()
                
def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    window.setup()
    arcade.run()
    
if __name__ == "__main__":
    main()