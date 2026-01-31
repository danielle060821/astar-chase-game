import pygame
import json
from a_Star import AStar
from renderer import Renderer
from game_state import Phase, GameState
import os

"""
    Make sure there is a path(goal is not blocked) and the starting point of player is not wall
"""
def check_asserts(ROWS, COLS):
    assert 0 <= start_row < ROWS, "Player starting y invalid"
    assert 0 <= start_col < COLS, "Player starting x invalid"
    assert grid[start_row][start_col] != 1, "Player starting point is wall"
    assert 0 <= goal_row < ROWS, "Goal y invalid"
    assert 0 <= goal_col < COLS, "Goal x invalid"
    assert grid[goal_row][goal_col] != 1, "Goal is wall"
    assert 0 <= astar_srow < ROWS, "Astar Agent starting y invalid"
    assert 0 <= astar_scol < COLS, "Astar Agent starting x invalid"
    assert grid[astar_srow][astar_scol] != 1, "Astar Agent starting point is wall"
    assert path is not None, "No path found"
    
#load level configuration
def load_level(filename):
    with open(filename) as f:
        level = json.load(f)
    return level

level_data = load_level("Maps/level1.json")

clock = pygame.time.Clock()

#background music
pygame.mixer.pre_init(44100, -16, 2, 2048)  # 44.1kHz, 16-bit, stereo, buffer 512
pygame.init()
pygame.mixer.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.music.load(os.path.join(BASE_DIR, level_data["music"]))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


"""
    Initialize
"""
grid = level_data["grid"]
renderer = Renderer()
ROWS, COLS = renderer.ROWS, renderer.COLS

#set caption for the current level 
#set "Space Game" as caption when level name is not found, avoid unexpected behaviour 
level_name = level_data.get("level_name", "Space Game")
renderer.set_caption(level_name) 
    
#player    
start = tuple(level_data["player_start"])
player_pos = start

#goal
goal = tuple(level_data["goal"])
goal_row, goal_col = goal

#astar agent
astar_agent = AStar()
astar_start = tuple(level_data["astar_start"])
astar_pos = astar_start
cur_pos = astar_pos
steps = 0

INITIAL_COUNTDOWN_MS = 3000
init_buffer_time = 4000
start_time = pygame.time.get_ticks()
over_text = None
over_color = None

PLAYER_COOLDOWN_MS = 300
AGENT_COOLDOWN_MS = 290
player_last_move = 0
astar_agent_last_move = 0

#get path
path = astar_agent.get_shortest_path(grid, start, goal)


start_row, start_col = start
astar_srow, astar_scol = astar_start

check_asserts(ROWS, COLS)

""" 
    Player is manual
""" 
def player_action(player_pos, player_last_move):
    
    #player can only move 1 step per PLAYER_COOLDOWN_MS // 1000 s
    now = pygame.time.get_ticks()  
    if now - player_last_move <= PLAYER_COOLDOWN_MS:
           return player_pos, player_last_move
       
    #Player controlling keys
    keys = pygame.key.get_pressed()
    r, c = player_pos
    new_r, new_c = r, c
    if keys[pygame.K_w]:
            new_r -= 1
    elif keys[pygame.K_s]:
            new_r += 1
    elif keys[pygame.K_a]:
            new_c -= 1
    elif keys[pygame.K_d]:
            new_c += 1
    else:
        #stay(did not press any key)
        return player_pos, player_last_move
            
    #if not wall, can go through
    if 0 <= new_r < ROWS and 0 <= new_c < COLS:
        if grid[new_r][new_c] == 0:
            #move
            return(new_r, new_c), now
    #at wall or grid boundary(can't move)       
    return player_pos, player_last_move

"""
    Astar agent
"""
def astar_agent_action(astar_pos, player_pos, steps,astar_agent_last_move):
    #Astar agent can only move 1 step per AGENT_COOLDOWN_MS // 1000s
    now = pygame.time.get_ticks()
    if now - astar_agent_last_move <= AGENT_COOLDOWN_MS:
        return astar_pos, steps, astar_agent_last_move
    
    astar_path = astar_agent.get_shortest_path(grid, astar_pos, player_pos)
    #only walk one step at a time(0 is start, 1 is the next step because i wrote came_from = {Start: None})
    #steps that have been used
    #if agent is only 1 step away from player or already chased player(or is path does not exist)
    if not astar_path or len(astar_path) < 2:
        return astar_pos, steps, astar_agent_last_move     
    if astar_path[1] != astar_pos:
        steps += 1
        astar_pos = astar_path[1]
    return astar_pos, steps, now

"""
    Game Rule
"""
def astar_caught_player(player_pos, astar_pos) -> bool:
    if astar_pos == player_pos and player_pos != goal:
        return True
    return False
 
def player_wins(player_pos, astar_pos) -> bool:
    if player_pos == goal and astar_pos != player_pos:
        return True
    return False
                      
"""
    Game loop
""" 
state = GameState()
state.set_phase(Phase.COUNTDOWN)
while state.running:
    #60 frames/s
    clock.tick(60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
               
    #cover the previous step
    renderer.draw_background() 
    
    #display steps    
    renderer.display_steps(steps)
    
    #buffer time(4s)before game starts 
    if state.phase == Phase.COUNTDOWN:
        renderer.draw_static_world(grid, goal_row, goal_col)
        renderer.draw_player(start_row, start_col)
        renderer.draw_astar_agent(astar_srow, astar_scol)
        now = pygame.time.get_ticks()
        elapsed = now - state.phase_start_time
        if elapsed < INITIAL_COUNTDOWN_MS:
            #count down: 3 -> 2 -> 1
            remaining = (INITIAL_COUNTDOWN_MS - elapsed + 999) // 1000
            renderer.set_countdown(remaining)
        elif elapsed < init_buffer_time:
            renderer.game_start_text()
        else:
            state.set_phase(Phase.PLAYING)
            
    
    elif state.phase == Phase.PLAYING:
        renderer.draw_static_world(grid, goal_row, goal_col)
            
        #draw player
        player_pos, player_last_move = player_action(player_pos, player_last_move)
        player_row, player_col = player_pos
        renderer.draw_player(player_row, player_col)
            
        #draw astar agent
        astar_pos, steps, astar_agent_last_move = astar_agent_action(astar_pos, player_pos, steps, astar_agent_last_move)
        astar_row, astar_col = astar_pos
        renderer.draw_astar_agent(astar_row, astar_col)
        
        #astar agent wins(player lost)
        if astar_caught_player(player_pos, astar_pos):
            state.set_phase(Phase.FINISHED)
            finish_time = pygame.time.get_ticks()
            over_text = "You Lost!"
            over_color = (255, 0, 0)
            
        #player wins
        elif player_wins(player_pos, astar_pos):
            state.set_phase(Phase.FINISHED)
            finish_time = pygame.time.get_ticks()
            over_text = "You Win!"
            over_color = (23, 199, 29)
    
    #delay 3 seconds after finish
    elif state.phase == Phase.FINISHED:
        renderer.draw_static_world(grid, goal_row, goal_col)
        #redraw player to prevent being covered by goal
        renderer.draw_player(player_row, player_col)
        renderer.draw_astar_agent(astar_row, astar_col)
        renderer.over_text(over_text, over_color)
        
        elapsed = pygame.time.get_ticks() - state.phase_start_time
        if elapsed > 3000:
            state.running = False
        
    pygame.display.flip()

pygame.quit()