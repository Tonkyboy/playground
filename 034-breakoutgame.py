
# Simple Breakout Game Python
import pygame
import math

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

ball = pygame.Rect(200, 200, 20, 20)
angle = math.radians(75)
ball_speed = [0, 0] 

paddle = pygame.Rect(180, 380, 60, 10)
paddle_speed = 5

score = 0
font = pygame.font.Font(None, 36)

def reset_game():
    global ball, ball_speed, paddle, score
    ball = pygame.Rect(200, 200, 20, 20)
    ball_speed = [0, 0]  
    paddle = pygame.Rect(180, 380, 60, 10)
    score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ball_speed == [0, 0]:
        ball_speed = [3 * math.cos(angle), 
        3 * math.sin(angle)]

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 5:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < 395:
        paddle.x += paddle_speed

    # Move the ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left < 0 or ball.right > 400:
        ball_speed[0] = -ball_speed[0]
    if ball.top < 0:
        ball_speed[1] = -ball_speed[1]
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        score += 1
        # Increase ball speed by 10%
        ball_speed[0] *= 1.1
        ball_speed[1] *= 1.1
        
        paddle.width = max(20, paddle.width - 5)
        paddle.x += (paddle.width - paddle.width) / 2  
    if ball.bottom > 400:
        reset_game()

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.ellipse(screen, (255, 0, 0), ball)
    pygame.draw.rect(screen, (0, 255, 0), paddle)
    score_text = font.render(f"Score: {score}", 
                             True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
