import pygame, sys
from Button import Button


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Minecraft Java Edition")

BG = pygame.image.load("assets/minecraftBackground.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def singleplayer_game():
    
        while True:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()

          SCREEN.blit(BG, (0, 0))

          PLAY_TEXT = get_font(18).render("Select World", True, "White")
          PLAY_RECT = PLAY_TEXT.get_rect(center=(750, 50))
          SCREEN.blit(PLAY_TEXT, PLAY_RECT)

          SELECT_BACK = Button(image=pygame.image.load("assets/SelectedWorldButton.jpg"), pos=(350, 560), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          SELECT_BACK.changeColor(PLAY_MOUSE_POS)
          SELECT_BACK.update(SCREEN)
          
          CREATE_BACK = Button(image=pygame.image.load("assets/CreateNewWorldButton.jpg"), pos=(980, 560), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          CREATE_BACK.changeColor(PLAY_MOUSE_POS)
          CREATE_BACK.update(SCREEN)
          
          EDIT_BACK = Button(image=pygame.image.load("assets/EditButton.jpg"), pos=(188, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          EDIT_BACK.changeColor(PLAY_MOUSE_POS)
          EDIT_BACK.update(SCREEN)
          
          DELETE_BACK = Button(image=pygame.image.load("assets/DeleteButton.jpg"), pos=(488, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          DELETE_BACK.changeColor(PLAY_MOUSE_POS)
          DELETE_BACK.update(SCREEN)
          
          RECREATE_BACK = Button(image=pygame.image.load("assets/RecreateButton.jpg"), pos=(800, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          RECREATE_BACK.changeColor(PLAY_MOUSE_POS)
          RECREATE_BACK.update(SCREEN)
          
          PLAY_BACK = Button(image=pygame.image.load("assets/BackButton.jpg"), pos=(1100, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          PLAY_BACK.changeColor(PLAY_MOUSE_POS)
          PLAY_BACK.update(SCREEN)

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
              if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
               main_menu()

          pygame.display.update() 
    
       
def multiplayer_game():

  while True:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()

          SCREEN.blit(BG, (0, 0))

          PLAY_TEXT = get_font(18).render("Play Multiplayer", True, "White")
          PLAY_RECT = PLAY_TEXT.get_rect(center=(750, 50))
          SCREEN.blit(PLAY_TEXT, PLAY_RECT)

          PLAY_BACK = Button(image=pygame.image.load("assets/BackButton.jpg"), pos=(940, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          PLAY_BACK.changeColor(PLAY_MOUSE_POS)
          PLAY_BACK.update(SCREEN)

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

            pygame.display.update()

def realm_game():
    
     while True:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()

          SCREEN.blit(BG, (0, 0))

          PLAY_TEXT = get_font(18).render("Minecraft Realms", True, "White")
          PLAY_RECT = PLAY_TEXT.get_rect(center=(750, 50))
          SCREEN.blit(PLAY_TEXT, PLAY_RECT)

          SELECT_BACK = Button(image=pygame.image.load("assets/SelectedWorldButton.jpg"), pos=(350, 560), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          SELECT_BACK.changeColor(PLAY_MOUSE_POS)
          SELECT_BACK.update(SCREEN)
          
          CREATE_BACK = Button(image=pygame.image.load("assets/CreateNewWorldButton.jpg"), pos=(980, 560), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          CREATE_BACK.changeColor(PLAY_MOUSE_POS)
          CREATE_BACK.update(SCREEN)
          
          EDIT_BACK = Button(image=pygame.image.load("assets/EditButton.jpg"), pos=(188, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          EDIT_BACK.changeColor(PLAY_MOUSE_POS)
          EDIT_BACK.update(SCREEN)
          
          DELETE_BACK = Button(image=pygame.image.load("assets/DeleteButton.jpg"), pos=(488, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          DELETE_BACK.changeColor(PLAY_MOUSE_POS)
          DELETE_BACK.update(SCREEN)
          
          RECREATE_BACK = Button(image=pygame.image.load("assets/RecreateButton.jpg"), pos=(800, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          RECREATE_BACK.changeColor(PLAY_MOUSE_POS)
          RECREATE_BACK.update(SCREEN)
          
          PLAY_BACK = Button(image=pygame.image.load("assets/BackButton.jpg"), pos=(1100, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          PLAY_BACK.changeColor(PLAY_MOUSE_POS)
          PLAY_BACK.update(SCREEN)

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
              if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
               main_menu()

          pygame.display.update() 
           
def accessiblility_game():
    pygame.init()
    
    pygame.quit()
    
def language_game():
    
     while True:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()

          SCREEN.blit(BG, (0, 0))

          PLAY_TEXT = get_font(18).render("Language...", True, "White")
          PLAY_RECT = PLAY_TEXT.get_rect(center=(750, 50))
          SCREEN.blit(PLAY_TEXT, PLAY_RECT)
          
          FONT_TEXT = get_font(10).render("(Language translations may not be 100% accurate)", True, "White")
          FONT_RECT = FONT_TEXT.get_rect(center=(800, 580))
          SCREEN.blit(FONT_TEXT, FONT_RECT)

          PLAY_BACK = Button(image=pygame.image.load("assets/BackButton.jpg"), pos=(940, 640), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

          PLAY_BACK.changeColor(PLAY_MOUSE_POS)
          PLAY_BACK.update(SCREEN)

          for event in pygame.event.get():
           if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                  if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                          
          pygame.display.update()

def options_game():
    
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(18).render("Options", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(750, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=pygame.image.load("assets/BackButton.jpg"), pos=(640, 640), 
                       text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_IMAGE = Button(image=pygame.image.load("assets/minceraft.png"), pos=(600, 140),
                           text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        JAVA_IMAGE  = Button(image=pygame.image.load("assets/edition.png"), pos=(650, 230),
                           text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SINGLEPLAYER_BUTTON = Button(image=pygame.image.load("assets/SinglePlayerJavaButton.png"), pos=(640, 280), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/MultiPlayerJavaButton.png"), pos=(640, 303), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        REALM_BUTTON = Button(image=pygame.image.load("assets/MinecraftRealmsJavaButton.png"), pos=(640, 325), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/OptionsJavaButton.png"), pos=(590, 348), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/QuitGameJavaButton.png"), pos=(690, 348), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        ACCESSIBILITY_BUTTON = Button(image=pygame.image.load("assets/AccessibilityButton.png"), pos=(752, 348), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        LANGUAGE_BUTTON = Button(image=pygame.image.load("assets/LanguageButton.png"), pos=(528, 348), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_IMAGE.image, MENU_IMAGE.rect)
        SCREEN.blit(JAVA_IMAGE.image, JAVA_IMAGE.rect)
        
        for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, REALM_BUTTON, ACCESSIBILITY_BUTTON, LANGUAGE_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    singleplayer_game()
                if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    multiplayer_game()
                if REALM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    realm_game()
                if ACCESSIBILITY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    accessiblility_game()
                if LANGUAGE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    language_game()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
        
main_menu()