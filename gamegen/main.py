import arcade
import game
from params import *

         
def main():
    width = min(MAX_SCREEN_WIDTH, WORLD_WIDTH * TILE_WIDTH)
    height = min(MAX_SCREEN_HEIGHT, WORLD_HEIGHT * TILE_HEIGHT + GUI_HEIGHT) 
    window = arcade.Window(width, height, WINDOW_TITLE, fullscreen=FULLSCREEN, vsync=True, center_window=True)
    main_game = game.Game()
    main_game.reset()
    window.show_view(main_game)
    window.run()
    
if __name__ == "__main__":
    main()