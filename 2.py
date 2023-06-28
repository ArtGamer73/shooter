from typing import Any
from pygame import *
from random import randint
 
# фонова музика
mixer.init()
mixer.music.load('Menu.mp3')
mixer.music.load('Legend.mp3')
mixer.music.play()

fire_sound = mixer.Sound('laser.mp3')

 
# шрифти і написи
font.init()
font2 = font.Font(None, 36)
 
# нам потрібні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_hero = "rocket.png"  # герой
img_enemy = "pon.png"  # ворог          
img_enemy2 = "ufo2.png"  # ворог
img_enemy3 = "ufo.png" #ворог
 
score = 0  # збито кораблів
lost = 0  # пропущено кораблів
 
# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)

        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet("blue.png", self.rect.centerx, self.rect.top, 10, 20, -20)
        bullets.add(bullet)
# клас спрайта-ворога
bullets = sprite.Group()

class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Enemy2(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
   
class Enemy3(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

font1 = font.Font(None, 80)

win = font1.render("YOU WON!", True, (0,255,0))
lose = font1.render("YOU LOSE!", True, (255, 0, 0))
#! уряяяяяяяяяяяяяяяяяя!!!!!

# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 25)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

monsters2 = sprite.Group()
for i in range(1, 6):
    monster = Enemy2(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
    monsters2.add(monster)

monsters3 = sprite.Group()
for i in range(1, 6):
    monster = Enemy3(img_enemy3, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
    monsters2.add(monster)
    monsters3.add(monster)




# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False

# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))
        
        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 


        # рухи спрайтів
        ship.update()
        bullets.update()
        monsters.update()
        monsters2.update()
        monsters3.update()
     

        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        monsters2.draw(window)
        monsters3.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for i in collides:
            score += 1
            enemy = Enemy("pon.png", randint(0, 600), 0, 100, 100, 5)
            monsters.add(enemy)



        for i in collides:
            score +=  3
            enemy2 = Enemy2("ufo2.png", randint(0, 600), 0, 100, 100, 5)
            monsters2.add(enemy)



        for i in collides:
            score +=  1
            enemy3 = Enemy3("ufo.png", randint(0, 600), 0, 100, 100, 5)
            monsters3.add(enemy)

        if sprite.spritecollide(ship, monsters, False) or lost >= 15:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 100:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)