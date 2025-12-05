# make a pop up window
import random
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Project")

clock = pygame.time.Clock()


# have pop up window have a pixilated farm setting
# Colors
SKY = (130, 200, 255)
GRASS = (97, 135, 84)
BARN_RED = (180, 40, 40)
ROOF_WHITE = (240, 240, 240)
DOOR = (60, 30, 10)
RAIN = (190, 190, 255)
STORMY_SKY = (75, 86, 107)
CLOUDS = (220, 223, 230)
CLOUDS_DARK = (49, 50, 54)
PIG_HEAD = (212, 150, 198)
PIG_BODY = (250, 195, 238)

# variables
toggle_storm = False
raindrops = []
pigs = []
grass_tiles = []

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

# Clouds
clouds = [
    {
        "x": 120,
        "y": 70,
        "parts": [
            (0, 0, 180, 80),
            (50, -30, 140, 90),
            (80, 10, 130, 70)
        ],
    },
    {
        "x": 500,
        "y": 70,
        "parts": [
            (0, 0, 140, 80),
            (-50, 30, 200, 70),
            (20, 40, 160, 60)
        ],
    },
    {
        "x": 300,
        "y": 30,
        "parts": [
            (0, 0, 170, 60),
            (50, -20, 140, 70),
            (80, 10, 150, 50)
        ],
    }
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

for row in range(len(farm_art)):
    for col in range(len(farm_art[0])):
        if farm_art[row][col] == GRASS:
            grass_tiles.append((row, col))

PIG_BODY_WIDTH = int(PIXEL_WIDTH * 0.8)
PIG_BODY_HEIGHT = int(PIXEL_HEIGHT * 0.8)
PIG_HEAD_RADIUS = int(min(PIG_BODY_WIDTH, PIG_BODY_HEIGHT) / 3)

# Draw farm
def draw_farm_popup(surface):
    for row in range(len(farm_art)):
        for col in range(len(farm_art[row])):
            color = farm_art[row][col]

            if toggle_storm and color == SKY:
                color = STORMY_SKY

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

# Draw clouds
def draw_clouds(surface):
    if toggle_storm:
        color = CLOUDS_DARK
    else:
        color = CLOUDS
    
    for cloud in clouds:
        base_x = cloud["x"]
        base_y = cloud["y"]
        for dx, dy, w, h in cloud["parts"]:
            pygame.draw.ellipse(
                surface,
                color,
                (base_x + dx, base_y + dy, w, h)
            )

def update_clouds():
    for cloud in clouds:
        cloud["x"] += 3

        min_dx = min(dx for (dx, dy, w, h) in cloud["parts"])
        max_dx_w = max(dx + w for (dx, dy, w, h) in cloud["parts"])

        left_edge = cloud["x"] + min_dx

        if left_edge > WIDTH:
            cloud["x"] = -max_dx_w

def spawn_raindrops(num_drops=10):
    # Create random raindrops froma  random x coordinate at the top of the screen
    for _ in range(num_drops):
        x = random.randint(0, WIDTH)
        y = random.randint(-50, 0)
        speed = random.randint(5, 15)
        raindrops.append([x, y, speed])

def update_raindrops(surface):
    for drop in raindrops:
        drop[1] += drop[2]  # Move raindrop down by its speed
        # Draw raindrop
        pygame.draw.line(
            surface, # Surface
            RAIN, # Color
            (drop[0], drop[1]), # Start point
            (drop[0], drop[1] + 3), # End point
            1 # Thickness
        )

    # Remove raindrops that have fallen off the screen
    raindrops[:] = [drop for drop in raindrops if drop[1] < HEIGHT]

def spawn_pig():
    if not grass_tiles:
        return
    row, col = random.choice(grass_tiles)

    tile_x = col * PIXEL_WIDTH
    tile_y = row * PIXEL_HEIGHT

    body_x = tile_x + (PIXEL_WIDTH - PIG_BODY_WIDTH) / 2
    body_y = tile_y + (PIXEL_HEIGHT - PIG_BODY_HEIGHT) / 2

    pigs.append((body_x, body_y))

def draw_pigs(surface):
    for body_x, body_y in pigs:
        # Draw body
        pygame.draw.ellipse(
            surface,
            PIG_BODY, # color
            (
                body_x,
                body_y,
                PIG_BODY_WIDTH,
                PIG_BODY_HEIGHT)
        )

        # Draw head
        head_center_x = int(body_x + PIG_BODY_WIDTH - PIG_HEAD_RADIUS * 0.2)
        head_center_y = int(body_y - PIG_HEAD_RADIUS * 0.4)
        pygame.draw.circle(
            surface,
            PIG_HEAD,
            (head_center_x, head_center_y),
            PIG_HEAD_RADIUS
        )


# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_storm = not toggle_storm
                if not toggle_storm:
                    raindrops.clear()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spawn_pig()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                toggle_storm = False
                raindrops.clear()
                pigs.clear()
            
    screen.fill((0,0,0))
    draw_farm_popup(screen)
    update_clouds()
    draw_clouds(screen)
    draw_pigs(screen)

    if toggle_storm:
        spawn_raindrops()
        update_raindrops(screen)

    pygame.display.flip()
    clock.tick(30)


# make farm setting move across the screen

pygame.quit()