import pygame

# 初始化 Pygame
pygame.init()

# 設定視窗尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("打磚塊")

# 定義顏色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
orange = (255, 165, 0)

brick_colors = [blue, green, yellow, orange, red, blue]

# 擋板屬性
paddle_width = 100
paddle_height = 20
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 10
paddle_speed = 10

# 球的屬性
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = 3
ball_speed_y = -3

# 磚塊屬性
brick_width = 75
brick_height = 20
brick_padding = 5
brick_offset_top = 50
bricks = []
brick_rows = 6
brick_cols = 10

# 創建彩色磚塊
for row in range(brick_rows):
    brick_color = brick_colors[row % len(brick_colors)]
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_padding)
        brick_y = row * (brick_height + brick_padding) + brick_offset_top
        bricks.append((pygame.Rect(brick_x, brick_y, brick_width, brick_height), brick_color))

# 生命值
lives = 3
font = pygame.font.Font(None, 36)

# 遊戲時鐘
clock = pygame.time.Clock()

# 遊戲迴圈
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 處理玩家輸入
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle_x += paddle_speed

        # 邊界檢查，防止擋板移出畫面
        if paddle_x < 0:
            paddle_x = 0
        elif paddle_x > screen_width - paddle_width:
            paddle_x = screen_width - paddle_width

        # 更新球的位置
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # 處理球與邊界的碰撞
        if ball_x + ball_radius > screen_width or ball_x - ball_radius < 0:
            ball_speed_x *= -1
        if ball_y - ball_radius < 0:
            ball_speed_y *= -1
        if ball_y + ball_radius > screen_height:
            lives -= 1
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_speed_y *= -1
            if lives == 0:
                game_over = True

        # 處理球與擋板的碰撞
        if ball_y + ball_radius >= paddle_y and \
           ball_x + ball_radius > paddle_x and \
           ball_x - ball_radius < paddle_x + paddle_width:
            ball_speed_y *= -1

        # 處理球與彩色磚塊的碰撞
        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        for brick, color in list(bricks):
            if ball_rect.colliderect(brick):
                bricks.remove((brick, color))
                ball_speed_y *= -1
                break

    # 清除畫面
    screen.fill(black)

    if not game_over:
        # 繪製擋板
        pygame.draw.rect(screen, white, [paddle_x, paddle_y, paddle_width, paddle_height])

        # 繪製球
        pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)

        # 繪製彩色磚塊
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # 顯示生命值 (左上角)
        lives_text = font.render(f"Lives: {lives}", True, white)
        screen.blit(lives_text, (10, 10))
    else:
        # 顯示遊戲結束訊息
        game_over_text = font.render("Game Over", True, white)
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, text_rect)

    # 更新畫面
    pygame.display.flip()

    # 控制遊戲速度
    clock.tick(60)

# 結束 Pygame
pygame.quit()