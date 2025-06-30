# Simple Falling Objects Game in Python
# @CodingTogether
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

basket_width = 100
basket = pygame.Rect(150, 380, basket_width, 10)
objects = []
score = 0
lives = 3
font = pygame.font.Font(None, 36)

def reset_game():
    global basket, objects, score, lives, basket_width
    basket_width = 100
    basket = pygame.Rect(150, 380, basket_width, 10)
    objects = []
    score = 0
    lives = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.left > 0:
        basket.x -= 8
    if keys[pygame.K_RIGHT] and basket.right < 400:
        basket.x += 8
    
    if random.random() < 0.02:
        objects.append(pygame.Rect(random.randint(0, 380), 0, 20, 20))
    
    for obj in objects[:]:
        obj.y += 2 
        if obj.colliderect(basket):
            score += 1
            objects.remove(obj)
            if score % 5 == 0:
                basket_width = max(50, basket_width - 10)
                basket.width = basket_width
                basket.x = min(basket.x, 400 - basket_width)
        elif obj.top > 400:
            objects.remove(obj)
            lives -= 1

    if lives <= 0:
        reset_game()
      
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), basket)
    for obj in objects:
        pygame.draw.rect(screen, (255, 0, 0), obj)
    score_lives_text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255, 255))
    screen.blit(score_lives_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
