import pygame
import sys
import copy

pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 600, 600
WINDOWC = (200, 200, 200)
LINEC = (100, 100, 100)
# GRID MATH - modify WIDTH, HEIGHT and LINEW for size chanegs
LINEW = 9   # odd number preferred
LINEW2 = (LINEW - 1) / 2
SQUARE = (WIDTH - (2*LINEW))/3
LINE1 = SQUARE + LINEW2
LINE2 = (SQUARE * 2) + LINEW + LINEW2
WLINEC = (255, 0, 0)
WLINEW = 9
# ASSETS
X_IMG = pygame.image.load("assets/X.png")   # 143px/2 = 71.5 px
O_IMG = pygame.transform.scale(pygame.image.load("assets/O.png"), (143, 143))
XO_SIZE2 = 71.5

SQUARES_CENTRE = [[(SQUARE / 2 - XO_SIZE2, SQUARE / 2 - XO_SIZE2),
                   (SQUARE / 2 - XO_SIZE2, LINE1 + LINEW2 + (SQUARE / 2) - XO_SIZE2),
                   (SQUARE / 2 - XO_SIZE2, LINE2 + LINEW2 + (SQUARE / 2) - XO_SIZE2)],
                  [(LINE1 + LINEW2 + (SQUARE/2)-XO_SIZE2, SQUARE/2-XO_SIZE2),
                   (LINE1 + LINEW2 + (SQUARE/2)-XO_SIZE2, LINE1 + LINEW2 + (SQUARE/2)-XO_SIZE2),
                   (LINE1 + LINEW2 + (SQUARE/2)-XO_SIZE2, LINE2 + LINEW2 + (SQUARE/2)-XO_SIZE2)],
                  [(LINE2 + LINEW2 + (SQUARE/2)-XO_SIZE2, SQUARE/2-XO_SIZE2),
                   (LINE2 + LINEW2 + (SQUARE/2)-XO_SIZE2, LINE1 + LINEW2 + (SQUARE/2)-XO_SIZE2),
                   (LINE2 + LINEW2 + (SQUARE/2)-XO_SIZE2, LINE2 + LINEW2 + (SQUARE/2)-XO_SIZE2)]]

# BASIC DISPLAY
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

# GLOBAL VARIABLES
to_move, board = None, []


def start_game():
    global to_move, board
    WINDOW.fill(WINDOWC)
    pygame.draw.line(WINDOW, LINEC, (0, LINE1), (WIDTH, LINE1), LINEW)
    pygame.draw.line(WINDOW, LINEC, (0, LINE2), (WIDTH, LINE2), LINEW)
    pygame.draw.line(WINDOW, LINEC, (LINE1, 0), (LINE1, HEIGHT), LINEW)
    pygame.draw.line(WINDOW, LINEC, (LINE2, 0), (LINE2, HEIGHT), LINEW)
    pygame.display.update()
    to_move = 'X'
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]


def move_human(position):
    global to_move, board
    xindex = int(position[0]/(WIDTH/3))
    yindex = int(position[1]/(HEIGHT/3))
    if board[xindex][yindex] is None:
        board[xindex][yindex] = to_move
        if to_move == 'X':
            to_move = 'O'
            WINDOW.blit(X_IMG, SQUARES_CENTRE[xindex][yindex])
        else:
            to_move = 'X'
            WINDOW.blit(O_IMG, SQUARES_CENTRE[xindex][yindex])


def move_ai():
    global board, to_move
    best_xy = min_max(board, to_move)
    if board[best_xy[1]][best_xy[2]] is None:
        board[best_xy[1]][best_xy[2]] = to_move
        if to_move == 'X':
            to_move = 'O'
            WINDOW.blit(X_IMG, SQUARES_CENTRE[best_xy[1]][best_xy[2]])
        else:
            to_move = 'X'
            WINDOW.blit(O_IMG, SQUARES_CENTRE[best_xy[1]][best_xy[2]])


def check_win(current_board):
    is_game_won, winning_line, player = False, (), None
    for i in range(3):
        if current_board[i][0] == current_board[i][1] == current_board[i][2] is not None:   # VERTICAL
            is_game_won, winning_line, player = True, ((SQUARES_CENTRE[i][0][0] + XO_SIZE2, 0), (SQUARES_CENTRE[i][0][0] + XO_SIZE2, HEIGHT)), current_board[i][0]
        elif current_board[0][i] == current_board[1][i] == current_board[2][i] is not None:    # HORIZONTAL
            is_game_won, winning_line, player = True, ((0, SQUARES_CENTRE[0][i][1] + XO_SIZE2), (600, SQUARES_CENTRE[0][i][1] + XO_SIZE2)), current_board[0][i]
    if current_board[0][0] == current_board[1][1] == current_board[2][2] is not None:   # DIAGONAL
        is_game_won, winning_line, player = True, ((0, 0), (WIDTH, HEIGHT)), current_board[0][0]
    elif current_board[2][0] == current_board[1][1] == current_board[0][2] is not None:    # DIAGONAL
        is_game_won, winning_line, player = True, ((WIDTH, 0), (0, HEIGHT)), current_board[2][0]
    return is_game_won, winning_line, player


def check_tie(current_board):    # use after check win!
    is_full = True
    for i in current_board:
        if not is_full:
            break
        for j in i:
            if j is None:
                is_full = False
                break
    return is_full


def evaluation_func(current_board):
    is_game_won, winning_line, win_player = check_win(current_board)
    if is_game_won:
        if win_player == 'X':
            return 100  # MAX
        return -100    # MIN
    elif check_tie(current_board):
        return 0    # DRAW
    else:
        return None


def min_max(current_board, player):
    score = evaluation_func(current_board)
    if score is None:
        minmax_temp = None
        for xindex in range(3):     # search through possible moves
            for yindex in range(3):
                board_temp = copy.deepcopy(current_board)
                if board_temp[xindex][yindex] is None:
                    board_temp[xindex][yindex] = player
                    minmax_output = min_max(board_temp, 'O' if player == 'X' else 'X')
                    if player == 'X' and minmax_output[0] == 100:       # 'X' wants to maximise, no further search is needed
                        return minmax_output[0], xindex, yindex
                    elif player == 'O' and minmax_output[0] == -100:    # 'O' wants to minimise, no further search is needed
                        return minmax_output[0], xindex, yindex
                    elif minmax_output[0] == 0:                         # draw if player can't win
                        minmax_temp = (0, xindex, yindex)
                    else:                                               # unavoidable failure
                        if minmax_temp is None:
                            minmax_temp = minmax_output[0], xindex, yindex
        return minmax_temp
    else:
        return score, 0, 0


def main():
    start_game()
    run = True
    while run:  # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                move_ai()
                pygame.event.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                move_human(pygame.mouse.get_pos())

            game_won, winning_line_indexes, player = check_win(board)
            if game_won:
                pygame.draw.line(WINDOW, WLINEC, winning_line_indexes[0], winning_line_indexes[1], WLINEW)
                pygame.display.update()
                pygame.time.wait(1000)
                pygame.event.clear()
                start_game()
            elif check_tie(board):
                pygame.display.update()
                pygame.time.wait(1000)
                pygame.event.clear()
                start_game()
        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
