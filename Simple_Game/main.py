import pygame
import os

# initialization
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('First Game')
WIDTH, HEIGHT = 900, 500
SPACE = pygame.transform.scale(pygame.image.load(os.path.join( '/home/dreytted/Y3 sem1/Graphics/Simple_Game', 'space.png')), (WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

#  sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('/home/dreytted/Y3 sem1/Graphics/Simple_Game', 'Grenade+1.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('/home/dreytted/Y3 sem1/Graphics/Simple_Game', 'Gun+Silencer.mp3'))

# font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# colors
RED =(255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# bullets
BULLET_VEL = 15
MAX_BULLETS = 3

# spaceship
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('/home/dreytted/Y3 sem1/Graphics/Simple_Game', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('/home/dreytted/Y3 sem1/Graphics/Simple_Game', 'spaceship_red.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)
FPS = 60
VEL = 5

# spaceship hit events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_window(red, yellow,red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))   #adding the background
    pygame.draw.rect(WIN, BLACK, BORDER) #drawing the in between surface border

    # health text
    red_health_text = HEALTH_FONT.render('Health:' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health:' + str(yellow_health), 1, WHITE)

    # drawing the spaceships
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    # drawing the bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


# function to handle the movement of the yellow spaceship
def yellow_movement(keys_pressed, yellow):

        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -=VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
            yellow.x +=VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
            yellow.y -=VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -15: # DOWN
            yellow.y +=VEL


# function to handle the movement of the red spaceship
def red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -=VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x +=VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
            red.y -=VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15: # DOWN
            red.y +=VEL

# function to handle bullet movement and hit
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# function to display the winner
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1 , WHITE)
    WIN.blit(draw_text, (WIDTH/2 -draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) #delay with the game in 5 seconds before restart

def main():
    red  = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow  = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []

    # health counter
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y+ yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y+ red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()

            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health == 0:
            winner_text = "Yellow wins"

        if yellow_health ==0:
            winner_text = "Red Wins"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets (yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow,red_bullets,yellow_bullets,red_health, yellow_health)
    main()

if __name__ == '__main__':
    main()