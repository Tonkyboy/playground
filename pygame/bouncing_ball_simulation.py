# Bouncing Ball Simulation Python
# @Cod1ngTogether
import pygame
import random

pygame.init()
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

num_balls = 10
balls = [
    {
        'x': random.uniform(20, width-20),
        'y': 20,
        'vx': random.uniform(-5, 5),
        'vy': random.uniform(-5, 5),
        'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        'radius': 10,
        'active': True
    }
    for _ in range(num_balls)
]
g = 0.5
bounce_factor = 0.8
velocity_threshold = 0.1
friction = 0.99

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ball in balls:
        if not ball['active']:
            continue

        ball['vy'] += g
        ball['x'] += ball['vx']
        ball['y'] += ball['vy']

        if ball['x'] <= ball['radius'] or ball['x'] >= width - ball['radius']:
            ball['vx'] *= -bounce_factor
            ball['x'] = max(ball['radius'], min(width - ball['radius'], ball['x']))

        if ball['y'] >= height - ball['radius']:
            ball['y'] = height - ball['radius']
            ball['vy'] *= -bounce_factor
            ball['vx'] *= friction
            if abs(ball['vy']) < velocity_threshold and abs(ball['vx']) < velocity_threshold:
                ball['active'] = False
                ball['vx'] = 0
                ball['vy'] = 0

    screen.fill((0, 0, 0))
    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball['radius'])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
