import pygame
import os
import sys
import math
import random
import tkinter as tk

if __name__ == '__main__':
    pygame.init()
    root = tk.Tk()
    size = width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    screen = pygame.display.set_mode(size)


class Button(pygame.sprite.Sprite):
    def __init__(self, group, status=True, text="", text_size=1, text_color=(0, 0, 0),
                width=1, height=1, coords=(0, 0), color=(0, 0, 0), border_size=0, border_color=(0, 0, 0)):
            super().__init__(group)
            self.width = width
            self.height = height
            self.board = [[1] * width for _ in range(height)]
            self.left = coords[0]
            self.top = coords[1]
            self.color = color
            self.border_size = border_size
            self.border_color = border_color
            self.status = status
            self.text = text
            self.text_size = text_size
            self.text_color = text_color

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def set_color(self, color):
        self.color = color

    def set_text_size(self, size):
        self.text_size = size

    def set_text(self, text):
        self.text = text

    def get_status(self):
        return self.status

    def update(self, ekran):
        mouse_pos = pygame.mouse.get_pos()
        if (self.left <= mouse_pos[0] <= self.left + self.width
                and self.top <= mouse_pos[1] <= self.top + self.height):
            pygame.draw.rect(ekran, self.border_color, (self.left - self.border_size,
                                                         self.top - self.border_size,
                                                         self.width + self.border_size * 2,
                                                         self.height + self.border_size * 2), self.border_size)
            pygame.draw.rect(ekran, self.color, (self.left,
                                                    self.top,
                                                    self.width,
                                                    self.height), 0)
        else:
            pygame.draw.rect(ekran, self.border_color, (self.left,
                                                        self.top,
                                                        self.width,
                                                        self.height), self.border_size)
            pygame.draw.rect(ekran, self.color, (self.left + self.border_size,
                                                 self.top + self.border_size,
                                                 self.width - self.border_size * 2,
                                                 self.height - self.border_size * 2), 0)
        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, self.text_color)
        text_x = (self.left + self.width // 2) - text.get_width() // 2
        text_y = (self.top + self.height // 2) - text.get_height() // 2
        ekran.blit(text, (text_x, text_y))
        self.mouse_on_button = False
    def on_click(self):
            if self.status == True:
                self.status = False
            else:
                self.status = True

    def get_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (self.left <= mouse_pos[0] <= self.left + self.width
                and self.top <= mouse_pos[1] <= self.top + self.height):
                self.on_click()




class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.timer = rows * columns

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.timer:
            self.kill()
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.timer -= 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    image = load_image("player.jpg")

    def __init__(self, group, x, y, w, h, hp):
        super().__init__(group)
        self.original_image = pygame.transform.scale(Player.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.timer_interval = 60
        self.iframe = 0
        self.shot = 0

    def shoot(self):
        make_bullet(x=self.rect.center[0],
                    y=self.rect.center[1], w=15, h=30, speed=30)
        self.shot += 20
    def get_hit(self):
        global running
        self.hp -= 1
        if self.hp < 1:
            running = False
            self.kill()
        self.iframe += self.timer_interval

    def update(self):
        self.moving()
        if self.rect.centerx <= 0:
            self.rect.centerx = 1
        if self.rect.centerx > width:
            self.rect.centerx = width
        if self.rect.centery <= 0:
            self.rect.centery = 1
        if self.rect.centery > height:
            self.rect.centery = height
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 90
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        if pygame.sprite.spritecollide(self, enemies, True):
            if not self.iframe:
                self.get_hit()
        if self.iframe > 0:
            self.iframe -= 1
        if self.shot > 0:
            self.shot -= 1

    def moving(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.move_ip(-5, 0)
        if key[pygame.K_d]:
            self.rect.move_ip(5, 0)
        if key[pygame.K_w]:
            self.rect.move_ip(0, -5)
        if key[pygame.K_s]:
            self.rect.move_ip(0, 5)
        if pygame.mouse.get_pressed()[0] and not self.shot:
            self.shoot()


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.jpg")

    def __init__(self, group, x, y, w, h, speed):
        super().__init__(group)
        self.original_image = pygame.transform.scale(Bullet.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 90
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.xspeed = (speed * math.sin(math.radians(self.angle)))
        self.yspeed = (speed * math.cos(math.radians(self.angle)))
        self.killcounter = False

    def update(self):
        if (self.rect.center[0] <= -20 or self.rect.center[0] >= width + 20 or
            self.rect.center[1] <= -20 or self.rect.center[1] >= height + 20):
            self.kill()
        if self.killcounter:
            self.kill()
        self.rect.move_ip(self.xspeed, self.yspeed)
        if pygame.sprite.spritecollide(self, enemies, False):
            self.killcounter = True



class Monster(pygame.sprite.Sprite):
    image = load_image("monster.jpg")

    def __init__(self, group, x, y, w, h, hp, speed, target):
        super().__init__(group)
        self.original_image = pygame.transform.scale(Monster.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.speed = speed
        self.target = target

    def update(self):
        if pygame.sprite.spritecollide(self, bullets, False):
            self.hp -= 1
        if self.hp <= 0:
            self.kill()
        tar_x, tar_y = self.target.rect.center
        rel_x, rel_y = tar_x - self.rect.center[0], tar_y - self.rect.center[1]
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 90
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        xspeed = (self.speed * math.sin(math.radians(self.angle)))
        yspeed = (self.speed * math.cos(math.radians(self.angle)))
        self.rect.move_ip(xspeed, yspeed)

    def kill(self):
        all_sprites.add(AnimatedSprite(load_image("pygame-8-1.png"), 8, 2, self.rect.x, self.rect.y))
        super().kill()


all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
players = pygame.sprite.Group()
fps = 60
clock = pygame.time.Clock()
running = True


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    start_bt = Button(buttons, status=False, text="начать", text_size=200,
                      width=width // 2, height=height // 3, coords=(width // 2 - width // 4, height // 4 - height // 6), color=(255, 255, 255),
                      border_color=(0, 0, 0), border_size=25)
    end_bt = Button(buttons, status=False, text="выйти", text_size=200,
                      width=width // 2, height=height // 3, coords=(width // 2 - width // 4, height - height // 6 - 200), color=(255, 255, 255),
                      border_color=(0, 0, 0), border_size=25)

    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            start_bt.get_click(event)
            end_bt.get_click(event)

        buttons.update(screen)
        if start_bt.get_status():
            return
        if end_bt.get_status():
            terminate()
        pygame.display.flip()
        clock.tick(fps)


def make_player(w, h, hp):
    return Player(players, width // 2 - w // 2, height // 2 - h // 2, w, h, hp)


def make_bullet(x, y, w, h, speed):
    b = Bullet(bullets, x, y, w, h, speed)
    all_sprites.add(b)


def make_monster(value):
    for i in range(value):
        a = random.choice([True, False])
        if a:
            b = random.randrange(-100, width + 100)
            c = random.choice([-100, height + 100])
        else:
            b = random.choice([-100, width + 100])
            c = random.randrange(-100, height + 100)
        m = Monster(enemies, b, c, 70, 40, 2, 8, p)
        all_sprites.add(m)


def make_hp_bar(color, x, y, w, h, step, value):
    if value:
        one_width = (w - step * (value - 1)) // value
        for i in range(value):
            pygame.draw.rect(screen, color, (x + (one_width + step) * i, y, one_width, h))


def make_shield(color, x, y, w, h, charge):
    if charge:
        pygame.draw.rect(screen, color, (x, y, w * charge, h))



start_screen()
p = make_player(width // 15, (width // 15) * 0.8, 5)
all_sprites.add(p)
monster_timer = 120
monster_interval = 60
while running:
    screen.fill((0, 100, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
    all_sprites.update()
    all_sprites.draw(screen)
    make_hp_bar((255, 0, 0), 50, 50, 50 * p.hp - 10, 30, 10, p.hp)
    make_shield((0, 100, 255), 50, 100, 240, 10, p.iframe / p.timer_interval)
    clock.tick(fps)
    if not monster_timer:
        wave = random.choice([1, 1, 1, 2, 2, 2, 3, 3, 4])
        make_monster(wave)
        monster_timer += monster_interval * wave
    monster_timer -= 1
    pygame.display.flip()
pygame.quit()
