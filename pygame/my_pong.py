# Simple Pong Game in Python
import pygame
import math
import random

# Constants
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paddles
LEFT_PADDLE_X = 50
LEFT_PADDLE_Y = 250
RIGHT_PADDLE_X = 730
RIGHT_PADDLE_Y = 250
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball
BALL_INIT_X = 390
BALL_INIT_Y = 290
BALL_RESET_X = 400
BALL_RESET_Y = 300
BALL_SIZE = 20
BALL_BASE_SPEED = 5
BALL_ANGLE_MIN = -math.pi / 4  # -45 degrees
BALL_ANGLE_MAX = math.pi / 4   # +45 degrees
BALL_SPEED_MULTIPLIER = 1.1

# Score display
FONT_SIZE = 36
SCORE_TEXT_X = 380
SCORE_TEXT_Y = 10

# Colors
COLOR_BLACK = (0, 0, 0)      # Background
COLOR_GREEN = (0, 255, 0)    # Paddles
COLOR_RED = (255, 0, 0)      # Ball
COLOR_WHITE = (255, 255, 255)  # Score text

# Frame rate
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Define paddles (left and right)
left_paddle = pygame.Rect(LEFT_PADDLE_X, LEFT_PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(RIGHT_PADDLE_X, RIGHT_PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

# Define ball
ball = pygame.Rect(BALL_INIT_X, BALL_INIT_Y, BALL_SIZE, BALL_SIZE)
ball_speed = [0, 0]  # [x speed, y speed]

# Score
score = [0, 0]  # [left player, right player]
font = pygame.font.Font(None, FONT_SIZE)

# Function to reset the ball
def reset_ball():
    ball.center = (BALL_RESET_X, BALL_RESET_Y)
    angle = random.uniform(BALL_ANGLE_MIN, BALL_ANGLE_MAX)
    direction = random.choice([-1, 1])
    ball_speed[0] = direction * BALL_BASE_SPEED * math.cos(angle)
    ball_speed[1] = BALL_BASE_SPEED * math.sin(angle)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    # Left paddle (Player 1: W and S)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.y += PADDLE_SPEED
    # Right paddle (Player 2: Arrow keys)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Start ball if stationary
    if ball_speed == [0, 0]:
        reset_ball()

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Bounce off top and bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Bounce off paddles and increase speed
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0] * BALL_SPEED_MULTIPLIER
        ball_speed[1] *= BALL_SPEED_MULTIPLIER

    # Score points and reset ball
    if ball.left <= 0:
        score[1] += 1  # Right player scores
        reset_ball()
    if ball.right >= SCREEN_WIDTH:
        score[0] += 1  # Left player scores
        reset_ball()

    # Draw everything
    screen.fill(COLOR_BLACK)
    pygame.draw.rect(screen, COLOR_GREEN, left_paddle)
    pygame.draw.rect(screen, COLOR_GREEN, right_paddle)
    pygame.draw.ellipse(screen, COLOR_RED, ball)
    score_text = font.render(f"{score[0]} - {score[1]}", True, COLOR_WHITE)
    screen.blit(score_text, (SCORE_TEXT_X, SCORE_TEXT_Y))
    pygame.display.flip()

    # Cap frame rate
    clock.tick(FPS)

pygame.quit()
