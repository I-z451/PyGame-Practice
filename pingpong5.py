import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)  # For the WIP sign

# Game states
MENU = 0
PLAYER_SELECT = 1
GAME = 2
game_state = MENU

# Game modes
NORMAL = 0
FOUR_BOARDS_SINGLE = 3
FOUR_BOARDS_TWO_PLAYER = 4
game_mode_selected = None

# Number of players
ONE_PLAYER = 1
TWO_PLAYERS = 2
num_players = None

# Fonts
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24) # For the WIP sign

# Game variables (initialized here, reset in game_loop)
player_score = 0
opponent_score = 0
ball_x = screen_width // 2 - 10 // 2
ball_y = screen_height // 2 - 10 // 2
ball_speed_x = 3
ball_speed_y = 3
player_paddle_y = screen_height // 2 - 60 // 2
opponent_paddle_y = screen_height // 2 - 60 // 2
top_paddle_x = screen_width // 2 - 60 // 2  # Initial position for top paddle
top_paddle_y = 30
bottom_paddle_x = screen_width // 2 - 60 // 2
bottom_paddle_y = screen_height - 40

def home_screen():
    global game_state, game_mode_selected
    screen.fill(black)
    title_text = font_large.render("Ping Pong", True, white)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    button_width = 200
    button_height = 50
    button_y_start = screen_height // 2 - button_height - 20

    # Normal Mode button
    normal_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, button_y_start, button_width, button_height)
    pygame.draw.rect(screen, gray, normal_button_rect)
    normal_text = font_medium.render("Normal Mode", True, white)
    normal_text_rect = normal_text.get_rect(center=normal_button_rect.center)
    screen.blit(normal_text, normal_text_rect)

    # 4 Boards Mode button
    four_boards_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, button_y_start + button_height + 20, button_width, button_height)
    pygame.draw.rect(screen, gray, four_boards_button_rect)
    four_boards_text = font_medium.render("4 Boards Mode", True, white)
    four_boards_text_rect = four_boards_text.get_rect(center=four_boards_button_rect.center)
    screen.blit(four_boards_text, four_boards_text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if normal_button_rect.collidepoint(event.pos):
                game_mode_selected = NORMAL
                game_state = PLAYER_SELECT
            elif four_boards_button_rect.collidepoint(event.pos):
                game_mode_selected = FOUR_BOARDS_SINGLE # Default to single player, will be refined in next screen
                game_state = PLAYER_SELECT

def player_select_screen():
    global game_state, num_players, game_mode_selected
    screen.fill(black)
    title_text = font_large.render("Select Players", True, white)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    button_width = 200
    button_height = 50
    button_y_start = screen_height // 2 - button_height - 40

    # 1 Player button
    one_player_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, button_y_start, button_width, button_height)
    pygame.draw.rect(screen, gray, one_player_button_rect)
    one_player_text = font_medium.render("1 Player", True, white)
    one_player_text_rect = one_player_text.get_rect(center=one_player_button_rect.center)
    screen.blit(one_player_text, one_player_text_rect)

    # 2 Players button
    two_players_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, button_y_start + button_height + 20, button_width, button_height)
    pygame.draw.rect(screen, gray, two_players_button_rect)
    two_players_text = font_medium.render("2 Players", True, white)
    two_players_text_rect = two_players_text.get_rect(center=two_players_button_rect.center)
    screen.blit(two_players_text, two_players_text_rect)

    # Back button
    back_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, button_y_start + 2 * (button_height + 20), button_width, button_height)
    pygame.draw.rect(screen, gray, back_button_rect)
    back_text = font_medium.render("Back", True, white)
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    screen.blit(back_text, back_text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if one_player_button_rect.collidepoint(event.pos):
                num_players = ONE_PLAYER
                if game_mode_selected == FOUR_BOARDS_SINGLE:
                    game_mode_selected = FOUR_BOARDS_SINGLE
                game_state = GAME
            elif two_players_button_rect.collidepoint(event.pos):
                num_players = TWO_PLAYERS
                if game_mode_selected == FOUR_BOARDS_SINGLE:
                    game_mode_selected = FOUR_BOARDS_TWO_PLAYER
                game_state = GAME
            elif back_button_rect.collidepoint(event.pos):
                game_state = MENU
                game_mode_selected = None
                num_players = None

def game_loop():
    global game_state, game_mode_selected, player_score, opponent_score, ball_x, ball_y, ball_speed_x, ball_speed_y, player_paddle_y, opponent_paddle_y, top_paddle_x, top_paddle_y, bottom_paddle_x, bottom_paddle_y, num_players

    # Reset game variables
    player_score = 0
    opponent_score = 0
    paddle_height = 60
    top_paddle_height = 10
    top_paddle_width = 60
    bottom_paddle_height = 10
    bottom_paddle_width = 60
    player_paddle_y = screen_height // 2 - paddle_height // 2
    opponent_paddle_y = screen_height // 2 - paddle_height // 2
    top_paddle_x = screen_width // 2 - top_paddle_width // 2
    top_paddle_y = 30
    bottom_paddle_x = screen_width // 2 - bottom_paddle_width // 2
    bottom_paddle_y = screen_height - 40
    ball_x = screen_width // 2 - 10 // 2
    ball_y = screen_height // 2 - 10 // 2
    ball_speed_x = 3
    ball_speed_y = 3

    paddle_width = 10
    paddle_speed = 5
    ball_size = 10
    font = pygame.font.Font(None, 36)

    running_game = True
    clock = pygame.time.Clock()

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
                    game_mode_selected = None
                    num_players = None
                    return True

        keys = pygame.key.get_pressed()
        # Player 1 controls (left vertical paddle - Red)
        if keys[pygame.K_w] and player_paddle_y > 0:
            player_paddle_y -= paddle_speed
        if keys[pygame.K_s] and player_paddle_y < screen_height - paddle_height:
            player_paddle_y += paddle_speed
        # Player 1 controls (top horizontal paddle - Red)
        if game_mode_selected == FOUR_BOARDS_TWO_PLAYER or game_mode_selected == FOUR_BOARDS_SINGLE:
            if keys[pygame.K_a] and top_paddle_x > 0:
                top_paddle_x -= paddle_speed
            if keys[pygame.K_d] and top_paddle_x < screen_width - top_paddle_width:
                top_paddle_x += paddle_speed

        # Opponent controls (right paddle - Blue)
        if game_mode_selected == NORMAL:
            if num_players == TWO_PLAYERS:
                if keys[pygame.K_UP] and opponent_paddle_y > 0:
                    opponent_paddle_y -= paddle_speed
                if keys[pygame.K_DOWN] and opponent_paddle_y < screen_height - paddle_height:
                    opponent_paddle_y += paddle_speed
            elif num_players == ONE_PLAYER:
                # Basic AI for opponent
                if opponent_paddle_y + paddle_height // 2 < ball_y and opponent_paddle_y < screen_height - paddle_height:
                    opponent_paddle_y += paddle_speed
                elif opponent_paddle_y + paddle_height // 2 > ball_y and opponent_paddle_y > 0:
                    opponent_paddle_y -= paddle_speed
        elif game_mode_selected == FOUR_BOARDS_SINGLE:
            # AI for right vertical paddle
            if opponent_paddle_y + paddle_height // 2 < ball_y and opponent_paddle_y < screen_height - paddle_height:
                opponent_paddle_y += paddle_speed
            elif opponent_paddle_y + paddle_height // 2 > ball_y and opponent_paddle_y > 0:
                opponent_paddle_y -= paddle_speed
            # AI for bottom horizontal paddle
            if bottom_paddle_x + bottom_paddle_width // 2 < ball_x and bottom_paddle_x < screen_width - bottom_paddle_width:
                bottom_paddle_x += paddle_speed
            elif bottom_paddle_x + bottom_paddle_width // 2 > ball_x and bottom_paddle_x > 0:
                bottom_paddle_x -= paddle_speed
        elif game_mode_selected == FOUR_BOARDS_TWO_PLAYER:
            # Player 2 controls (right vertical paddle - Blue)
            if keys[pygame.K_UP] and opponent_paddle_y > 0:
                opponent_paddle_y -= paddle_speed
            if keys[pygame.K_DOWN] and opponent_paddle_y < screen_height - paddle_height:
                opponent_paddle_y += paddle_speed
            # Player 2 controls (bottom horizontal paddle - Blue)
            if keys[pygame.K_LEFT] and bottom_paddle_x > 0:
                bottom_paddle_x -= paddle_speed
            if keys[pygame.K_RIGHT] and bottom_paddle_x < screen_width - bottom_paddle_width:
                bottom_paddle_x += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        player_paddle_rect = pygame.Rect(50, player_paddle_y, 10, 60)
        opponent_paddle_rect = pygame.Rect(screen_width - 50 - 10, opponent_paddle_y, 10, 60)
        ball_rect = pygame.Rect(ball_x, ball_y, 10, 10)
        top_paddle_rect = pygame.Rect(top_paddle_x, top_paddle_y, 60, 10)
        bottom_paddle_rect = pygame.Rect(bottom_paddle_x, bottom_paddle_y, 60, 10)

        if ball_rect.colliderect(player_paddle_rect):
            ball_speed_x *= -1
        if ball_rect.colliderect(opponent_paddle_rect):
            ball_speed_x *= -1
        if game_mode_selected == FOUR_BOARDS_SINGLE or game_mode_selected == FOUR_BOARDS_TWO_PLAYER:
            if ball_rect.colliderect(top_paddle_rect):
                ball_speed_y *= -1
                ball_y = top_paddle_rect.bottom + 1
            if ball_rect.colliderect(bottom_paddle_rect):
                ball_speed_y *= -1
                ball_y = bottom_paddle_rect.top - ball_size - 1

        if game_mode_selected == FOUR_BOARDS_SINGLE or game_mode_selected == FOUR_BOARDS_TWO_PLAYER:
            if ball_y <= 0:
                opponent_score += 1
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_y *= -1
            elif ball_y >= screen_height - ball_size:
                player_score += 1
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_y *= -1
            elif ball_x <= 0:
                opponent_score += 1
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_x *= -1
            elif ball_x >= screen_width - ball_size:
                player_score += 1
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_x *= -1
        else: # Normal Mode Scoring
            if ball_y <= 0 or ball_y >= screen_height - ball_size:
                ball_speed_y *= -1
            if ball_x < 0:
                opponent_score += 1
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_x *= -1
            elif ball_x > screen_width:
                player_score += 1
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_x *= -1

        screen.fill(black)
        # Draw paddles with appropriate colors based on game mode
        if game_mode_selected == FOUR_BOARDS_SINGLE or game_mode_selected == FOUR_BOARDS_TWO_PLAYER:
            pygame.draw.rect(screen, red, (50, player_paddle_y, 10, 60))  # Left paddle (red)
            pygame.draw.rect(screen, blue, (screen_width - 50 - 10, opponent_paddle_y, 10, 60))  # Right paddle (blue)
            pygame.draw.rect(screen, red, (top_paddle_x, top_paddle_y, 60, 10))  # Top paddle (red)
            pygame.draw.rect(screen, blue, (bottom_paddle_x, bottom_paddle_y, 60, 10))  # Bottom paddle (blue)
        else: # Normal Mode
            pygame.draw.rect(screen, white, (50, player_paddle_y, 10, 60))
            pygame.draw.rect(screen, white, (screen_width - 50 - 10, opponent_paddle_y, 10, 60))

        pygame.draw.circle(screen, white, (ball_x, ball_y), 10)

        # Draw scoreboard in the center for 4 boards mode
        if game_mode_selected == FOUR_BOARDS_SINGLE or game_mode_selected == FOUR_BOARDS_TWO_PLAYER:
            red_score_text = font_medium.render(f"{player_score}", True, red)
            colon_text = font_medium.render(":", True, white)
            blue_score_text = font_medium.render(f"{opponent_score}", True, blue)

            red_rect = red_score_text.get_rect()
            colon_rect = colon_text.get_rect()
            blue_rect = blue_score_text.get_rect()

            total_width = red_rect.width + colon_rect.width + blue_rect.width
            start_x = screen_width // 2 - total_width // 2
            y_pos = screen_height // 2

            red_rect.midright = (start_x + red_rect.width, y_pos)
            colon_rect.midleft = red_rect.midright
            blue_rect.midleft = colon_rect.midright

            screen.blit(red_score_text, red_rect)
            screen.blit(colon_text, colon_rect)
            screen.blit(blue_score_text, blue_rect)
        else: # Normal Mode Scoreboard
            player_score_text = font.render(str(player_score), True, white)
            opponent_score_text = font.render(str(opponent_score), True, white)
            screen.blit(player_score_text, (screen_width // 4, 20))
            screen.blit(opponent_score_text, (screen_width * 3 // 4, 20))

        # Remove middle line in 4 boards mode
        if game_mode_selected == NORMAL:
            pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 1)

        pygame.display.flip()
        clock.tick(60)

    return True

running = True
while running:
    if game_state == MENU:
        home_screen()
    elif game_state == PLAYER_SELECT:
        player_select_screen()
    elif game_state == GAME:
        if not game_loop():
            running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()