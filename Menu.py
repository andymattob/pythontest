import pygame, sys
from Button import Button
from games. breakout import BreakoutGame
from games. tictactoe import run_Game, TicTacToeGame
import tkinter as tk
from games.memorygame import MemoryGame

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Menu")

BG = pygame.image.load("games/images/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def breakout_game():
    pygame.init()
    
    BreaKout = BreakoutGame()  
    BreaKout.run_game()    

   
    pygame.quit()
    
    
def tictactoe_game():
    pygame.init()
    
    TicTacToeGame = run_Game()
    TicTacToeGame.run_game()
    
    pygame.quit()

def memory_game():
    pygame.init()
    
    
    pygame.quit()
    
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("GameMenu", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 90))

        BREAKOUT_BUTTON = Button(image=pygame.image.load("assets/start_breakout_button.png"), pos=(140, 250), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        TICTACTOE_BUTTON = Button(image=pygame.image.load("assets/start_tictactoe_button.png"), pos=(350, 250), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MEMORY_BUTTON = Button(image=pygame.image.load("assets/start_tetris_button.png"), pos=(560, 250), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/exit_button.png"), pos=(440, 550), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [BREAKOUT_BUTTON, TICTACTOE_BUTTON, MEMORY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BREAKOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    breakout_game()
                if TICTACTOE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    tictactoe_game()
                if MEMORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    memory_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()