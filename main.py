import pygame
import chess

# Constants
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
GRAY = (181, 136, 99)
HIGHLIGHT = (186, 202, 43)
LAST_MOVE_COLOR = (246, 246, 105)

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
font = pygame.font.SysFont("arial", 18)

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
            score += value if piece.color == chess.WHITE else -value
    return score


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
                break
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
                break
        return min_eval, best_move


def draw_board(selected_square=None, last_move=None):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

    # Highlight selected square
    if selected_square:
        row, col = selected_square
        pygame.draw.rect(screen, HIGHLIGHT, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

    # Highlight last move
    if last_move:
        start = last_move.from_square
        end = last_move.to_square
        for sq in [start, end]:
            row = 7 - chess.square_rank(sq)
            col = chess.square_file(sq)
            pygame.draw.rect(screen, LAST_MOVE_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


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


def draw_move_history(history):
    x_offset = WIDTH + 10
    y_offset = 10
    for i, move in enumerate(history[-10:]):  # Last 10 moves
        text = font.render(f"{i + 1 + max(0, len(history)-10)}. {move}", True, (0, 0, 0))
        screen.blit(text, (10, HEIGHT - 150 + i * 15))


def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return 7 - row, col  # Convert to chess rank, file


def get_move_history_san(move_stack):
    temp_board = chess.Board()
    san_moves = []
    for move in move_stack:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)
    return san_moves


def draw_promotion_ui(color):
    # Draw a simple promotion selection box in the center
    pieces = ['q', 'r', 'b', 'n']
    box_width = 60
    box_height = 60
    x = WIDTH // 2 - 2 * box_width
    y = HEIGHT // 2 - box_height // 2
    for i, p in enumerate(pieces):
        rect = pygame.Rect(x + i * (box_width + 10), y, box_width, box_height)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        img = PIECES[color + p.upper()]
        screen.blit(img, rect)
    pygame.display.flip()


def get_promotion_choice(color):
    # Wait for user to click on a promotion piece
    pieces = ['q', 'r', 'b', 'n']
    box_width = 60
    box_height = 60
    x = WIDTH // 2 - 2 * box_width
    y = HEIGHT // 2 - box_height // 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(4):
                    rect = pygame.Rect(x + i * (box_width + 10), y, box_width, box_height)
                    if rect.collidepoint(mx, my):
                        return pieces[i]
        pygame.time.wait(10)


def main():
    board = chess.Board()
    clock = pygame.time.Clock()
    selected_square = None
    move_history = []
    running = True
    player_turn = chess.WHITE
    game_result = None

    while running:
        last_move = board.move_stack[-1] if board.move_stack else None

        # Check for game over (checkmate or stalemate)
        if not game_result and board.is_game_over():
            if board.is_checkmate():
                winner = "Black" if board.turn == chess.WHITE else "White"
                game_result = f"Checkmate! {winner} wins."
            elif board.is_stalemate():
                game_result = "Draw by stalemate."
            else:
                game_result = "Draw."

        draw_board(selected_square, last_move)
        draw_pieces(board)
        draw_move_history(get_move_history_san(board.move_stack))

        # Draw game result if game is over
        if game_result:
            result_text = font.render(game_result, True, (200, 0, 0))
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()

        if board.turn == chess.BLACK and not board.is_game_over():
            _, move = minimax(board, 3, float('-inf'), float('inf'), False)
            if move:
                # If AI move is a promotion, promote to queen
                if board.piece_at(move.from_square) and board.piece_at(move.from_square).piece_type == chess.PAWN and (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7):
                    move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                board.push(move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    # Undo AI move (if exists)
                    if len(board.move_stack) >= 1:
                        board.pop()
                    # Undo Player move (if exists)
                    if len(board.move_stack) >= 1:
                        board.pop()
                    selected_square = None

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
                        # Check for pawn promotion
                        if board.piece_at(start_square).piece_type == chess.PAWN and (chess.square_rank(end_square) == 0 or chess.square_rank(end_square) == 7):
                            # Draw promotion UI
                            draw_board(selected_square, last_move)
                            draw_pieces(board)
                            draw_promotion_ui('w')
                            promo = get_promotion_choice('w')
                            move = chess.Move(start_square, end_square, promotion={'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}[promo])
                        board.push(move)
                    selected_square = None

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
