import pygame
import chess

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
GRAY = (181, 136, 99)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KSAN CHESS")

PIECES = {}
piece_types = ['P', 'B', 'N', 'R', 'Q', 'K']
for color in ['w', 'b']:
    for piece in piece_types:
        filename = f'assets/pieces/alpha/alpha/{color}{piece}.svg'
        image = pygame.image.load(filename)
        PIECES[color + piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))


# Draw board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces from board state
def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - square // 8
            col = square % 8
            color = 'w' if piece.color == chess.WHITE else 'b'
            piece_symbol = piece.symbol().lower()
            image = PIECES[color + piece_symbol.upper()]
            screen.blit(image, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    board = chess.Board()
    clock = pygame.time.Clock()
    running = True

    while running:
        draw_board()
        draw_pieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
