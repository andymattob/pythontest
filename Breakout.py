# -*- coding: utf-8 -*-
import pygame
import sys
import random

class Paddle:
    def __init__(self, x, y):
        """Initialize the Paddle class.

        Args:
            x (int): The initial x-coordinate of the paddle.
            y (int): The initial y-coordinate of the paddle.
        """
        self.rect = pygame.Rect(x, y, 80, 10)

    def draw(self, screen):
        """Draw the paddle on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the paddle on.
        """
        pygame.draw.rect(screen, (255,255,255), self.rect)

    def move(self, speed):
        """Move the paddle based on user input.

        Args:
            speed (int): The speed at which the paddle moves.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-speed, 0)
        elif keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.move_ip(speed, 0)

class Brick:
    def __init__(self, x, y):
        """Initialize the Brick class.

        Args:
            x (int): The initial x-coordinate of the brick.
            y (int): The initial y-coordinate of the brick.
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 60, 20)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, screen):
        """Draw the brick on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the brick on.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.display.set_caption('Andreas Breakout')
class Ball:
    def __init__(self, x, y):
        """Initialize the Ball class.

        Args:
            x (int): The initial x-coordinate of the ball.
            y (int): The initial y-coordinate of the ball.
        """
        self.start_x = x
        self.start_y = y
        self.reset()

    def reset(self):
        """Reset the ball to its initial position and direction."""
        self.rect = pygame.Rect(self.start_x, self.start_y, 10, 10)
        self.dx = 1
        self.dy = -1

    def draw(self, screen):
        """Draw the ball on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the ball on.
        """
        pygame.draw.rect(screen, (255,255,255), self.rect)

    def move(self, speed):
        """Move the ball based on its current direction and speed.

        Args:
            speed (int): The speed at which the ball moves.
        """
        self.rect.move_ip(self.dx * speed, self.dy * speed)

    def bounce(self, paddle, bricks):
        """Handle ball bouncing off walls, paddle, and bricks.

        Args:
            paddle (Paddle): The paddle object.
            bricks (list): List of Brick objects.

        Returns:
            int or None: The index of the brick that the ball hit, or None if no brick was hit.
        """
        if self.rect.left < 0 or self.rect.right > 800:
            self.dx *= -1
        elif self.rect.top < 0 or self.rect.colliderect(paddle.rect):
            self.dy *= -1
        else:
            hit_brick = self.rect.collidelist(bricks)
            if hit_brick != -1:
                self.dy *= -1
                return hit_brick

class BreakoutGame:
    def __init__(self, width=800, height=600):
        """Initialize the BreakoutGame class.

        Args:
            width (int, optional): Width of the game window. Defaults to 800.
            height (int, optional): Height of the game window. Defaults to 600.
        """
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.score = 0

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.paddle = Paddle(width / 2, height - 20)
        self.ball = Ball(width / 2, height / 2)

        self.lives = 3
        self.reset_bricks()

    def reset_bricks(self):
        """Reset the bricks for a new game."""
        self.bricks = []
        for i in range(5):
            for j in range(12):
                self.bricks.append(Brick(j * 60 + 50, i * 20 + 50))

    def draw_text(self, text, pos):
        """Draw text on the screen.

        Args:
            text (str): The text to display.
            pos (tuple): The position (x, y) to display the text.
        """
        surface = self.font.render(text, True, (255,255,255))
        rect = surface.get_rect(center=pos)
        self.screen.blit(surface, rect)

    def run_game(self):
        """Main game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.paddle.move(2)
            
            if not self.bricks:
                self.ball.dx = 0
                self.ball.dy = 0
                self.draw_text("Gratulerar! Du Vann!", (self.screen.get_width() / 2, self.height / 2))
                self.draw_text("Tryck på någo knapp för att starta", (self.screen.get_width() / 2, self.height / 2 + 50))

                pygame.display.flip()
                # Wait for player to press any key
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            waiting_for_input = False

                self.reset_bricks()
                self.ball.reset()
                self.paddle = Paddle(self.width / 2, self.height - 20)
                self.score = 0
                continue
            
            self.ball.move(2)
            hit_brick = self.ball.bounce(self.paddle, self.bricks)

            if hit_brick is not None:
                del self.bricks[hit_brick]
                self.score += 5

            # Check if ball hit the bottom of the screen
            if self.ball.rect.bottom > self.height:
                self.lives -= 1
                if self.lives == 0:
                    self.lives = 3
                    self.reset_bricks()
                    self.score = 0
                self.ball.reset()
                self.paddle = Paddle(self.width / 2, self.height - 20)

            self.screen.fill((128, 128, 128))
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.draw_text(f"Poäng: {self.score}", (self.screen.get_width() / 2, 20))
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    from Main import main_menu