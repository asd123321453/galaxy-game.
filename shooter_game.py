#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
font.init()
font1 = font1.('Arial', 40)


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shoteer')
galaxy = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

win = font1.render('you win', True, (255, 255, 255))
lose = font1.render('you lose', True, (180, 0 ,0))

max_lost = 5

clock = time.Clock()
FPS = 60
game = True

finish = False
rel_time = False
run = False
num_fire = 0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


img = 'rocke.jpg'

if rel_time == True:
    now_time = timer()


    if now_time - last_time <3:
        reload = font2.render('Wait, reload...', 1, (150, 0, 0))
        window.blit(reload, (260, 460))
    else:
        num_fire = 0
        rel_time = False

    if num_fire < 5 and rel_time == False:
       num_fire = num_fire + 1
       fire_sound.play()
       ship.fire()
       

    if num_fire >= 5 and rel_time == False:
       last_time = timer()
       rel_time = True

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, size_x, size_y, p_speed):
      super().__init__()
      self.image = transform.scale(image.load(p_image), (size_x, size_y))
      self.speed = p_speed
      self.rect = self.image.get_rect() 
      self.rect.x = x
      self.rect.y = y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#управление
class Player(GameSprite):
    def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
        self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 65:
        self.rect.x += self.speed

    def fire (self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        global lost 
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, win_width-80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()            
        

player = Player('rocket.png', win_width // 2 -80 , win_height - 100, 80, 100, 10)
bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monsters.add (Enemy('ufo.png',  randint(80, win_width -80), -40, 80, 50, randint (1, 2)))
    monsters.add(monsters)

asteroids = sprite.Group()
for i in range(1, 6):
    asteroids.add (Enemy('asteroid.png',  randint(80, win_width -80), -40, 80, 50, randint (1, 2)))
    

lost = 0
score = 0

win






while game:
    window.blit(galaxy,(0, 0))
   

    for e in event.get():
        if e.type == QUIT:
            game = False


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if num_fire < 5 and rel_time == False:
       num_fire = num_fire + 1
       fire_sound.play()
       player.fire()
       

    if num_fire >= 5 and rel_time == False:
       last_time = timer()
       rel_time = True


    if not finish:
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(galaxy, (0, 0))
        window.blit(text, (10, 50))
        window.blit(text_lose, (10, 20))
        player.reset()
        player.update()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        sprites_list = sprite.spritecollide(player, monsters, False)
        if lost >= max_lost:
            finish = True
            window.blit(lose, (320, 235))

        if score == 5:
            finish = True
            window.blit(win, (320, 235))
        sprite.groupcollide(asteroids, bullets, False, True)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list :
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if rel_time == True:
            now_time = timer()


            if now_time - last_time <3:
                reload = font1.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        display.update()
        
        
        

    

    


    
    clock.tick(FPS)


