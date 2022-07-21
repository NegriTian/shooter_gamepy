from pygame import *
from random import randint

from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'

img_ast = 'asteroid.png'
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_img), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0

bullets = sprite.Group()

win_width = 700
win_height = 500
display.set_caption('_____________________')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

finish = False
run = True

font.init()
font1 = font.Font(None, 26)
win = font1.render('NEVER GONNA GIVE YOU UP NEVER GONNA LET YOU DOWN', True, (0, 255, 0))
lose = font1.render('DEAD INSIDE', True, (255, 0, 0))

font2 = font.Font(None, 36)
score = 0
lost = 0

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

img_enemy = 'ufo.png'

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), 40, 80, 50, randint(1, 5))
    monsters.add(monster)

max_lost = 3
goal = 20

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid(img_ast, randint(30, win_width-30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

rel_time = False
num_fire = 0

while run:
    for e in event.get():                    
        if e.type == QUIT:
            run = False
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт' + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))

        text_lost = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font2.render('Подождите, идет перезарядка...', 1, (255, 0, 0))
                window.blit(reload_text, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if lost >= max_lost:
            finish = True

        ship.update()
        ship.reset()

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (255, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        monsters.update()
        monsters.draw(window)

        display.update()
    else:
        finish = False
        score = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_height-30), -40, 80, 50, randint(1, 7))
    time.delay(50)