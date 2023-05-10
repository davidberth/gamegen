import arcade
import game
from params import *
import time
         
def main():
    width = min(MAX_SCREEN_WIDTH, WORLD_WIDTH * TILE_WIDTH)
    height = min(MAX_SCREEN_HEIGHT, WORLD_HEIGHT * TILE_HEIGHT + GUI_HEIGHT) 
    #window = arcade.Window(width, height, WINDOW_TITLE, fullscreen=FULLSCREEN, vsync=True, center_window=True)
    main_game = game.Game(width, height, WINDOW_TITLE, "nn", "human", fullscreen=FULLSCREEN, vsync=True, center_window=True)
    main_game.reset() 

    
    # Custom game loop
    last_update_time = time.time()
    frame = 0
    while frame < 15000:
      
        current_time = time.time()
        delta_time = current_time - last_update_time
        main_game.dispatch_events()        
        main_game.on_update(delta_time)
        if frame % 50 == 0:
            main_game.on_draw()
            main_game.flip()
        last_update_time = current_time
     
        #time.sleep(1/60)  # Sleep for 1/60 seconds to limit the frame rate to 60 FPS
        frame+=1


    
if __name__ == "__main__":
    main()