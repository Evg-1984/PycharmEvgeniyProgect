import pygame
import os
import sys
import math

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
        self.timer_interval = 180
        self.iframe = 0

    def shoot(self):
        pass

    def get_hit(self):
        self.hp -= 1
        self.iframe += self.timer_interval

    def update(self):
        if self.hp < 1:

            self.kill()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 90
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        if not self.iframe:
            if pygame.sprite.spritecollide(self, enemies, False):
                self.get_hit()
        else:
            self.iframe -= 1

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


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.jpg")

    def __init__(self, group, x, y, w, h, speed):
        super().__init__(group)
        self.original_image = pygame.transform.scale(Bullet.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.xspeed = 0
        self.yspeed = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 90
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.move_ip(self.rect.bottom)
        if (self.rect.center[0] <= -20 or self.rect.center[0] >= width + 20 or
            self.rect.center[1] <= -20 or self.rect.center[1] >= height + 20):
            self.kill()


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
                      width=1080, height=400, coords=(width // 2 - 540, height // 4 - 200), color=(255, 255, 255),
                      border_color=(0, 0, 0), border_size=25)
    end_bt = Button(buttons, status=False, text="выйти", text_size=200,
                      width=1080, height=400, coords=(width // 2 - 540, height - height // 4 - 200), color=(255, 255, 255),
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
    return Player(all_sprites, width // 2 - w // 2, height // 2 - h // 2, w, h, hp)

start_screen()
p1 = make_player(100, 80, 3)
b1 = Bullet(bullets, 500, 500, 30, 60, 0)
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
    p1.moving()
    all_sprites.update()
    all_sprites.draw(screen)
    bullets.update()
    bullets.draw(screen)
    pygame.sprite.groupcollide(enemies, bullets, False, True)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()