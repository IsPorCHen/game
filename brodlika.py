import pygame
import random

# Инициализация Pygame
pygame.init()

# Размер окна
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ходилка-бродилка")

# Цвета
WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (200, 200, 200)
PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW]

# Игровые переменные
BOARD_SIZE = 100
CELL_SIZE = 50
players = [{"pos": 0, "skip": False, "color": PLAYER_COLORS[i]} for i in range(4)]
current_player = 0
dice_result = (0, 0)
game_over = False
message = "Игра начинается!"

# Специальные клетки
SPECIAL_CELLS = {
    10: +10, 20: -5, 30: +15, 40: -10, 50: +10, 60: -20,
    25: "skip", 45: "skip", 70: "skip", 85: "skip", 95: "skip"
}

# Шрифты
FONT = pygame.font.Font(None, 28)
LARGE_FONT = pygame.font.Font(None, 36)

def draw_board():
    """Отрисовка игрового поля."""
    for row in range(10):
        for col in range(10):
            cell_num = row * 10 + col
            color = GRAY if cell_num in SPECIAL_CELLS else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            text = FONT.render(str(cell_num), True, BLACK)
            screen.blit(text, (col * CELL_SIZE + 15, row * CELL_SIZE + 15))

def draw_players():
    """Отрисовка фишек игроков."""
    for i, player in enumerate(players):
        col, row = player["pos"] % 10, player["pos"] // 10
        x, y = col * CELL_SIZE + 25 + (i % 2) * 10, row * CELL_SIZE + 25 + (i // 2) * 10
        pygame.draw.circle(screen, player["color"], (x, y), 8)

def roll_dice():
    """Бросок кубиков."""
    return random.randint(1, 6), random.randint(1, 6)

def draw_interface():
    """Отрисовка интерфейса справа."""
    pygame.draw.rect(screen, WHITE, (550, 0, 450, HEIGHT))
    
    # Чей ход
    pygame.draw.rect(screen, PLAYER_COLORS[current_player], (600, 50, 200, 50))
    text = LARGE_FONT.render(f"Ход игрока {current_player + 1}", True, BLACK)
    screen.blit(text, (620, 65))
    
    # Кубики
    pygame.draw.rect(screen, WHITE, (600, 150, 200, 50), 2)
    text = LARGE_FONT.render(f"Кубики: {dice_result[0]} + {dice_result[1]}", True, BLACK)
    screen.blit(text, (620, 165))

    # Сообщения
    pygame.draw.rect(screen, WHITE, (600, 250, 300, 100), 2)
    text = FONT.render(message, True, BLACK)
    screen.blit(text, (610, 270))
    
    # Кнопка "Сделать ход"
    pygame.draw.rect(screen, BLUE, (600, 400, 200, 50))
    text = LARGE_FONT.render("Сделать ход", True, WHITE)
    screen.blit(text, (620, 415))

running = True
while running:
    screen.fill(WHITE)
    draw_board()
    draw_players()
    draw_interface()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 600 <= x <= 800 and 400 <= y <= 450 and not game_over:  # Кнопка "Сделать ход"
                if players[current_player]["skip"]:
                    players[current_player]["skip"] = False
                    message = f"Игрок {current_player + 1} пропускает ход!"
                else:
                    dice_result = roll_dice()
                    step = sum(dice_result)
                    players[current_player]["pos"] += step
                    players[current_player]["pos"] = min(players[current_player]["pos"], BOARD_SIZE - 1)

                    if players[current_player]["pos"] in SPECIAL_CELLS:
                        effect = SPECIAL_CELLS[players[current_player]["pos"]]
                        if isinstance(effect, int):
                            players[current_player]["pos"] = max(0, min(players[current_player]["pos"] + effect, BOARD_SIZE - 1))
                        else:
                            players[current_player]["skip"] = True
                            message = f"Игрок {current_player + 1} пропускает ход!"

                    if players[current_player]["pos"] == BOARD_SIZE - 1:
                        message = f"Игрок {current_player + 1} победил!"
                        game_over = True

                current_player = (current_player + 1) % 4

pygame.quit()
