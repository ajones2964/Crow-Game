# Imports
import pygame
import random
import sys
import os

if getattr(sys, 'frozen', False):
    current_path = sys._MEIPASS
else:
    current_path = os.path.dirname(__file__)


# Initialize game engine
pygame.init()

# Settings
laser_amt = 1
# Window
TITLE = "Crow Game"
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
x, y = screen.get_size()
HEIGHT = y
WIDTH = x
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 120

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(current_path  +"/assets/fonts/Machinations.ttf", 24)
FONT_MD = pygame.font.Font(current_path  +"/assets/fonts/Machinations.ttf", 32)
FONT_LG = pygame.font.Font(current_path  +"/assets/fonts/Machinations.ttf", 64)
FONT_XL = pygame.font.Font(current_path  +"/assets/fonts/Machinations.ttf", 96)

# Images
back_img = pygame.image.load(current_path  +'/assets/images/back.png')
back_img = pygame.transform.scale(back_img, (WIDTH, HEIGHT))
ship_img = pygame.image.load(current_path  +'/assets/images/player.png')
laser_img = pygame.image.load(current_path  +'/assets/images/laserGreen.png')
mob_img = pygame.image.load(current_path  +'/assets/images/enemy.png')
bomb_img = pygame.image.load(current_path  +'/assets/images/umg.png')

# Sounds
#EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')

# Stages
START = 0
PLAYING = 1
END = 2

# Lists
lasero = 0

# Game classes
class shipHealth(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_health():
        pass
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = WIDTH/100
        self.shield = 5

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            #EXPLOSION.play()
            self.kill()

        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
            global lasero
            lasero -= 1
            
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            #EXPLOSION.play()
            player.score += 1
            self.kill()
            global lasero
            lasero -= 1


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = WIDTH/200
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()
            
# Make game objects
ship = Ship(384, (HEIGHT-128), ship_img)
mob1 = Mob((WIDTH/9 * 0.5), (HEIGHT/20), mob_img)
mob2 = Mob((WIDTH/9 * 1.5), (HEIGHT/20), mob_img)
mob3 = Mob((WIDTH/9 * 2.5), (HEIGHT/20), mob_img)
mob4 = Mob((WIDTH/9 * 3.5), (HEIGHT/20), mob_img)
mob5 = Mob((WIDTH/9 * 4.5), (HEIGHT/20), mob_img)
mob6 = Mob((WIDTH/9 * 0.5), (HEIGHT/5), mob_img)
mob7 = Mob((WIDTH/9 * 1.5), (HEIGHT/5), mob_img)
mob8 = Mob((WIDTH/9 * 2.5), (HEIGHT/5), mob_img)
mob9 = Mob((WIDTH/9 * 3.5), (HEIGHT/5), mob_img)
mob10 = Mob((WIDTH/9 * 4.5), (HEIGHT/5), mob_img)

# Make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)
player.score = 0
player.shield = ship.shield

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10)

bombs = pygame.sprite.Group()

fleet = Fleet(mobs)

def setup():
    player.score = 0
    ship = Ship(384, (HEIGHT-128), ship_img)
    mob1 = Mob((WIDTH/9 * 0.5), (HEIGHT/20), mob_img)
    mob2 = Mob((WIDTH/9 * 1.5), (HEIGHT/20), mob_img)
    mob3 = Mob((WIDTH/9 * 2.5), (HEIGHT/20), mob_img)
    mob4 = Mob((WIDTH/9 * 3.5), (HEIGHT/20), mob_img)
    mob5 = Mob((WIDTH/9 * 4.5), (HEIGHT/20), mob_img)
    mob6 = Mob((WIDTH/9 * 0.5), (HEIGHT/5), mob_img)
    mob7 = Mob((WIDTH/9 * 1.5), (HEIGHT/5), mob_img)
    mob8 = Mob((WIDTH/9 * 2.5), (HEIGHT/5), mob_img)
    mob9 = Mob((WIDTH/9 * 3.5), (HEIGHT/5), mob_img)
    mob10 = Mob((WIDTH/9 * 4.5), (HEIGHT/5), mob_img)
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10)

def levelup():
    ship = Ship(384, (HEIGHT-128), ship_img)
    mob1 = Mob((WIDTH/9 * 0.5), (HEIGHT/20), mob_img)
    mob2 = Mob((WIDTH/9 * 1.5), (HEIGHT/20), mob_img)
    mob3 = Mob((WIDTH/9 * 2.5), (HEIGHT/20), mob_img)
    mob4 = Mob((WIDTH/9 * 3.5), (HEIGHT/20), mob_img)
    mob5 = Mob((WIDTH/9 * 4.5), (HEIGHT/20), mob_img)
    mob6 = Mob((WIDTH/9 * 0.5), (HEIGHT/5), mob_img)
    mob7 = Mob((WIDTH/9 * 1.5), (HEIGHT/5), mob_img)
    mob8 = Mob((WIDTH/9 * 2.5), (HEIGHT/5), mob_img)
    mob9 = Mob((WIDTH/9 * 3.5), (HEIGHT/5), mob_img)
    mob10 = Mob((WIDTH/9 * 4.5), (HEIGHT/5), mob_img)
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10)
    fleet.speed = fleet.speed * 1.5
# set stage
stage = START

# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("Crow Game!", 1, WHITE)
    screen.blit(title_text, [(WIDTH/3), (HEIGHT/3)])

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    shield_text = FONT_MD.render(str(ship.shield), 1, WHITE)
    screen.blit(score_text, [32, 32])
    screen.blit(shield_text, [32, 64])

# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    if len(lasers) < 1:
                        ship.shoot()
                    
            

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]: 
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        if ship.shield == 0:
            done = True

        if len(mobs) == 0:
            #done = True
            levelup()

        

    #health()
            
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()

     
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(back_img, (0,0))
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    #screen.blit(hbar5_img, (0,0))
    show_stats(player)

    if stage == START:
        show_title_screen()

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
