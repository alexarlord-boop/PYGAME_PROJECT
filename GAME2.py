import pygame
from pygame import draw
import pyganim
import os
import sys
import random

# h = 650
# w = 850
h = 600
w = 1000

k = 100
t = k + 1
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 100, 0)]
bright_colors = [(200, 0, 0), (0, 200, 0), (0, 0, 255), (170, 700, 0)]
GRAVITY = 10
ANIMATION_DELAY = 30
ANIMATION_DELAY_2 = 140

pygame.init()
screen = pygame.display.set_mode(size=(w, h))
os.environ['SDL_VIDEO_CENTERED'] = '1'


def load_img(filename, colorkey=None):
    img_name = os.path.join('data', filename)
    image = pygame.image.load(img_name)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


#        IMAGES
# HERO
hero_images = [pygame.transform.scale(load_img(f'x wing/wing{i}.png'), (k, k)) for i in range(1, 5)]
# BLASTERS
red_shot = pygame.transform.scale(load_img('blasterR.png'), (k, k))
green_shot = pygame.transform.scale(load_img('blasterG.png'), (k, k))
bfg = load_img('BFG.png')
shots_images = [red_shot, green_shot, bfg]

# GAME OBJECTS
asteroids_images = [pygame.transform.scale(load_img(f'asteroids/aster{i}.png', -1), (50, 50)) for i in range(1, 7)]
explosion_images = [pygame.transform.scale(load_img(f'explode/{i}.png', -1), (40, 40)) for i in range(1, 8)]
bonus_images = [load_img(f'bonus{i}.png', -1) for i in range(1, 3)]
# GAME SCREEN I.
pause_img = load_img(f'screen_img/pause.png')
gameover_img = load_img(f'screen_img/gameover.png')
win_img = load_img(f'screen_img/win.png')
start_img = load_img(f'screen_img/start2.png')
rules = load_img('screen_img/rules.png')

quit_button = pygame.transform.scale(load_img(f'buttons/QUITB.png'), (200, 50))
restart_button = pygame.transform.scale(load_img(f'buttons/RESB.png'), (200, 50))
resume_button = pygame.transform.scale(load_img(f'buttons/RESUMEB.png'), (200, 50))
newgame_button = pygame.transform.scale(load_img(f'buttons/NEWGAME.png'), (200, 50))
buttons_images = {'new game': newgame_button, 'quit': quit_button, 'restart': restart_button, 'resume': resume_button}

hp_line = pygame.transform.scale(load_img(f'player_info/hp_line.png'), (100, 10))
hp_border = pygame.transform.scale(load_img(f'player_info/hp_border.png'), (100, 10))

# ANIMATION
ANIMATION_FLY = [(pygame.transform.scale(load_img(f'fire/{i}.png'), (k, k)), ANIMATION_DELAY_2) for i in range(1, 6)]
ANIMATION_EXPLODE = [(pygame.transform.scale(load_img(f'explode/{i}.png'), (50, 50)), ANIMATION_DELAY_2) for i in
                     range(1, 8)]

# SOUNDS
fire_s = pygame.mixer.Sound('data/sounds/FIRE1.wav')
fire_s.set_volume(0.05)
fire_2 = pygame.mixer.Sound('data/sounds/FIRE2_0.wav')
fire_2.set_volume(0.05)
fire_3 = pygame.mixer.Sound('data/sounds/FIRE3.wav')
fire_3.set_volume(0.2)
bonus = pygame.mixer.Sound('data/sounds/Bonus.wav')
bonus.set_volume(0.2)

explode_s = pygame.mixer.Sound('data/sounds/explode.wav')
explode_s.set_volume(0.7)

droid_s = [pygame.mixer.Sound(f'data/sounds/droid/{i}.wav') for i in range(1, 4)]
for elem in droid_s:
    elem.set_volume(0.3)

# GROUPS
ships = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
blaster_shots = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
all_bonuses = pygame.sprite.Group()
everything_on_screen = [ships, blaster_shots, asteroids, all_sprites, all_bonuses]

pause = False
gameover = False
start = False


def terminate():
    pygame.quit()
    sys.exit()


