import arcade
import main_view
from params import *

         
def main():
    width = min(MAX_SCREEN_WIDTH, WORLD_WIDTH * TILE_WIDTH)
    height = min(MAX_SCREEN_HEIGHT, WORLD_HEIGHT * TILE_HEIGHT + GUI_HEIGHT) 
    window = arcade.Window(width, height, WINDOW_TITLE, fullscreen=FULLSCREEN, vsync=True, center_window=True)
    main = main_view.MainView()
    main.reset()
    window.show_view(main)
    window.run()
    
if __name__ == "__main__":
    main()