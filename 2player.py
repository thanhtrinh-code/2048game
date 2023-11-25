import pygame
import random

pygame.init()
# Implementation: Game Over Screen (Win, Lose, Tie), probability for higher number, menu screen, music, Restart game
# Initial set up
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048 - 2 Players')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# Game variables initialize
board_values_player1 = [[0 for _ in range(4)] for _ in range(4)]
board_values_player2 = [[0 for _ in range(4)] for _ in range(4)]
game_over_player1 = False
game_over_player2 = False
spawn_new_player1 = True
spawn_new_player2 = True
init_count_player1 = 0
init_count_player2 = 0
direction_player1 = ''
direction_player2 = ''
score_player1 = 0
score_player2 = 0

# Spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# Draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, WIDTH // 2, HEIGHT], 0, 10)
    pygame.draw.line(screen, 'black', [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 5)
    score_player1_text = font.render(f'Player 1\'s Score: {score_player1}', True, 'black')
    score_player2_text = font.render(f'Player 2\'s Score: {score_player2}', True, 'black')
    screen.blit(score_player1_text, (10, 410))
    screen.blit(score_player1_text, (410, 410))

# Draw tiles for game
def draw_pieces(board, offset):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20 + offset, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font_size = 48 - (5 * value_len)
                font = pygame.font.Font('freesansbold.ttf', font_size)
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57 + offset, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20 + offset, i * 95 + 20, 75, 75], 2, 5)

# take turn based on key press
def take_turn(direc, board):
    global score_player1, score_player2
    merged = [[False for _ in range(4)] for _ in range(4)]
    #Player 1
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score_player1 += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True


    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score_player1 += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j-shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score_player1 += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][ 3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                    and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score_player1 += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    #Player 2
    elif direc == 'w':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score_player2 += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True


    elif direc == 's':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score_player2 += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif direc == 'a':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j-shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score_player2 += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'd':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][ 3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                    and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score_player2 += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# Main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')

    draw_board()
    draw_pieces(board_values_player1, 0)
    draw_pieces(board_values_player2, WIDTH // 2)

    if spawn_new_player1 or init_count_player1 < 2:
        board_values_player1, game_over_player1 = new_pieces(board_values_player1)
        spawn_new_player1 = False
        init_count_player1 += 1

    if spawn_new_player2 or init_count_player2 < 2:
        board_values_player2, game_over_player2 = new_pieces(board_values_player2)
        spawn_new_player2 = False
        init_count_player2 += 1
    
    if direction_player1 != '':
        board_values_player1 = take_turn(direction_player1, board_values_player1)
        spawn_new_player1 = True
        direction_player1 = ''
    
    if direction_player2 != '':
        board_values_player2 = take_turn(direction_player2, board_values_player2)
        spawn_new_player2 = True
        direction_player2 = ''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP: #Player 1
                direction_player2 = 'UP'
            elif event.key == pygame.K_DOWN:
                direction_player2 = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction_player2 = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction_player2 = 'RIGHT'
            elif event.key == pygame.K_w: #Player 2
                direction_player1 = 'w'
            elif event.key == pygame.K_s:
                direction_player1 = 's'
            elif event.key == pygame.K_a:
                direction_player1 = 'a'
            elif event.key == pygame.K_d:
                direction_player1 = 'd'


    pygame.display.flip()

pygame.quit()