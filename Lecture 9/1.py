import pygame, sys
from pygame.locals import *
import random, time
from pygame.transform import smoothscale
pygame.init()

FPS = pygame.time.Clock()
speed_enemy = 5    # Скорость врагов
score = 0   # Очки
coin_score = 0   # Очки за монеты
speed_coin = 3    # Скорость монет

# Шрифты для текста
font = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 20)
game_over = font.render("Game Over", True, (0, 0, 0))
background = pygame.image.load("AnimatedStreet.png")

# Настройка display
display = pygame.display.set_mode((400, 600))
display.fill((255, 255, 255))
pygame.display.set_caption("Racer Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        # Enemy появляются случайно в верхней части экрана
        self.rect.center = (random.randint(40, 400 - 40), 0)  

    def move(self):
        global score
        # Движение enemy вниз
        self.rect.move_ip(0, speed_enemy)
        if (self.rect.top > 600): # Если enemy выходит за пределы экрана
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, 400 - 40), 0) # Перемещаем enemy в верхнюю часть экрана

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        # Начальная позиция player
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed() # Движение player
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < 400:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("coin.png").convert_alpha()
        
        self.weight = random.randint(1, 3) # Случайный вес coin
        size_multiplier = 0.5 + self.weight * 0.5  # 1x, 1.5x, 2x
        self.size = int(30 * size_multiplier)
        self.image = smoothscale(original_image, (self.size, self.size))
        
        self.rect = self.image.get_rect()
        # Coin появляется случайно в верхней части экрана
        self.rect.center = (
            random.randint(40, 400-40),
            random.randint(-100, -10) 
        )
        self.speed = random.randint(2, 4)
    
    def move(self):
        self.rect.move_ip(0, self.speed)
        # Если coin выходит за пределы экрана, ее положение обновляется
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (
                random.randint(40, 400-40),
                random.randint(-100, -10)
            )
            self.speed = random.randint(2, 4)  # Случайная скорость coin
       
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 2000) # Spawn coin каждые 2000 миллисекунд 

while True:
    for event in pygame.event.get():
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display.blit(background, (0, 0)) # Отображение фона

    # Отображение счета
    score_text = font_small.render(f"Score: {score}", True, (0, 0, 0))
    display.blit(score_text, (10, 10))
    coin_text = font_small.render(f"Coins: {coin_score}", True, (0, 0, 0))
    display.blit(coin_text, (400-120, 10))
 
    # Отображение всех спрайтов и их движения
    for entity in all_sprites:
        display.blit(entity.image, entity.rect)
        entity.move()

    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected_coins:
        coin_score += coin.weight  # Увеличиваем счет в зависимости от веса монеты
        
        # Увеличиваем скорость врагов каждые 5 монет
        if coin_score % 5 == 0:
            speed_enemy += 1

    # Проверка на столкновение с enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()  # Звук столкновения
        time.sleep(0.5)   # Задержка
        display.fill((255, 0, 0))  # Красный экран
        display.blit(game_over, (90, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()   # Удаление всех спрайтов
        time.sleep(2)   # Задержка перед выходом
        pygame.quit()
        sys.exit()
        
    pygame.display.update()   # Обновление экрана
    FPS.tick(60)  # Установка частоты кадров (60 FPS)