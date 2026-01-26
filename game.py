import pygame
from a_Star import AStar
from Maps.grid_level1 import grid

#import os
#print(os.listdir("images"))

CELL = 50
ROWS, COLS = 15, 15
WIDTH, HEIGHT = ROWS * CELL, COLS * CELL
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first grid game")
clock = pygame.time.Clock()

#background
screen.fill((20,20,20))

#background music
pygame.mixer.pre_init(44100, -16, 2, 2048)  # 44.1kHz, 16-bit, stereo, buffer 512
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/Space_Game_Music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

font = pygame.font.SysFont(None, 60)
"""
    Initialize
"""
#player
ship_img = pygame.image.load("assets/images/Space_Ship(Player).png").convert_alpha()
ship_img = pygame.transform.scale(ship_img, (CELL, CELL))
start = (1, 1)
player_pos = start

#goal
goal = (14, 14)
goal_row, goal_col = goal
flag_img = pygame.image.load("assets/images/Flag(Goal).png").convert_alpha()
flag_img = pygame.transform.scale(flag_img, (CELL, CELL))

#astar agent
alien_img = pygame.image.load("assets/images/Alien(AStar_Agent).png").convert_alpha()
alien_img = pygame.transform.scale(alien_img, (CELL, CELL))
astar_agent = AStar()
astar_start = (5, 5)
astar_pos = astar_start
cur_pos = astar_pos
steps = 0

running = True
INITIAL_COUNTDOWN_MS = 3000
init_buffer_time = 4000
buffer_done = False
finished = False
finish_time = None
start_time = pygame.time.get_ticks()
over_text = None

PLAYER_COOLDOWN_MS = 300
AGENT_COOLDOWN_MS = 290
player_last_move = 0
astar_agent_last_move = 0

#get path
path = astar_agent.get_shortest_path(grid, start, goal)

"""
    Make sure there is a path(goal is not blocked) and the starting point of player is not wall
"""
start_row, start_col = start
astar_srow, astar_scol = astar_start
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

#draw goal and grid(draw goal after girid, or will be covered)
def draw_static_world() -> None:
    #draw grid
    for r in range(ROWS):
            for c in range(COLS):
                color = (23, 16, 43) if grid[r][c] == 1 else (217, 211, 253)
                pygame.draw.rect(
                    screen,
                    color,
                    (CELL * c, CELL * r, CELL, CELL),
                    0
                )                   
    #draw goal(grids have length!!)(be careful -- x, y and row, col are opposite)
    gx = goal_col * CELL + CELL // 2
    gy = goal_row * CELL + CELL // 2
    rect = flag_img.get_rect(center = (gx, gy))
    screen.blit(flag_img, rect)
            
#draw player(put player in the middle of a grid)
def draw_player(player_row, player_col) -> None:
    px = player_col * CELL + CELL // 2 
    py = player_row * CELL + CELL // 2 
    #center
    rect = ship_img.get_rect(center = (px, py))
    screen.blit(ship_img, rect)
    
#draw A* agent
def draw_astar_agent(astar_row, astar_col) -> None:
    astar_x = astar_col * CELL + CELL // 2 
    astar_y = astar_row * CELL + CELL // 2 
    rect = alien_img.get_rect(center = (astar_x, astar_y))
    screen.blit(alien_img, rect)

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
     
while(running):
    #60 frames/s
    clock.tick(60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #cover the previous step
    screen.fill((20, 20, 20)) 
    
    #buffer time(4s)before game starts 
    if not buffer_done:
        draw_static_world()
        draw_player(start_row, start_col)
        draw_astar_agent(astar_srow, astar_scol)
        
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        if elapsed < INITIAL_COUNTDOWN_MS:
            #count down: 3 -> 2 -> 1
            remaining = (INITIAL_COUNTDOWN_MS - elapsed + 999) // 1000
            wait_text = font.render(f"Get Ready... {remaining}", True, (226, 83, 0))
            screen.blit(wait_text, ((WIDTH // 2 - 80), HEIGHT // 2 - 40))
        elif elapsed < init_buffer_time:
            wait_text = font.render("GO!", True, (226, 83, 0))
            screen.blit(wait_text, ((WIDTH // 2 - 80), HEIGHT // 2 - 40))
        if(now - start_time > init_buffer_time):
            buffer_done = True
    
    else:
        draw_static_world()
        
        #only display motion when the game is not finished
        if not finished:      
            #draw player
            player_pos, player_last_move = player_action(player_pos, player_last_move)
            player_row, player_col = player_pos
            draw_player(player_row, player_col)
            
            #draw astar agent
            astar_pos, steps, astar_agent_last_move = astar_agent_action(astar_pos, player_pos, steps, astar_agent_last_move)
            astar_row, astar_col = astar_pos
            draw_astar_agent(astar_row, astar_col)
        
        #astar agent wins
        if astar_caught_player(player_pos, astar_pos):
            finished = True
            finish_time = pygame.time.get_ticks()
            over_text = font.render(f"You Lost!", True, (255, 0, 0))
            rect = over_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
            screen.blit(over_text, rect)
            
        #player wins
        elif player_wins(player_pos, astar_pos):
            finished = True
            finish_time = pygame.time.get_ticks()
            over_text = font.render(f"You Won!", True, (23, 199, 29))
            rect = over_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
            screen.blit(over_text, rect)
        
    #display steps    
    step_text = font.render(f"Alien Steps: {steps}", True, (47, 1, 108))
    screen.blit(step_text, (10, 10))
    
    #delay 3 seconds after finish
    if finished:
        #redraw player to prevent being covered by goal
        draw_player(player_row, player_col)
        draw_astar_agent(astar_row, astar_col)
        rect = over_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, rect)
        
        elapsed = pygame.time.get_ticks() - finish_time
        if elapsed > 3000:
            running = False
        
    pygame.display.flip()

pygame.quit()