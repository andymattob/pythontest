# -*- coding: utf-8 -*-
import pygame
import sys
import random

class Paddle:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (80, 15))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move_with_mouse(self, screen_width):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

class Brick:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (60, 20))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Ball:
    def __init__(self, x, y, image, sounds):
        self.start_x = x
        self.start_y = y
        self.image = pygame.transform.scale(image, (10, 10))
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = 1
        self.dy = -1
        self.sounds = sounds

    def reset(self):
        self.rect.center = (self.start_x, self.start_y)
        self.dx = 1
        self.dy = -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, speed):
        self.rect.move_ip(self.dx * speed, self.dy * speed)

    def bounce(self, paddle, bricks):
        if self.rect.left < 0 or self.rect.right > 800:
            self.dx *= -1
            self.sounds["bounce"].play()
        elif self.rect.top < 0 or self.rect.colliderect(paddle.rect):
            self.dy *= -1
            self.sounds["bounce"].play()
        else:
            hit_brick = self.rect.collidelist([b.rect for b in bricks])
            if hit_brick != -1:
                self.dy *= -1
                self.sounds["brick_hit"].play()
                return hit_brick

class BreakoutGame:
    def __init__(self, width=800, height=600):
        pygame.init()
        pygame.mixer.init()  # 🎵 Starta ljudsystemet

        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.lives = 3

        # 🖼️ Ladda bilder
        self.bg_image = pygame.image.load("assets/background.png").convert()
        self.brick_image = pygame.image.load("assets/brick.png").convert()
        self.ball_image = pygame.image.load("assets/ball.png").convert_alpha()
        self.paddle_image = pygame.image.load("assets/paddle.png").convert_alpha()

        # 🔊 Ladda ljud
        self.sounds = {
            "bounce": pygame.mixer.Sound("assets/bounce.wav"),
            "brick_hit": pygame.mixer.Sound("assets/brick_hit.wav"),
            "lose_life": pygame.mixer.Sound("assets/lose_life.wav"),
            "win": pygame.mixer.Sound("assets/win.wav")
        }

        # 🧱 Skapa objekt
        self.paddle = Paddle(width / 2, height - 30, self.paddle_image)
        self.ball = Ball(width / 2, height / 2, self.ball_image, self.sounds)
        self.reset_bricks()

    def reset_bricks(self):
        self.bricks = []
        for i in range(5):
            for j in range(12):
                x = j * 60 + 50
                y = i * 20 + 50
                self.bricks.append(Brick(x, y, self.brick_image))

    def draw_text(self, text, pos):
        surface = self.font.render(text, True, (255,255,255))
        rect = surface.get_rect(center=pos)
        self.screen.blit(surface, rect)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.paddle.move_with_mouse(self.width)

            # 🏆 Vinst
            if not self.bricks:
                self.sounds["win"].play()
                self.ball.dx = 0
                self.ball.dy = 0
                self.draw_text("Gratulerar! Du Vann!", (self.width / 2, self.height / 2))
                self.draw_text("Tryck på någon knapp för att starta", (self.width / 2, self.height / 2 + 50))
                pygame.display.flip()

                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            waiting_for_input = False

                self.reset_bricks()
                self.ball.reset()
                self.paddle = Paddle(self.width / 2, self.height - 30, self.paddle_image)
                self.score = 0
                continue

            self.ball.move(3)
            hit_brick = self.ball.bounce(self.paddle, self.bricks)
            if hit_brick is not None:
                del self.bricks[hit_brick]
                self.score += 5

            # 💀 Boll missad
            if self.ball.rect.bottom > self.height:
                self.sounds["lose_life"].play()
                self.lives -= 1
                if self.lives == 0:
                    self.lives = 3
                    self.reset_bricks()
                    self.score = 0
                self.ball.reset()
                self.paddle = Paddle(self.width / 2, self.height - 30, self.paddle_image)

            # 🎨 Rita scenen
            self.screen.blit(self.bg_image, (0, 0))
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.draw_text(f"Poäng: {self.score}", (self.width / 2, 20))
            self.draw_text(f"Liv: {self.lives}", (70, 20))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    from Main import main_menu