# SCREENS & UI
def game_screen(screen_img, buttons, ev):
    global start, running, pause, gameover
    pygame.mouse.set_visible(True)
    pygame.mouse.set_pos(w // 2, h // 2)
    mouse_pos = (-1, -1)
    if ev:
        pygame.mixer.music.set_volume(0.15)
    while ev:

        buttons_menu = Menu(w, h, 20, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

        # for group in everything_on_screen:
        #    group.draw(screen)

        buttons_menu.update(mouse_pos)

        screen.blit(screen_img, (w // 2 - 250, 50))
        pygame.display.flip()


def start_screen(screen_img):  # заменен функцией game_screen()
    global start
    pygame.mouse.set_visible(True)
    mouse_pos = (-1, -1)

    while not start:

        buttons_menu = Menu(w, h, 20, ['quit', 'new game'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

        # for group in everything_on_screen:
        # group.draw(screen)

        buttons_menu.update(mouse_pos)
        screen.blit(screen_img, (w // 3, h // 3))
        pygame.display.flip()


def pause_screen(screen_img):
    global pause, running
    pygame.mouse.set_visible(True)
    mouse_pos = (-1, -1)

    while pause:

        buttons_menu = Menu(w, h, 20, ['quit', 'resume', 'restart'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

        for group in everything_on_screen:
            group.draw(screen)

        buttons_menu.update(mouse_pos)

        screen.blit(screen_img, (w // 2 - 250, 10))
        pygame.display.flip()


def gameover_screen(screen_img):  # заменен функцией game_screen()
    global gameover, running
    pygame.mouse.set_visible(True)
    mouse_pos = (-1, -1)

    buttons_menu = Menu(w, h, 20, ['quit', 'restart'])

    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

        for group in everything_on_screen:
            group.draw(screen)

        buttons_menu.update(mouse_pos)

        screen.blit(screen_img, (0, 0))
        pygame.display.flip()

    # CLASSES


class Button:
    def __init__(self, x, y, type_b, func):
        global bright_colors, colors, buttons_images
        self.x = x
        self.y = y
        self.a = 200
        self.b = 50
        self.image = buttons_images[type_b]

        self.func = func
        self.hover = False
        self.clicked = False
        self.mouse_pos = (0, 0)

        self.surf = pygame.Surface((self.a, self.b))
        self.surf.fill((0, 0, 0))
        # self.surf.set_alpha(2)

        self.surf.blit(self.image, (0, 0))
        # self.surf.set_alpha(255)
        # draw.rect(self.surf, self.color, (self.x, self.y, self.a, self.b))

    def mouse_on_button(self, mpos):
        # print(mpos)
        self.mouse_pos = mpos
        if mpos[0] in range(self.x, self.x + self.a) and mpos[1] in range(self.y, self.y + self.b):
            # print(self.mouse_pos)
            return True

        else:
            return False

    def mouse_clicked_on_button(self, mpos):
        if self.mouse_on_button(mpos):
            self.func_call()
            # print(self.func)

    def func_call(self):
        global start, pause, gameover

        if self.func == 'quit':
            terminate()
        elif self.func == 'restart' or self.func == 'new game':
            start = True
            gameover = False
            game_loop()
        elif self.func == 'resume':
            pause = False


class Menu:
    def __init__(self, win_w, win_h, xd, args):
        self.n = len(args)
        self.xd = xd
        self.pos = ((win_w - (self.n * (xd + 200))) // 2, win_h - win_h // 3)
        self.buttons = [Button(x=self.pos[0] + (200 + self.xd) * i, y=self.pos[1], type_b=args[i],
                               func=args[i]) for i
                        in range(self.n)]

        # print(self.buttons[1].func)

    def update(self, mpos):
        for button in self.buttons:
            screen.blit(button.surf, (button.x, button.y))
            button.surf.set_alpha(10)
            # screen.blit(button.surf, (button.x + 2, button.y + 2))
            button.mouse_clicked_on_button(mpos)


class MeasureLine:
    def __init__(self, x, y, w_size, h_size, k_t, color, orientation='horizontal'):
        super().__init__()
        self.base = 100
        self.k = k_t

        self.x = x - w_size // 2 - 50
        self.y = y - 10
        self.w = w_size
        self.h = h_size

        self.rect = [self.x, self.y, self.w, self.h]
        self.color = pygame.Color(color)
        self.orientation = orientation

        self.surf = pygame.Surface((self.rect[2], self.rect[3]))
        self.surf.fill(self.color)

    def update(self, new_number):
        if new_number < 0:
            pass
        else:
            if self.orientation == 'horizontal':
                self.surf = pygame.transform.scale(self.surf, (new_number * self.k, self.h))

            else:
                self.surf = pygame.transform.scale(self.surf,
                                                   (self.w, self.h * new_number * self.k // self.base))

        self.draw()

    def draw(self):
        screen.blit(self.surf, (self.rect[0], self.rect[1]))
        draw.rect(screen, pygame.Color('yellow'), (self.x, self.y, self.w, self.h), 1)


# MAIN CLASSES
class Hero(pygame.sprite.Sprite):
    def __init__(self, ship_images, direction):
        super().__init__()
        global h, w, k
        self.image = ship_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = w / 2 - self.rect[2] / 2
        self.rect.y = h - k * 2
        self.pos = (self.rect.x, self.rect.y)

        self.hp = 100
        self.hp_l = MeasureLine(w // 2, h - 10, self.hp, 10, 1, 'red')
        self.hitted = False
        self.hits = 0

        self.shield = 1
        self.sp_l = MeasureLine(w // 2 + 105, h - 10, 75, 10, 1, 'blue')

        self.bonus_type = ''
        self.bonus_points = 1
        self.bonus_l = MeasureLine(90, h - 100, 10, 100, 1, 'green', 'vert')

        self.dest_way = MeasureLine(70, h - 100, 10, 100, 1, 'red', 'vert')

        self.direction = direction
        self.speed = 4
        self.shots = []

        self.heroAnim = pyganim.PygAnimation(ANIMATION_FLY)
        self.heroAnim.play()

        self.heroAnimEx = pyganim.PygAnimation(ANIMATION_EXPLODE)
        self.heroAnimEx.play()

        blaster_shots.add(self.shots)
        ships.add(self)

    def move(self, pressed):
        if bool(sum(pressed)) is False:
            self.update(1)

        if pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.update(3)

        if pressed[pygame.K_d] and self.rect.x < w - k:
            self.rect.x += self.speed
            self.update(2)

        if pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.update(1)
            self.heroAnim.blit(self.image, (0, 0))

        if pressed[pygame.K_s] and self.rect.y <= h - k:
            self.rect.y += self.speed
            self.update(0)

        collided_sp = pygame.sprite.spritecollide(self, asteroids, False)
        collided_gp = pygame.sprite.groupcollide(blaster_shots, asteroids, False, False)

        if collided_sp:
            if collided_sp[0].hit_ship is False:
                self.take_damage(collided_sp[0].damage)
                collided_sp[0].hit_ship = True
                collided_sp[0].take_damage(5)

        for elem in collided_gp.values():
            # print(elem[0].strength)
            if elem[0].b_type_hit == 2:
                self.inc_total_health(1)

    def inc_total_health(self, point):
        if self.hp >= 100:
            pass
        else:
            self.hp += point

    def reload(self, c_type):

        if c_type == 2:
            new_shot = Shot((self.rect.x + self.rect[2] // 2 - 50, self.rect.y), c_type, 7)
            self.bonus_points -= 20
            if self.bonus_points <= 0:
                self.bonus_points = 1
                self.bonus_type = ''

        else:
            new_shot = Shot((self.rect.x, self.rect.y), c_type, 19)

        self.shots.append(new_shot)
        blaster_shots.add(new_shot)

    def shooting(self):
        for shot in self.shots:
            if self.direction > 0:
                shot.move(1)

            else:
                shot.move(-1)

    def take_damage(self, heatpoint):
        global gameover
        if self.shield > 2:
            self.shield -= heatpoint
        else:
            if heatpoint != 0:
                self.hp -= heatpoint
                droid_s[0].play()

        self.hitted = True
        self.hits += 1
        if self.shield < 0:
            droid_s[1].play()
            self.shield = 1
            self.update()
        # print(f'HERO -{heatpoint}')
        if self.hp <= 0:
            self.hp = 0
            droid_s[2].play()
            self.update()
            gameover = True
            explode_s.play()
            self.kill()
            # pygame.mixer.music.stop()
            print('GAME OVER')

    def update(self, arg=None):
        if arg is not None:
            self.image = hero_images[arg].copy()

        self.sp_l.update(self.shield)
        # self.sp_l.draw()
        self.hp_l.update(self.hp)
        # self.hp_l.draw()
        self.bonus_l.update(self.bonus_points)
        # self.bonus_l.draw()
        self.dest_way.draw()

        # print(self.shield)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, b_type, bonus, target):
        global w, h, hero, bonus_images
        super().__init__()
        self.image = bonus_images[b_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, 900)
        self.rect.y = -10
        self.speed = 3

        self.bonus = bonus
        self.target = target
        all_bonuses.add(self)

    def move(self):
        if self.rect.y >= h:
            self.kill()
        else:
            collided_sp = pygame.sprite.spritecollide(self, ships, False)
            if collided_sp:
                bonus.play()
                self.kill()
                # функции для корабля (бонусы)

        self.rect.y += self.speed

    def bonus_call(self):
        if self.bonus == 'BFG':  # BFG !!!
            # self.target.reload(2)
            self.target.bonus_type = self.bonus
            self.target.bonus_points = 100

        if self.bonus == 'Shield':
            self.target.bonus_type = self.bonus
            self.target.shield = 75

            # print(self.target.shield)
            # self.target.sp_l.update(self.target.shield)

        if self.bonus == 'BFB':
            pass

    def update(self):
        if pygame.sprite.collide_rect(self, self.target):
            # print('bonus call', self.target.bonus_points, self.bonus, sep='\n')
            self.bonus_call()
        self.move()


class Shot(pygame.sprite.Sprite):
    def __init__(self, ship_pos, c_type, speed):
        super().__init__()
        self.image = shots_images[c_type]
        self.rect = self.image.get_rect()
        self.rect.x = ship_pos[0]
        self.rect.y = ship_pos[1] + 20
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed
        self.blasted = False
        self.c_type = c_type
        if self.c_type == 0:
            self.damage = 10
        elif self.c_type == 1:
            self.damage = 20
        elif self.c_type == 2:
            self.damage = 1000

        blaster_shots.add(self)

    def move(self, dir_k):
        if self.blasted:
            self.kill()

        collided_sp = pygame.sprite.spritecollide(self, asteroids, False)
        if collided_sp:
            if self.c_type != 2:
                self.blasted = True
                self.damage = 0

        # for a_elem in asteroids:
        #    if pygame.sprite.collide_rect(self, a_elem):
        #        a_elem.take_damage(self.damage)
        #        self.blasted = True
        #        self.damage = 0
        # elem.AnimEx.blit(elem.image, (0, 0))

        if self.rect.y <= -70:
            self.damage = 0
            self.kill()
        else:
            self.rect.y -= self.speed * dir_k


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(random.choice(asteroids_images), random.randint(10, 180))
        self.k = random.randint(50, 90)
        self.image = pygame.transform.scale(self.image, (self.k, self.k))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, w)
        self.rect.y = random.randint(-500, -100)

        self.surf = pygame.Surface((80, 80))
        # self.surf.set_alpha(0)

        self.speed = random.randint(1, 4)
        self.strength = random.randint(30, 40)
        self.damage = random.randint(10, 20)

        self.timer = 0
        self.b_type_hit = -1
        self.hitted = False
        self.hit_ship = False

        self.AnimEx = pyganim.PygAnimation(ANIMATION_EXPLODE)
        self.AnimEx.play()

        asteroids.add(self)

    def move(self):
        if self.rect.y >= h + 20:
            self.kill()

        collided_sp = pygame.sprite.spritecollide(self, blaster_shots, False)

        if collided_sp:  # вместо цикла на проверку попадания
            self.take_damage(collided_sp[0].damage)
            self.b_type_hit = collided_sp[0].c_type
            # print(collided_sp[0].damage)
        else:
            self.rect.y += self.speed

    def take_damage(self, heatpoint):
        self.strength -= heatpoint
        self.hitted = True
        if self.strength <= 0:
            self.strength = 0
            self.damage = 0

    def update(self):
        self.move()

        if self.strength == 0:
            self.timer += 1
            self.AnimEx.blit(self.image, (self.rect[2] // 2 - 25, self.rect[3] // 2 - 25))

            if self.timer >= 50:
                self.kill()


class AsteroidWave:
    def __init__(self):
        self.asteroids_group = []

    def create(self, b=False):
        if b:
            self.asteroids_group.extend([Asteroid() for i in range(25)])
            # print(self.asteroids_group)

    def update(self):
        for a_elem in self.asteroids_group:
            a_elem.update()

        # print(len(self.asteroids_group))


# MAIN

UPDATEENEMY = pygame.USEREVENT + 1

clock = pygame.time.Clock()
pygame.time.set_timer(UPDATEENEMY, 5000)
fps = 60
running = True
shoot = False


def update_lvl(lvl_data, target):
    asteroid_wave_is_set = False
    endgame = False
    try:
        fase = next(lvl_data)
        print(fase)
        if fase == 'a':
            asteroid_wave_is_set = True
        elif fase == 'b1':
            a = Bonus(0, 'BFG', target)

        elif fase == 'b2':
            b = Bonus(1, 'Shield', target)

        elif fase == '-':
            pass
        elif fase == 'X':
            endgame = True
    except StopIteration:
        pass

    return [asteroid_wave_is_set, endgame]


def prepare_field():
    pygame.mixer.music.load('data/sounds/theme.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(10)

    for e_elem in everything_on_screen:
        for sprite in e_elem:
            sprite.kill()

    hero = Hero(hero_images, 1)
    a_wave = AsteroidWave()
    return hero, a_wave


def game_loop():
    global pause, running, start
    # random.randint(1, 3)
    level_n = random.randint(1, 3)
    print('Level: ',level_n)
    with open(f'data/levels/{level_n}.txt') as f:  # загрузка событий уровня
        data = f.read().split(',')
        way_l = len(data)
        fase_n = len(data)
        lvl = iter(data)

    hero, a_wave = prepare_field()  # инициализация основных объектов
    ships.add(hero)

    while running:  # главный игровой цикл

        screen.fill((0, 0, 0))

        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():

            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                running = False
                terminate()

            elif event.type == pygame.USEREVENT + 1:
                data = update_lvl(lvl, hero)  # загрузка данных о фазе уровня
                if way_l == 0:
                    pass
                else:
                    way_l -= 1
                hero.dest_way.update(100 // fase_n * way_l)

                aster, to_endgame = data[0], data[1]  # создание объектов фазы уровня
                a_wave.create(aster)

                if to_endgame:
                    game_screen(win_img, ['quit', 'new game'], to_endgame)

            elif pressed[pygame.K_SPACE]:
                pause = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and pressed[pygame.K_w]:
                    fire_2.play()
                    hero.reload(1)
                elif event.button == 1:
                    fire_s.play()
                    hero.reload(0)
                elif event.button == 2:
                    if hero.bonus_points > 1:
                        fire_3.play()
                        hero.reload(2)

        # обработка остальных событий
        if not start:
            # start_screen(start_img)
            # screen.blit(rules, (w // 2 - 100, 50))
            game_screen(start_img, ['quit', 'new game'], not start)

        elif pressed[pygame.K_SPACE]:
            hero.update()
            pause_screen(pause_img)
            # game_screen(pause_img, ['quit', 'restart', 'resume'], pause)

        elif gameover:
            game_screen(gameover_img, ['quit', 'restart'], gameover)

        pygame.mouse.set_visible(False)

        hero.move(pressed)
        hero.shooting()

        for group in everything_on_screen:
            group.draw(screen)
            for ev_elem in group:
                ev_elem.update()

        pygame.display.flip()  # смена кадра

        clock.tick(fps)


game_loop()
terminate()
