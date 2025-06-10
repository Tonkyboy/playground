import pygame
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Define game objects and variables
FPS = 60
bird = pygame.Rect(100, 200, 20, 20)  # x, y, width, height
bird_vel = 0
pipes = []
score = 0
font = pygame.font.Font(None, 36)

# Function to reset the game state
def reset_game():
    global bird, bird_vel, pipes, score
    bird.topleft = (100, 200)  # Reset bird position
    bird_vel = 0              # Reset bird velocity
    pipes.clear()             # Clear all pipes
    score = 0                 # Reset score

# Initial game setup
reset_game()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_vel = -5  # Make the bird 'flap' upwards

    # Update bird physics (gravity)
    bird_vel += 0.2
    bird.y += bird_vel

    # Pipe generation
    # Create new pipes if none exist or the last pipe is far enough away
    if len(pipes) == 0 or pipes[-1].x < 250: # Adjusted spacing for new pipes
        gap_y = random.randrange(80, 300) # Random Y position for the gap
        pipe_width = 50
        pipe_gap_height = 150 # Size of the gap

        # Top pipe
        pipes.append(pygame.Rect(400, 0, pipe_width, gap_y - pipe_gap_height // 2))
        # Bottom pipe
        pipes.append(pygame.Rect(400, gap_y + pipe_gap_height // 2, pipe_width, 400 - (gap_y + pipe_gap_height // 2)))

    # Move pipes and handle scoring/removal
    for pipe in pipes[:]: # Iterate over a copy to allow safe removal
        pipe.x -= 2 # Move pipe to the left

        # Remove pipes that have moved off-screen
        if pipe.x < -pipe.width:
            pipes.remove(pipe)
        
        # Scoring: Check if the bird has passed this pipe (only count once per pipe pair)
        # We check for a pipe that's at the bird's x-coordinate, and also ensure it's
        # the upper part of a pipe (height > 0, not a small invisible segment)
        # A more robust scoring system might use a boolean flag on pipe objects.
        if pipe.x == bird.x and pipe.height > 0 and pipe.y < 200: # Arbitrary check for upper pipe part
             score += 1 # Increment score when bird passes the x-coordinate

    # Collision detection
    # Check for collision with any pipe
    for pipe in pipes:
        if bird.colliderect(pipe):
            reset_game()
            # If you want the game to completely end on collision, uncomment `running = False`
            # running = False
            # break # Exit pipe loop if collision detected
    
    # Check for collision with top or bottom screen boundaries
    if bird.top < 0 or bird.bottom > 400:
        reset_game()
        # If you want the game to completely end on collision, uncomment `running = False`
        # running = False


    # Drawing
    screen.fill((0, 0, 0)) # Black background
    pygame.draw.rect(screen, (255, 0, 0), bird) # Draw red bird
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), pipe) # Draw green pipes

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255)) # White text
    screen.blit(score_text, (10, 10)) # Position score

    # Update the full display surface to the screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
