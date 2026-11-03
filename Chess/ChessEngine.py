'''
Class responsible for:
    * Chess state
    * Valid moves
    * Move log
'''
#new chess
class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves, "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.white_to_move = True
        self.move_log = []

    def get_piece(self, r, c):
        if 0 <= r < len(self.board):
            if 0 <= c < len(self.board[r]):
                return self.board[r][c]

        return "  "

    def make_move(self, move, ):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.moved_piece
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.moved_piece[1] == "P":
            print("moved a pawn")

    def get_legal_moves(self):
        moves = []
        for move in self.get_all_possible_moves():
            valid = True
            self.make_move(move)

            enemy_moves = self.get_all_possible_moves()
            for enemy_move in enemy_moves:
                if enemy_move.captured_piece[1] == "K":
                    valid = False
                    break
                    
            self.undo_move()

            if valid:
                moves.append(move)
            # else:
                # print("king is endangered, ", move.get_chess_notation())
        
        return moves

    def get_all_possible_moves(self):
        moves = []

        # Iterate the board, find all possible moves
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]

                if (piece_color == "w" and self.white_to_move) or (piece_color == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves) # call move function for the piece
        return moves

    def get_moves_in_direction(self, r, c, dir, moves):
        enemy_color = "b" if self.white_to_move else "w"
        i = 1
        location = (r + dir[0]*i, c + dir[1]*i)
        p = self.get_piece(location[0], location[1])

        while p == "--":
            moves.append(Move((r, c), location, self.board))
            i += 1
            location = (r + dir[0]*i, c + dir[1]*i)

            p = self.get_piece(location[0], location[1])
        
        if p[0] == enemy_color:
            moves.append(Move((r, c), location, self.board))

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:
            # white pawn patrol forward
            if self.get_piece(r-1, c) == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.get_piece(r-2, c) == "--":
                    moves.append(Move((r,c), (r-2,c), self.board))

            # white pawn capture
            if self.get_piece(r-1, c-1)[0] == "b":
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if self.get_piece(r-1, c+1)[0] == "b":
                moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            # black pawn patrol forward
            if self.get_piece(r+1, c) == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.get_piece(r+2, c) == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
                    
            # black pawn capture
            if self.get_piece(r+1, c-1)[0] == "w":
                moves.append(Move((r, c), (r+1, c-1), self.board))
            if self.get_piece(r+1, c+1)[0] == "w":
                moves.append(Move((r, c), (r+1, c+1), self.board))

    def get_rook_moves(self, r, c, moves):
        self.get_moves_in_direction(r, c, (1, 0), moves)
        self.get_moves_in_direction(r, c, (-1,0), moves)
        self.get_moves_in_direction(r, c, (0, 1), moves)
        self.get_moves_in_direction(r, c, (0,-1), moves)

    def get_knight_moves(self, r, c, moves):
        directions = ((2, -1), (2, 1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2))
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            p = self.get_piece(r + d[0], c + d[1])
            if p == "--" or p[0] == enemy_color:
                moves.append(Move((r, c), (r + d[0], c + d[1]), self.board))

    def get_bishop_moves(self, r, c, moves):
        self.get_moves_in_direction(r, c, (1,  1), moves)
        self.get_moves_in_direction(r, c, (-1, 1), moves)
        self.get_moves_in_direction(r, c, (-1,-1), moves)
        self.get_moves_in_direction(r, c, (1, -1), moves)

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        for i in range(r-1, r+1+1):
            for j in range(c-1, c+1+1):
                p = self.get_piece(i, j)
                if p == "--" or (p[0] == "b" and self.white_to_move) or (p[0] == "w" and not self.white_to_move):
                    moves.append(Move((r, c), (i, j), self.board))

    def undo_move(self):
        if len(self.move_log) != 0:
            last_move = self.move_log.pop()

            self.board[last_move.end_row][last_move.end_col] = last_move.captured_piece
            self.board[last_move.start_row][last_move.start_col] = last_move.moved_piece
            
            self.white_to_move = not self.white_to_move


class Move:
    # files = cols = x
    # ranks = rows = y
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.end_row][self.end_col]
        
        self.move_id = self.start_col * 1000 + self.start_row * 100 + self.end_col * 10 + self.end_row

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
