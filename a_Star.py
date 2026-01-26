"""
1. heuristic(manhattan)
2. f = g + h
3. a star: open set(heapq get smallest f) -> need: start, goal, grid
           closed set
"""
import heapq 

class AStar: 
    def __init__(self):
        #             up    down   left  right
        self.direction = [(0,1),(0,-1),(-1,0),(1,0)]
    
    #manhattan distance. Pure math equation, isolated.
    @staticmethod
    def heuristic(a,b):
        return abs(a[0]-b[0])+abs(a[1]-b[1])
    
    def get_neighbour(self, pos, grid):
        #valid? is wall?
        neighbour = []
        pos_x = pos[0]
        pos_y = pos[1]
        for dir in self.direction:
           dir_x = dir[0]
           dir_y = dir[1]
           new_x = pos_x + dir_x
           new_y = pos_y + dir_y
           if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == 0:
               neighbour.append((new_x,new_y))
        return neighbour           
        
    def get_shortest_path(self, grid, start, goal):
        
        #initialize
        #open_set: f_score, current position
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        closed_set = set()
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            neighbours = self.get_neighbour(current, grid)
            for nb in neighbours:
                #prevent repeat
                if nb in closed_set:
                    continue
                closed_set.add(current)
                
                tentative_gscore = g_score[current] + 1
                if nb not in g_score or tentative_gscore < g_score[nb]:
                    g_score[nb] = tentative_gscore
                    f_score = tentative_gscore + self.heuristic(nb, goal)
                    came_from[nb] = current
                    heapq.heappush(open_set,(f_score, nb))
            
            
            if current == goal:
                path = []
                #need to be not none because dont want to include starting point
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]
    
        
                
        
        
        
       
            
        
        
            
            
                
            
        