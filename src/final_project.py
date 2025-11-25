# make a pop up window
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Project")

clock = pygame.time.Clock()


# have pop up window have a pixilated farm setting
# Colors
SKY = (130, 200, 255)
GRASS = (80, 180, 80)
BARN_RED = (180, 40, 40)
ROOF_WHITE = (240, 240, 240)
DOOR = (60, 30, 10)

# Farm art
farm_art = [
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [SKY]*20,
    [GRASS]*20,
]

# Add barn rows manually
for r in range(11, 20):
    row = []
    for c in range(20):
        if 6 <= c <= 13:
            if r == 11 or r == 12:       # Roof
                row.append(ROOF_WHITE)
            else:
                if r >= 14 and 9 <= c <= 10:
                    row.append(DOOR)     # Door
                else:
                    row.append(BARN_RED) # Barn body
        else:
            row.append(GRASS)
    farm_art.append(row)

PIXEL_WIDTH = WIDTH // len(farm_art[0])
PIXEL_HEIGHT = HEIGHT // len(farm_art)

# Draw farm
def draw_farm_popup(surface):
    for row in range(len(farm_art)):
        for col in range(len(farm_art[row])):
            color = farm_art[row][col]
            pygame.draw.rect(
                surface,
                color,
                (
                    col * PIXEL_WIDTH,
                    row * PIXEL_HEIGHT,
                    PIXEL_WIDTH,
                    PIXEL_HEIGHT
                )
            )

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0,0,0))
    draw_farm_popup(screen)

    pygame.display.flip()
    clock.tick(30)


# make farm setting move across the screen

# left mouse click spawns farm animals or make rain bursts

# space bar toggles storm

# r resets area

pygame.quit()