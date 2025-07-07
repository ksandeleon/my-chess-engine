import pygame
import chess
import random

# Constants
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
GRAY = (181, 136, 99)
HIGHLIGHT = (186, 202, 43)
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

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



def evaluate_board(board):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score  # Positive is good for white, negative for black

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move


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
    return 7 - row, col  # chess rank, file

def main():
    board = chess.Board()
    clock = pygame.time.Clock()
    selected_square = None
    running = True
    player_turn = chess.WHITE  # human plays white

    while running:
        draw_board(selected_square)
        draw_pieces(board)
        pygame.display.flip()

        if board.turn == chess.BLACK and not board.is_game_over():
            # AI's turn: make a random move
            _, move = minimax(board, 3, float('-inf'), float('inf'), False)  # AI is minimizing
            if move:
                board.push(move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == player_turn:
                rank, file = get_square_under_mouse()
                clicked_square = chess.square(file, rank)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == player_turn:
                        selected_square = (7 - rank, file)
                        start_square = clicked_square
                else:
                    end_square = clicked_square
                    move = chess.Move(start_square, end_square)
                    if move in board.legal_moves:
                        board.push(move)
                    selected_square = None

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
