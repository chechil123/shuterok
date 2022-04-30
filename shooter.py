from pygame import *
from random import randint
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
 
# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_bullet = "bullet.png" # пуля
img_enemy = "ufo.png" # враг
 
score = 0 # сбито кораблей
lost = 0 # пропущено кораблей
count_bullets = 20
 
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        shot.play()
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        direction = randint(1,2)
        if direction == 1:
            self.rect.x += randint(1, 15)
        else:
            self.rect.x -= randint(1, 15)   
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# класс спрайта-пули   
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
 
# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
 
# создаем спрайты
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
bullets = sprite.Group()
 
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                count_bullets -= 1
                ship.fire()
 
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        text_bullets = font2.render('Пуль осталось:' + str(count_bullets),
                                    1, (255,255,255))
        window.blit(text_bullets,(10,90))
        sprite_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        for killed in sprite_list:
            score += 1
            monsters.add(monster)
        if count_bullets == 0:
            text_bullets_over = font2.render('ПУЛИ ЗАКОНЧИСЬ',
                                            1, (255,0,0))
            text_bullets_over1 = font2.render('ПОВЕЗЛО ПОВЕЗЛО',
                                            1, (255,0,0))
            window.blit(text_bullets_over,(300,250))
            window.blit(text_bullets_over1,(300,300))
            finish = True
        if lost >= 3:
            text_lost = font1.render('ботинок',
            True, (255, 0, 0))
            window.blit(text_lost, (win_height/2, win_width/2-100))
            finish = True
        if score >= 10:
            text_win = font1.render('отлично, попуск', True, (255, 0, 0))
            window.blit(text_win, (300, 300))
            finish = True
        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
 
        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
 
        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)
