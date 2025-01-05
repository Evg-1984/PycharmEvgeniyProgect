import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)


    class Button:
        def __init__(self, status=True, text="", text_size=1,
                     width=1, height=1, coords=(0, 0), color=(0, 0, 0), border_size=0, border_color=(0, 0, 0)):
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

        def render(self, ekran):
            pygame.draw.rect(ekran, self.border_color, (self.left,
                                                         self.top,
                                                         self.width,
                                                         self.height), self.border_size)
            pygame.draw.rect(ekran, self.color, (self.left + self.border_size,
                                                    self.top + self.border_size,
                                                    self.width - self.border_size * 2,
                                                    self.height - self.border_size * 2), 0)
            font = pygame.font.Font(None, self.text_size)
            text = font.render(self.text, True, (100, 255, 100))
            text_x = (self.left + self.width) // 2 - text.get_width() // 2
            text_y = (self.top + self.height) // 2 - text.get_height() // 2
            ekran.blit(text, (text_x, text_y))

        def on_click(self):
            if self.status == True:
                self.status = False
            else:
                self.status = True

        def get_click(self, mouse_pos):
            if (self.left <= mouse_pos[0] <= self.left + self.width
                    and self.top <= mouse_pos[1] <= self.top + self.height):
                self.on_click()


    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(pygame.mouse.get_pos())
        clock.tick(fps)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()