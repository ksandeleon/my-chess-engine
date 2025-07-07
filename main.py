import pygame
import chess

# Constants
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
GRAY = (181, 136, 99)
HIGHLIGHT = (186, 202, 43)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KSAN CHESS")

# Load images
PIECES = {}
piece_types = ['P', 'B', 'N', 'R', 'Q', 'K']
for color in ['w', 'b']:
    for piece in piece_types:
        filename = f'assets/pieces/alpha/alpha/{color}{piece}.svg'
        image = pygame.image.load(filename)
        PIECES[color + piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(selected_square=None):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            if selected_square == (row, col):
                pygame.draw.rect(screen, HIGHLIGHT, rect, 4)

def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - square // 8
            col = square % 8
            color = 'w' if piece.color == chess.WHITE else 'b'
            symbol = piece.symbol().upper()
            image = PIECES[color + symbol]
            screen.blit(image, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return 7 - row, col  # return chess rank, file

def main():
    board = chess.Board()
    clock = pygame.time.Clock()
    selected_square = None
    running = True

    while running:
        draw_board(selected_square)
        draw_pieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                rank, file = get_square_under_mouse()
                clicked_square = chess.square(file, rank)

                if selected_square is None:
                    # First click - select piece
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == board.turn:
                        selected_square = (7 - rank, file)  # for highlighting
                        start_square = clicked_square
                else:
                    # Second click - try move
                    end_square = clicked_square
                    move = chess.Move(start_square, end_square)
                    if move in board.legal_moves:
                        board.push(move)
                    selected_square = None  # reset selection

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
