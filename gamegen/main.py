import arcade
import game
import info_bar as info_bar
from params import *

class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.game = game.Game(0, 0, self.window.width, self.window.height - GUI_HEIGHT)
        self.info_bar = info_bar.InfoBar(0, self.window.height - GUI_HEIGHT, self.window.width, GUI_HEIGHT)
        
        self.section_manager.add_section(self.game)
        self.section_manager.add_section(self.info_bar)
        
    def setup(self):
        self.game.setup()
                            
    def on_draw(self):
        arcade.start_render()
        
    def on_update(self, delta_time: float):
        self.info_bar.score = self.game.score

         
def main():
    width = min(MAX_SCREEN_WIDTH, WORLD_WIDTH * TILE_WIDTH)
    height = min(MAX_SCREEN_HEIGHT, WORLD_HEIGHT * TILE_HEIGHT + GUI_HEIGHT) 
    window = arcade.Window(width, height, WINDOW_TITLE, fullscreen=False, vsync=True, center_window=True)
    main_view = MainView()
    main_view.setup()
    window.show_view(main_view)
    window.run()
    
if __name__ == "__main__":
    main()