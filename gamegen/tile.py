import arcade

tiles = [ 
['empty', arcade.color.BLACK, 255],
['wall', arcade.color.GRAY, 255],
['start', arcade.color.BLUE, 190],
['goal', arcade.color.GREEN, 190]
]
    
class Tile(arcade.Sprite):
    def __init__(self, texture, tile_type):
        super().__init__(texture=texture)
        self.tile_type = tile_type

