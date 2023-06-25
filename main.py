import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# DISPLAY
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIRE")
# ===================================

# DIFFICULTY SETTINGS
FPS = 60
VEL = 4
UFO_MAX_HEALTH = 20
SHIP_MAX_HEALTH = 3
BULLET_VEL = 5
MAX_BOMBS = 10
MAX_BULLETS = 3
TARGET_VEL = 6
TARGET_SWITCH_WAY_SECONDS = 3
BOMB_DROP_INTERVAL_SECONDS = 1
# ===================================

# SOUND LOADING
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullet-hit.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullet_fire.wav'))
LASER_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser-hit.wav'))
BOMB_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'BOMB-HIT.wav'))
DEAD_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'dead.mp3'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'win.mp3'))
BULLET_HIT_SOUND.set_volume(0.2)
BULLET_FIRE_SOUND.set_volume(0.2)
LASER_HIT_SOUND.set_volume(0.2)
BOMB_HIT_SOUND.set_volume(0.2)
DEAD_SOUND.set_volume(0.2)
WIN_SOUND.set_volume(0.2)
# ===================================

# IMAGE LOADING
BORDER = pygame.Rect(0, 95, WIDTH, 10)
OUTLINE = 5
TARGET_SIZE = BORDER.y - OUTLINE*2
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'background.jpg'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Spaceship.png'))
SPACESHIP = pygame.transform.scale(
    SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

TARGET_IMAGE = pygame.image.load(
    os.path.join('Assets', 'UFO.png'))
TARGET_R = pygame.transform.scale(
    TARGET_IMAGE, (TARGET_SIZE, TARGET_SIZE))
# ===================================

# TEXT FONT
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
#

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
# ===================================

# EVENTS CUSTOM
SHIP_HIT = pygame.USEREVENT + 1
UFO_HIT = pygame.USEREVENT + 2
BOMB_DROP = pygame.USEREVENT + 3

# CALCULATIONS
TARGET_SWITCH_WAY_TICKS = FPS*TARGET_SWITCH_WAY_SECONDS
BOMB_DROP_INTERVAL = BOMB_DROP_INTERVAL_SECONDS * 1000
# ===================================


def draw_window(ship, target, bullets, ship_health, ufo_health, laser_stage_one, laser_stage_more_one, bombs):
    # BACKGROUND, BORDER, UFO, SPACESHIP
    WIN.fill(BLACK)
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(TARGET_R, (target.x, target.y))
    WIN.blit(SPACESHIP, (ship.x, ship.y))
    # ===================================

    # HEALTH TEXT
    ship_health_text = HEALTH_FONT.render("SHIP: " + str(ship_health), 1, WHITE)
    ufo_health_text = HEALTH_FONT.render("UFO: " + str(ufo_health), 1, WHITE)
    WIN.blit(ufo_health_text, (WIDTH - ufo_health_text.get_width() - 10, 105))
    WIN.blit(ship_health_text, (10, 105))
    # ===================================

    # BULLETS, BOMBS
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bomb in bombs:
        pygame.draw.rect(WIN, YELLOW, bomb)
    # ===================================

    # LASER
    pygame.draw.rect(WIN, GREEN, laser_stage_one)
    pygame.draw.rect(WIN, GREEN, laser_stage_more_one)
    # ===================================

    pygame.display.update()


def ship_movements(keys_pressed, ship):

    # LEFT, UP, DOWN, RIGHT
    if keys_pressed[pygame.K_LEFT] and ship.x - VEL > 0:
        ship.x -= VEL
    if keys_pressed[pygame.K_UP] and ship.y - VEL > BORDER.y + BORDER.height:
        ship.y -= VEL
    if keys_pressed[pygame.K_DOWN] and ship.y + VEL < HEIGHT - SPACESHIP_HEIGHT:
        ship.y += VEL
    if keys_pressed[pygame.K_RIGHT] and ship.x + VEL < WIDTH - SPACESHIP_WIDTH:
        ship.x += VEL
    # ===================================


def handle_bullets(bullets, target):

    # BULLET COLLISIONS
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if target.colliderect(bullet):
            pygame.event.post(pygame.event.Event(UFO_HIT))
            bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.y < 0:
            bullets.remove(bullet)
    # ===================================


def handle_bombs(bombs, ship):

    # BOMB COLLISIONS
    for bomb in bombs:
        bomb.y += 1
        if ship.colliderect(bomb):
            pygame.event.post(pygame.event.Event(SHIP_HIT))
            bombs.remove(bomb)
            BOMB_HIT_SOUND.play()
        elif bomb.y > HEIGHT:
            bombs.remove(bomb)
    # ===================================


def handle_laser(ship, laser_stage, ufo):

    # BASE LASER RESET
    laser_stage_one = pygame.Rect(
        ufo.x, ufo.y + ufo.height, ufo.width, 0)
    laser_stage_more_one = pygame.Rect(
        ufo.x + ufo.width // 2 - 10, ufo.y + ufo.height, 20, 0)
    # ===================================

    # LASER STAGE - DISPLAY
    if laser_stage >= 1:
        laser_stage_one = pygame.Rect(
            ufo.x, ufo.y + ufo.height, ufo.width, 10)
    if laser_stage > 1:
        laser_stage_more_one = pygame.Rect(
            ufo.x + ufo.width//2 - 10, ufo.y + ufo.height, 20, 100 * laser_stage)
    # ===================================

    # LASER COLLISIONS
    if ship.colliderect(laser_stage_more_one):
        pygame.event.post(pygame.event.Event(SHIP_HIT))
        laser_stage = 0
        LASER_HIT_SOUND.play()
    # ===================================

    return laser_stage_one, laser_stage_more_one, laser_stage


def target_movements(target, target_left_right):

    # RANDOM GEN. 'GO OTHER WAY'
    ran = random.randrange(1, TARGET_SWITCH_WAY_TICKS, 1)
    if ran == 1:
        if target_left_right == 0:
            target_left_right = 1
        else:
            target_left_right = 0
    # ===================================

    # GO RIGHT OR LEFT (False = RIGHT = 0 ; True = LEFT = 1)
    if target.x < WIDTH - OUTLINE - TARGET_SIZE - TARGET_VEL and target_left_right == 0:
        target.x += TARGET_VEL
    else:
        target_left_right = 1

    if target.x > OUTLINE + TARGET_VEL and target_left_right == 1:
        target.x -= TARGET_VEL
    else:
        target_left_right = 0
    # ===================================

    return target_left_right


def draw_winner(text, winner):

    # DISPLAYS 'WINNER' OR 'DEAD'
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,
             (WIDTH/2 - draw_text.get_width() / 2,
             HEIGHT/2 - draw_text.get_height() / 2))

    if winner == 0:
        DEAD_SOUND.play()
    if winner == 1:
        WIN_SOUND.play()

    pygame.display.update()
    pygame.time.delay(5000)
    # ===================================


def main():

    # CREATES: SHIP AND UFO(TARGET)
    ship = pygame.Rect(
        WIDTH/2 - SPACESHIP_WIDTH//2, HEIGHT/2 - SPACESHIP_HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    target = pygame.Rect(
        OUTLINE, OUTLINE, TARGET_SIZE, TARGET_SIZE
    )
    # ===================================

    # DIFFERENT VARIABLES
    bullets = []
    bombs = []
    ufo_laser_stage = 0
    target_left_right = 0

    ufo_health = UFO_MAX_HEALTH
    ship_health = SHIP_MAX_HEALTH

    clock = pygame.time.Clock()
    pygame.time.set_timer(BOMB_DROP, BOMB_DROP_INTERVAL)
    # ===================================

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # BOMB DROP
            if event.type == BOMB_DROP and ufo_health <= UFO_MAX_HEALTH/2 and len(bombs) < MAX_BOMBS:
                bomb = pygame.Rect(
                    target.x + target.width//2 - 5, target.y + target.height, 10, 20)
                bombs.append(bomb)
            # ===================================

            # FIRE BULLET
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        ship.x + ship.width//2 - 2, ship.y + ship.height, 5, 10)
                    bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            # ===================================

            # LASER RANDOM STAGE
            ran = random.randrange(1, 300, 1)
            if ran <= 10:
                ufo_laser_stage += 1
            elif ran >= 299:
                ufo_laser_stage = 0
            # ===================================

            # HEALTH HANDLER
            if event.type == UFO_HIT:
                ufo_health -= 1

            if event.type == SHIP_HIT:
                ship_health -= 1
            # ===================================

        # SHIP MOVEMENTS
        keys_pressed = pygame.key.get_pressed()
        ship_movements(keys_pressed, ship)
        # ===================================

        # HANDLERS OF COLLISIONS AND MOVEMENT OF ENTITIES
        handle_bullets(bullets, target)
        laser_stage_one, laser_stage_more_one, ufo_laser_stage = handle_laser(ship, ufo_laser_stage, target)
        handle_bombs(bombs, ship)

        target_left_right_copy = target_movements(target, target_left_right)
        target_left_right = target_left_right_copy
        # ===================================

        # DRAW ON DISPLAY
        draw_window(ship, target, bullets, ship_health, ufo_health, laser_stage_one, laser_stage_more_one, bombs)
        # ===================================

        # WINNER TEXT
        winner_text = ""
        winner = 0

        if ship_health <= 0:
            winner_text = "DEAD"
            winner = 0

        elif ufo_health <= 0:
            winner_text = "WINNER"
            winner = 1

        if winner_text != "":
            draw_winner(winner_text, winner)
            break
        # ===================================
    main()


if __name__ == "__main__":
    main()
