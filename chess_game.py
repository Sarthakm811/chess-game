import pygame
import chess
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess - Smart GUI")

# Fonts
font = pygame.font.SysFont('Arial', 44)

# Colors
lIGHTBROWN_SQUARE = (240, 217, 181)
DARKBROWN_SQUARE = (181,136,99)
HIGHLIGHT = (0, 255, 0)
CHECK_COLOR = (255, 0, 0)
PIECE_WHITE = (255, 255, 255)
PIECE_BLACK = (0, 0, 0)

# Chess board and symbols
board = chess.Board()
selected_square = None

# Realistic chess Unicode characters
UNICODE_PIECES = {
    'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K',
    'p': 'p', 'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k'
}


def get_square(mouse_pos):
    x, y = mouse_pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)


def draw_board():
    for row in range(8):
        for col in range(8):
            color = lIGHTBROWN_SQUARE if (row + col) % 2 == 0 else DARKBROWN_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            symbol = UNICODE_PIECES[piece.symbol()]
            color = PIECE_BLACK if piece.color == chess.WHITE else PIECE_WHITE
            text = font.render(symbol, True, color)
            text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                              row * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(text, text_rect)


def draw_highlights(square):
    if square is not None:
        for move in board.legal_moves:
            if move.from_square == square:
                to_square = move.to_square
                row = 7 - (to_square // 8)
                col = to_square % 8
                pygame.draw.circle(screen, HIGHLIGHT,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)


def draw_check():
    if board.is_check():
        king_square = board.king(board.turn)
        row = 7 - (king_square // 8)
        col = king_square % 8
        pygame.draw.rect(screen, CHECK_COLOR, pygame.Rect(
            col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)


# Main game loop
running = True
while running:
    draw_board()
    draw_check()
    draw_highlights(selected_square)
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_square = get_square(pygame.mouse.get_pos())
            if selected_square is None:
                piece = board.piece_at(clicked_square)
                if piece is not None and piece.color == board.turn:
                    selected_square = clicked_square
            else:
                move = chess.Move(selected_square, clicked_square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

pygame.quit()
sys.exit()
