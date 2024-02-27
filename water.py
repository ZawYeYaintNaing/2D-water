import pygame, time, math, sys
from pygame import gfxdraw

pygame.init()

# window
width, height = 600, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Water")

clock = pygame.time.Clock()

# grid
grid_line = []
for row in range(0, height, 50):
    for column in range(0, width, 50):
        grid_line.append(pygame.Rect(column, row, 50, 50))

# origin point
origin = [width/2, height/2+50]

# springs
springs = []
spread = 0.06

# ball
balls = []

for i in range(0, width+1, 10):
    x, y = i, origin[1]
    vel = 0
    springs.append([x, y, vel])

# delta time
last_time = time.perf_counter()
dt_setting = 60
dt = 0

# loop
while True:
    dt = time.perf_counter() - last_time
    dt *= 60
    last_time = time.perf_counter()

    if dt > 1:
        dt = 1

    window.fill((30, 30, 30))
    water_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    water_surf.set_alpha(200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                balls.append([list(pygame.mouse.get_pos()), 0, 0.3, pygame.mouse.get_pos()])
    
    # render grid
    [pygame.draw.rect(window, (60, 60, 80), grid, 2) for grid in grid_line]

    mx, my = pygame.mouse.get_pos()

    # ball
    for ball in balls:
        pygame.draw.circle(window, 'orange', ball[0], 20)

        if ball[1] > 15:
            ball[1] = 15
        if ball[0][1] > height:
            balls.remove(ball)
        ball[1] += ball[2] * dt
        ball[0][1] += ball[1] * dt

    # draw
    pygame.draw.polygon(water_surf, (0, 100, 200), [(0, height)] + [spring[:2] for spring in springs] + [(width, height)])
    window.blit(water_surf, (0, 0))
    pygame.draw.lines(window, (200, 200, 200), False, [spring[:2] for spring in springs], 4)

    # springs water
    for data in springs:
        # surface rect as dots
        spring = pygame.Rect(data[:2], (25, 25))

        for ball in balls:
            if spring.collidepoint(ball[0]):
                if abs(-0.005 * (data[1] - origin[1]) + -0.05 * data[2]) < 0.3:
                    data[2] += ball[1] * dt

        if spring.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
            if abs(-0.005 * (data[1] - origin[1]) + -0.05 * data[2]) < 0.3:
                data[1] += (my - data[1]) * dt
        else:
            extension = data[1] - origin[1]
            loss = -0.05 * data[2]

            force = -0.005 * extension + loss
            data[2] += force  * dt # velocity

            data[1] += data[2] * dt # y pos

        # spreading
        if springs.index(data) > 0:
            springs[springs.index(data) - 1][2] += spread * (springs[springs.index(data)][1] - springs[springs.index(data) - 1][1]) * dt
        try:
            springs[springs.index(data) + 1][2] += spread * (springs[springs.index(data)][1] - springs[springs.index(data) + 1][1]) * dt
        except:
            pass
    

    # update
    pygame.display.update()
    clock.tick(1000)
    print(f"{round(clock.get_fps()):.1f}")
