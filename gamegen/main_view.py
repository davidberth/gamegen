import arcade
import game
import info_bar
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
        self.game.score = 0
                            
    def on_draw(self):
        arcade.start_render()
        
    def on_update(self, delta_time: float):
        self.info_bar.score = int(self.game.score)
        if self.game.goal_reached:
            self.info_bar.previous_score = int(self.game.score)
            if self.info_bar.max_score < self.game.score:
                self.info_bar.max_score = int(self.game.score)
            self.game.goal_reached = False  
            self.setup()
        