import ChessEngine
import pygame

WIDTH = HEIGHT = 512 # screen resolution
DIMENSION = 8 # board dimension
SQ_SIZE = WIDTH // DIMENSION # square size
MAX_FPS = 15
IMAGES = {}

SQ_COLORS = (pygame.Color("white"), pygame.Color("gray"), pygame.Color("green"))

def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        image = pygame.image.load("Chess/images/" + piece + ".png")
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE,SQ_SIZE))

def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.Clock()
    screen.fill("white")
    load_images()
    gs = ChessEngine.GameState()

    running = True
    sq_selected = ()
    player_clicks = []

    possible_moves = gs.get_legal_moves()
    
    while running:
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sq_selected == (row, col): # clicked selected square, deselect
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2: # move piece
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    if move in possible_moves:
                        gs.make_move(move)
                        possible_moves = gs.get_legal_moves()
                    sq_selected = ()
                    player_clicks = []

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
                    possible_moves = gs.get_legal_moves()



        draw_game_state(screen, gs, sq_selected)
        clock.tick()
        pygame.display.flip()

def draw_game_state(screen, gs, sq_selected):
    draw_board(screen, sq_selected)
    draw_pieces(screen, gs)

def draw_board(screen, sq_selected):
    for r in range(DIMENSION):
        for c  in range(DIMENSION):
            if sq_selected == (r,c):
                color = SQ_COLORS[2]
            else:
                color = SQ_COLORS[((c+r)%2)]
            
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen: pygame.Surface, gs):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = gs.board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
