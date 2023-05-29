import arcade

tiles = [ 
['empty', arcade.color.BLACK, 255],
['wall', arcade.color.GRAY, 255],
['start', arcade.color.BLUE, 190],
['goal', arcade.color.GREEN, 190],
['coin', arcade.color.GOLD, 110],
]
    
class Tile(arcade.SpriteSolidColor):
    def __init__(self, x, y, width, height, margin, tile_type):
        color = tiles[tile_type][1]
        sprite_width = width - margin * 2
        sprite_height = height - margin * 2
        super().__init__(sprite_width, sprite_height, color)
        self.alpha = tiles[tile_type][2]
        self.center_x = x * sprite_width + sprite_width // 2
        self.center_y = y * sprite_width + sprite_height // 2
        self.tile_type = tile_type
        self.level_x = x
        self.level_y = y
        
        

