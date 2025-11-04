import pygame as pg
import sys
from random import randint

WIN_SIZE = 900
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)


class TicTacToeGame:
    def __init__(self, game):
        self.game = game
        self.field_image = self.get_scaled_image('games/images/field.png', [WIN_SIZE] * 2)
        self.O_image = self.get_scaled_image('games/images/o.png', [CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image('games/images/x.png', [CELL_SIZE] * 2)

        # spelplan (INF = tom ruta)
        self.game_array = [[INF, INF, INF],
                           [INF, INF, INF],
                           [INF, INF, INF]]

        # slumpa startspelare (0 = O, 1 = X)
        self.player = randint(0, 1)

        # möjliga vinstkombinationer
        self.line_indices_array = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        self.winner = None
        self.winner_line = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 4, True)

    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            if sum_line in {0, 3}:  # 0 = O, 3 = X
                self.winner = 'XO'[sum_line == 0]
                start_v = vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER
                end_v = vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER
                self.winner_line = [
                    (int(start_v.x), int(start_v.y)),
                    (int(end_v.x), int(end_v.y))
                ]

    def run_game_process(self):
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    image = self.X_image if obj else self.O_image
                    self.game.screen.blit(image, vec2(x, y) * CELL_SIZE)

    def draw_hover_highlight(self):
        """Ritar ljusgrå highlight över den cell musen är på, om den är tom"""
        if self.winner:
            return  # ingen highlight efter att spelet är slut

        mouse_pos = pg.mouse.get_pos()
        cell = vec2(mouse_pos) // CELL_SIZE
        col, row = map(int, cell)

        if 0 <= col < 3 and 0 <= row < 3:
            if self.game_array[row][col] == INF:
                highlight_rect = pg.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                s = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
                s.fill((200, 200, 200, 80))  # ljusgrå genomskinlig
                self.game.screen.blit(s, highlight_rect.topleft)

    def draw_winner(self):
        if self.winner and self.winner_line:
            start, end = self.winner_line
            width = max(1, int(CELL_SIZE * 0.1))
            pg.draw.line(self.game.screen, pg.Color('red'), start, end, width)

            label = self.font.render(f'Spelare "{self.winner}" vinner!', True, pg.Color('white'), pg.Color('black'))
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_hover_highlight()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        if self.winner:
            pg.display.set_caption(f'Spelare "{self.winner}" vinner! Tryck på mellanslag för att starta om')
        elif self.game_steps == 9:
            pg.display.set_caption('Oavgjort! Tryck på mellanslag för att starta om')
        else:
            pg.display.set_caption(f'Spelare "{ "OX"[self.player] }" tur!')

    def run_game(self):
        self.print_caption()
        self.draw()
        self.run_game_process()


class run_Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToeGame(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToeGame(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.new_game()

    def run_game(self):
        while True:
            self.tic_tac_toe.run_game()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
   from Menu import main_menu



                