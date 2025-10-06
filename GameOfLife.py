import numpy as np
import tkinter as tk
import time



class GameOfLife:

    def __init__(self):
        self.GRID_SIZE = 100
        self.PAUSE_TIME = 200
        self.MainGrid = np.zeros((self.GRID_SIZE,self.GRID_SIZE))
        self.isPaused = True                
        self.MainGrid[50][50] = 1
        self.Root = tk.Tk()

        # canvas
        self.canvas = tk.Canvas(self.Root, height=self.GRID_SIZE*10, width=self.GRID_SIZE*10, bg="black")
        self.canvas.pack()  
        self.canvas.bind("<Button-1>", self.OnClick)

        # pause/play button
        self.btn = tk.Button(self.Root, text="play", command=self.SwapPause)
        self.btn.pack()
        
        self.RenderGrid()
        self.Root.after(self.PAUSE_TIME, self.GridUpdate)
        self.Root.mainloop()


    def OnClick(self, event):
        x = int(event.x/10)
        y = int(event.y/10)
        self.MainGrid[x][y] = 1
        self.Root.after(100, self.RenderGrid)
        
        
    # go through every cell and check it against the rules
    def GridUpdate(self):
        if self.isPaused:
            return
        temp_array = self.MainGrid.copy()
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                temp_array[i][j] = self.CheckRules(i, j)
        self.MainGrid = temp_array
        self.RenderGrid()
        self.Root.after(self.PAUSE_TIME, self.GridUpdate)

    # Rule 1: Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
    # Rule 2: Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
    # Rule 3: Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
    # Rule 4: Any dead cell with exactly 3 live neighbors becomes alive, by reproduction
    
    # Each rule will return true if it's passed, false if it's failed.

    def CheckRules(self, x_pos:int, y_pos:int):
        num_neighbors = 0
        for i in range(x_pos-1, x_pos+2):
            for j in range(y_pos-1, y_pos+2):
                # avoid breaking out of grid:
                if i >= self.GRID_SIZE or j >= self.GRID_SIZE or i < 0 or j < 0:
                    continue
                # avoid self
                if (i == x_pos and j == y_pos):
                    continue
                # record # of neighbors
                if self.MainGrid[i][j] == 1:
                    num_neighbors += 1
        # DEAD check if revived:
        if self.MainGrid[x_pos][y_pos] == 0 and num_neighbors == 3:
            return 1
        if self.MainGrid[x_pos][y_pos] == 0:
            return 0
        
        # ALIVE check against rules based on # of neighbors:
        if num_neighbors <= 1:
            return 0
        elif num_neighbors <= 3 and num_neighbors >= 2:
            return 1
        else:
            return 0
        
    # draw the grid based on 0's and 1's
    def RenderGrid(self):
        self.canvas.delete("all")
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.MainGrid[i][j] == 1:
                    self.canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="white")

    def SwapPause(self):
        self.isPaused = not self.isPaused
        if not self.isPaused:
            self.btn.config(text="pause")
        else:
            self.btn.config(text="play")
            
        self.GridUpdate()
        
# start 
GOL = GameOfLife()
