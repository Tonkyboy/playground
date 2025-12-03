import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 450 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pac-Man")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

TILE_SIZE = 30
ROWS = len(maze)
COLS = len(maze[0])

player_x, player_y = 1, 1
player_dir = (0, 0)
next_dir = (0, 0) 

ghosts = [[18, 1], [18, 11], [1, 11]] 
ghost_dirs = [(0, 1), (0, -1), (1, 0)] 

score = 0
font = pygame.font.Font(None, 36)
game_over = False
won = False

def can_move(x, y):
    if 0 <= x < COLS and 0 <= y < ROWS:
        return maze[y][x] != 1
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                next_dir = (1, 0)
            elif event.key == pygame.K_UP:
                next_dir = (0, -1)
            elif event.key == pygame.K_DOWN:
                next_dir = (0, 1)
            elif event.key == pygame.K_r and (game_over or won):
                running = False 

    if not game_over and not won:
        if can_move(player_x + next_dir[0], player_y + next_dir[1]):
            player_dir = next_dir
        
        new_x = player_x + player_dir[0]
        new_y = player_y + player_dir[1]

        if can_move(new_x, new_y):
            player_x, player_y = new_x, new_y

        if maze[player_y][player_x] == 0:
            maze[player_y][player_x] = 2
            score += 10

        pellets_left = sum(row.count(0) for row in maze)
        if pellets_left == 0:
            won = True

        for i in range(len(ghosts)):
            gx, gy = ghosts[i]
            dx, dy = ghost_dirs[i]
            
            next_gx, next_gy = gx + dx, gy + dy

            if not can_move(next_gx, next_gy):
                possible_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(possible_dirs)
                for pdx, pdy in possible_dirs:
                    if can_move(gx + pdx, gy + pdy):
                        ghost_dirs[i] = (pdx, pdy)
                        break
            else:
                if random.random() < 0.1: 
                     possible_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                     valid_dirs = []
                     for pdx, pdy in possible_dirs:
                         if can_move(gx + pdx, gy + pdy):
                             valid_dirs.append((pdx, pdy))
                     ghost_dirs[i] = random.choice(valid_dirs)
                
                ghosts[i][0] += ghost_dirs[i][0]
                ghosts[i][1] += ghost_dirs[i][1]

            if player_x == ghosts[i][0] and player_y == ghosts[i][1]:
                game_over = True

    screen.fill(BLACK)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 0:
                pygame.draw.circle(screen, YELLOW, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 4)

    pygame.draw.circle(screen, YELLOW, (player_x*TILE_SIZE + TILE_SIZE//2, player_y*TILE_SIZE + TILE_SIZE//2), 12)

    for gx, gy in ghosts:
        pygame.draw.circle(screen, RED, (gx*TILE_SIZE + TILE_SIZE//2, gy*TILE_SIZE + TILE_SIZE//2), 12)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))

    if game_over:
        msg = font.render("GAME OVER!", True, RED)
        screen.blit(msg, (WIDTH//2 - 80, HEIGHT//2))
    elif won:
        msg = font.render("YOU WIN!", True, YELLOW)
        screen.blit(msg, (WIDTH//2 - 70, HEIGHT//2))
    pygame.display.flip()
    clock.tick(8) 

pygame.quit()