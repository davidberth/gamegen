import pyglet
import numpy as np

class Level:
    tilemap: np.ndarray
    sizex: int
    sizey: int
        
    def load(self, filename: str):
        # load a text file into a 2D numpy array
        with open(filename) as f:
            lines = f.readlines()
        self.sizex = len(lines[0].strip())
        self.sizey = len(lines)
        self.tilemap = np.zeros((self.sizex, self.sizey), dtype=int)
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
                self.tilemap[x, y] = int(c)
    
    def print(self):
        for y in range(self.sizey):
            for x in range(self.sizex):
                print(self.tilemap[x, y], end='')
            print()
    
    
if __name__=='__main__':
    level = Level()
    level.load('worlds/map.txt')
    level.print()
    

    
    