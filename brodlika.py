import pygame
import random

pygame.init()

board_img = pygame.image.load("sprites/board.png")
BOARD_SIZE = board_img.get_width()

LEFT_BORDER = 37
RIGHT_BORDER = 37
TOP_BORDER = 40
BOTTOM_BORDER = 40

CELL_SIZE = (BOARD_SIZE - LEFT_BORDER - RIGHT_BORDER) // 10  # 64 пикселя

WIDTH, HEIGHT = BOARD_SIZE + 300, BOARD_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ходилка-бродилка")

WHITE, BLACK, BLUE, RED = (255, 255, 255), (0, 0, 0), (0, 0, 255), (200, 0, 0)


player_sprites = [
    pygame.image.load("sprites/pieceRed.png"),
    pygame.image.load("sprites/pieceGreen.png"),
    pygame.image.load("sprites/pieceBlue.png"),
    pygame.image.load("sprites/pieceYellow.png")
]

player_sprites = [pygame.transform.scale(sprite, (CELL_SIZE // 2, CELL_SIZE // 2)) for sprite in player_sprites]

players = [{"pos": 0, "skip": False, "sprite": player_sprites[i]} for i in range(4)]
current_player = 0
dice_result = (0, 0)
game_over = False
message = "Игра начинается!"
show_rules = False  # Флаг для отображения правил

dice_sprites = [pygame.image.load(f"sprites/dice{i}.png") for i in range(1, 7)]

# Спецклетки
SPECIAL_CELLS = {10: -10, 26: -10, 78: -10, 7: +10, 40: +10, 58: +10}
SKIP_CELLS = {25, 45, 70, 85, 95}
LADDERS = {81: 100, 51: 70}  # Удален переход 21 → 40

# Спрайты для правил
stop_sprite = pygame.image.load("sprites/Stop.png")
ladder_sprite = pygame.image.load("sprites/ladder1.png")
move_forward = pygame.image.load("sprites/Move(-10).png")
move_inward = pygame.image.load("sprites/Move(+10).png")

FONT = pygame.font.Font(None, 30)


def get_cell_position(cell_num):
    """Возвращает координаты центра клетки по номеру с учетом рамки."""
    if cell_num < 1:
        return LEFT_BORDER + CELL_SIZE // 2, HEIGHT - BOTTOM_BORDER - CELL_SIZE // 2

    row = (cell_num - 1) // 10
    col = (cell_num - 1) % 10 if row % 2 == 0 else 9 - (cell_num - 1) % 10

    x = LEFT_BORDER + col * CELL_SIZE + CELL_SIZE // 2
    y = HEIGHT - BOTTOM_BORDER - (row * CELL_SIZE + CELL_SIZE // 2)

    return x, y


def draw_board():
    """Отрисовка игрового поля."""
    screen.blit(board_img, (0, 0))


def draw_players():
    """Отрисовка фишек игроков с разнесением."""
    positions = {}

    for player in players:
        pos = player["pos"]
        if pos in positions:
            positions[pos] += 1
        else:
            positions[pos] = 0

        x, y = get_cell_position(pos)
        shift_x = (positions[pos] % 2) * 15 - 7
        shift_y = (positions[pos] // 2) * 15 - 7

        sprite = player["sprite"]
        sprite_rect = sprite.get_rect(center=(x + shift_x, y + shift_y))
        screen.blit(sprite, sprite_rect.topleft)


def roll_dice():
    """Бросок кубиков."""
    return random.randint(1, 6), random.randint(1, 6)


def draw_interface():
    """Отрисовка интерфейса справа."""
    pygame.draw.rect(screen, WHITE, (BOARD_SIZE, 0, 300, HEIGHT))

    text = FONT.render(f"Ход игрока {current_player + 1}", True, BLACK)
    screen.blit(text, (BOARD_SIZE + 50, 50))

    screen.blit(dice_sprites[dice_result[0] - 1], (BOARD_SIZE + 50, 150))
    screen.blit(dice_sprites[dice_result[1] - 1], (BOARD_SIZE + 150, 150))

    text = FONT.render(message, True, BLACK)
    screen.blit(text, (BOARD_SIZE + 50, 300))

    pygame.draw.rect(screen, BLUE, (BOARD_SIZE + 50, 400, 200, 50))
    text = FONT.render("Сделать ход", True, WHITE)
    screen.blit(text, (BOARD_SIZE + 80, 415))

    pygame.draw.rect(screen, RED, (BOARD_SIZE + 50, 500, 200, 50))
    text = FONT.render("Правила", True, WHITE)
    screen.blit(text, (BOARD_SIZE + 100, 515))


def draw_rules():
    """Отображение окна с правилами игры."""
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100))
    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100), 3)

    title = FONT.render("Правила игры", True, BLACK)
    screen.blit(title, (WIDTH // 2 - 60, 70))

    text_lines = [
        "1. Бросайте два кубика и двигайтесь вперед.",
        "2. Некоторые клетки имеют спецэффекты:",
        "   - Пропуск хода (красная клетка):",
        "   - Лестницы (подъем вверх):",
        "   - Движение назад (синяя клетка):",
        "   - Движение вперед (зеленая клетка):",
    ]

    y_offset = 120
    for line in text_lines:
        text = FONT.render(line, True, BLACK)
        screen.blit(text, (80, y_offset))
        y_offset += 40

    screen.blit(stop_sprite, (500, 170))  # Пропуск хода
    screen.blit(ladder_sprite, (400, 230))  # Лестница
    screen.blit(move_forward, (470, 260))
    screen.blit(move_inward, (470, 300))

    pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT - 100, 100, 40))
    text = FONT.render("Закрыть", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 35, HEIGHT - 90))


running = True
while running:
    screen.fill(WHITE)
    draw_board()
    draw_players()

    if show_rules:
        draw_rules()
    else:
        draw_interface()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if show_rules:
                if WIDTH // 2 - 50 <= x <= WIDTH // 2 + 50 and HEIGHT - 100 <= y <= HEIGHT - 60:
                    show_rules = False
            else:
                if BOARD_SIZE + 50 <= x <= BOARD_SIZE + 250 and 400 <= y <= 450 and not game_over:
                    if players[current_player]["skip"]:
                        players[current_player]["skip"] = False
                        message = f"Игрок {current_player + 1} пропускает ход!"
                    else:
                        dice_result = roll_dice()
                        step = sum(dice_result)
                        players[current_player]["pos"] += step
                        players[current_player]["pos"] = min(players[current_player]["pos"], 100)

                        if players[current_player]["pos"] in SKIP_CELLS:
                            players[current_player]["skip"] = True
                            message = f"Игрок {current_player + 1} пропускает ход!"

                        if players[current_player]["pos"] in SPECIAL_CELLS:
                            players[current_player]["pos"] += SPECIAL_CELLS[players[current_player]["pos"]]

                        if players[current_player]["pos"] in LADDERS:
                            players[current_player]["pos"] = LADDERS[players[current_player]["pos"]]

                        if players[current_player]["pos"] == 100:
                            message = f"Игрок {current_player + 1} победил!"
                            game_over = True

                    current_player = (current_player + 1) % 4

                elif BOARD_SIZE + 50 <= x <= BOARD_SIZE + 250 and 500 <= y <= 550:
                    show_rules = True

pygame.quit()
