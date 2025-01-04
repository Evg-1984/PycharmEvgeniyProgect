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

        def get_status(self):
            return self.status

        def render(self, screen):
            pygame.draw.rect(screen, self.border_color, (self.left,
                                                         self.top,
                                                         self.width,
                                                         self.height), self.border_size)
            pygame.draw.rect(screen, self.color, (self.left - self.border_size,
                                                    self.top - self.border_size,
                                                    self.width - self.border_size * 2,
                                                    self.height - self.border_size * 2), 0)
            font = pygame.font.Font(None, self.text_size)
            text = font.render(self.text, True, (100, 255, 100))
            text_x = width // 2 - text.get_width() // 2
            text_y = height // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))

        def get_cell(self, mouse_pos):
            cell_x = (mouse_pos[0] - self.left) // self.cell_size
            cell_y = (mouse_pos[1] - self.top) // self.cell_size
            if (cell_x < 0 or cell_x >= self.width or
                    cell_y < 0 or cell_y >= self.height):
                return None
            return cell_x, cell_y

        def on_click(self, cell):
            self.board[cell[1]][cell[0]] = 0 if self.board[cell[1]][cell[0]] == 1 else 1
            for i in range(self.width):
                self.board[cell[1]][i] = 0 if self.board[cell[1]][i] == 1 else 1
            for i in range(self.height):
                self.board[i][cell[0]] = 0 if self.board[i][cell[0]] == 1 else 1

        def get_click(self, mouse_pos):
            cell = self.get_cell(mouse_pos)
            if not cell is None:
                self.on_click(cell)

    fps = 60
    clock = pygame.time.Clock()
    board = Button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()