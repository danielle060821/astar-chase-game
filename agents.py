from a_Star import AStar

"""
    Astar agent
"""
class AStarAgent:
    def __init__(self, start_pos):
        self.pos = tuple(start_pos)
        self.steps = 0
        self.ASTAR_COOLDOWN_MS = 330
        self.last_move = 0
        self.astar_agent = AStar()
             
    def update(self, grid, player_pos, now):
        #Astar agent can only move 1 step per AGENT_COOLDOWN_MS // 1000s
        if now - self.last_move <= self.ASTAR_COOLDOWN_MS:
            return self.pos, self.steps, self.last_move
        else:
            #cooldown over, reset last_move(time)
            self.last_move = now
            
        path = self.astar_agent.get_shortest_path(grid, self.pos, player_pos)
        #only walk one step at a time(0 is start, 1 is the next step because i wrote came_from = {Start: None} in a_Star.py)
        #steps that have been used
        #if agent is only 1 step away from player or already chased player(or path does not exist)
        if not path or len(path) < 2:
            return self.pos, self.steps, self.last_move     
        if path[1] != self.pos:
            self.steps += 1
            self.pos = path[1]
        return self.pos, self.steps, now
    
    def reset(self):
        self.pos = self.start_pos
        self.step = 0
        self.last_move = 0