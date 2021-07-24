from copy import deepcopy
from GameBoard import GameBoard

class Evaluate:

    def __init__(self, board, pColor, eColor):
        
        self.board = board
        self.pColor = pColor 
        self.eColor = eColor
    

    def getAllPieces(self, board, color = 'both'):

        allBlackPieces = []
        allWhitePieces = []

        for i in range(8):
            for j in range(8):

                if board[i][j] == 'b' or board[i][j] == 'B':
                    allBlackPieces.append((i,j))

                if board[i][j] == 'w' or board[i][j] == 'W':
                    allWhitePieces.append((i,j))
        
        if color == 'b':
            return allBlackPieces
        if color == 'w':
            return allWhitePieces

        return allBlackPieces, allWhitePieces

    def get_pieces_count(self, board):

        black_pawns = []
        white_pawns = []
        black_kings = []
        white_kings = []
        white_back_row = 0
        black_back_row = 0
        white_middle_box = 0
        black_middle_box = 0
        white_middle_two_rows = 0
        black_middle_two_rows = 0
        white_protected_cnt = 0
        black_protected_cnt = 0
        white_vulnerable_cnt = 0
        black_vulnerable_cnt = 0
        white_adv_pawn_count = 0
        black_adv_pawn_count = 0
        white_safe_piece_count = 0
        black_safe_piece_count = 0


        for i in range(8):
            for j in range(8):

                if board[i][j] == 'b':
                    black_pawns.append((i, j))
                
                elif board[i][j] == 'B':
                    black_kings.append((i, j))

                elif board[i][j] == 'w':
                    white_pawns.append((i, j))

                elif board[i][j] == 'W':
                    white_kings.append((i, j))

        for piece in black_pawns + black_kings:
            
            x, y = piece
            
            if x == 0:
                black_back_row += 1
            
            if 3 <= x <= 4 and 3 <= y <= 4:
                black_middle_box += 1
            
            if 3 <= x <= 4:
                black_middle_two_rows += 1

            if x > 2:
                black_adv_pawn_count += 1
            
            if y == 0 or y == 7:
                black_safe_piece_count += 1
            
            if ((x - 1, y - 1) in black_kings + black_pawns) or ((x - 1, y + 1) in black_kings + black_pawns):
                black_protected_cnt += 1
            
            if x != 0 and x != 7 and y != 0 and y != 7:
                if (x + 1, y - 1) in white_kings + white_pawns or (x + 1, y + 1) in white_kings + white_pawns or ((x - 1, y - 1) in white_kings or (x - 1, y + 1) in white_kings):
                    black_vulnerable_cnt += 1
        
        for piece in white_pawns + white_kings:
            
            x, y = piece
            
            if x == 7:
                white_back_row += 1
            
            if 3 <= x <= 4 and 3 <= y <= 4:
                white_middle_box += 1
            
            if 3 <= x <= 4:
                white_middle_two_rows += 1

            if x < 4:
                white_adv_pawn_count += 1
            
            if y == 0 or y == 7:
                white_safe_piece_count += 1
            
            if (x + 1, y - 1) in white_kings + white_pawns or (x + 1, y + 1) in white_kings + white_pawns:
                white_protected_cnt += 1
            
            if x != 0 and x != 7 and y != 0 and y != 7:
                if (x - 1, y - 1) in black_kings + black_pawns or (x - 1, y + 1) in black_kings + black_pawns or ((x + 1, y - 1) in black_kings or (x + 1, y + 1) in black_kings):
                    white_vulnerable_cnt += 1

        return (len(black_pawns), len(white_pawns)), (len(black_kings), len(white_kings)), (black_back_row, white_back_row), (black_middle_box, white_middle_box), (black_middle_two_rows, white_middle_two_rows), (black_protected_cnt, white_protected_cnt), (black_vulnerable_cnt, white_vulnerable_cnt), (black_adv_pawn_count, white_adv_pawn_count), (black_safe_piece_count, white_safe_piece_count)

    
    def any_winner(self, board):
        
        all_black_pieces, all_white_pieces = self.getAllPieces(board)
        
        if len(all_black_pieces) == 0 or len(all_white_pieces) == 0:
            return True 
        
        return False 
        
        
    def get_all_moves(self, board, color):
        
        gameboard = GameBoard(board)
        any_jump_moves = False
        all_pieces = self.getAllPieces(board, color)
        
        jump_moves = []
        positional_moves = []

        for piece in all_pieces:
            j, p = gameboard.allValidMoves(piece)

            if j != []:
                for ele in j:
                    jump_moves.append((piece, ele))
            
            elif p != []:
                for ele in p:
                    positional_moves.append((piece, ele))
        
        return jump_moves, positional_moves


    def alphabeta(self, board, depth, max_player, alpha = float('-inf'), beta = float('inf')):

        if depth == 0 or self.any_winner(board): 
            return self.evaluate(board), board
        
        if max_player:
            
            maxEval = float('-inf')
            best_move = None
            jump_moves, positional_moves = self.get_all_moves(board, self.pColor)
            jumped = False
            
            if len(jump_moves) > 0:
                all_moves = jump_moves
                jumped = True
            else:
                all_moves = positional_moves
            
            for move in all_moves:

                piece, temp = move
                target, skips = temp
                possible_board = self.movepiece(deepcopy(board), piece, target, skips, jumped)
                evaluation = self.alphabeta(possible_board, depth-1, False, alpha, beta)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move
                
                alpha = max(alpha, maxEval)

                if beta <= alpha:
                    return maxEval, best_move
            
            return maxEval, best_move
        
        else:

            minEval = float('inf')
            best_move = None
            jump_moves, positional_moves = self.get_all_moves(board, self.eColor)
            jumped = False
            
            if len(jump_moves) > 0:
                all_moves = jump_moves
                jumped = True
            else:
                all_moves = positional_moves

            for move in all_moves:

                piece, temp = move
                target, skips = temp
                possible_board = self.movepiece(deepcopy(board), piece, target, skips, jumped)
                evaluation = self.alphabeta(possible_board, depth-1, True, alpha, beta)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move
                
                beta = min(beta, minEval)

                if beta <= alpha:
                    return minEval, best_move
                
            return minEval, best_move

        
    def movepiece(self, board, piece, target, skips, jumped):
        
        cx, cy = piece
        tx, ty = target
        temp = board[cx][cy]
        board[cx][cy] = '.'
        if jumped:
            for ele in skips:
                sx, sy = ele
                board[sx][sy] = '.'

        if temp == 'w' and tx == 0:
            temp = 'W'

        if temp == 'b' and tx == 7:
            temp = 'B'    

        board[tx][ty] = temp
    
        return board

    
    def evaluate(self, board):
        
        num_pawns, num_kings, back_row, middle_box, middle_two_row, protected_count, vulnerable_count, advanced_pawn_count, safe_piece_count = self.get_pieces_count(board)

        if num_pawns[0] + num_kings[0] > 0:
            black_agg_adv_pawn = (advanced_pawn_count[0]/(num_kings[0] + num_pawns[0]))
            black_agg_safe_cnt = (safe_piece_count[0] / (num_kings[0] + num_pawns[0]))
        else:
            black_agg_adv_pawn = 0
            black_agg_safe_cnt = 0

        if num_pawns[1] + num_kings[1] > 0:
            white_agg_adv_pawn = (advanced_pawn_count[1]/(num_kings[1] + num_pawns[1]))
            white_agg_safe_cnt = (safe_piece_count[1] / (num_kings[1] + num_pawns[1]))
        else:
            white_agg_adv_pawn = 0
            white_agg_safe_cnt = 0

        black_eval = (4.98 * num_pawns[0]) + (8.3 * num_kings[0]) + (2.1 * back_row[0]) + (0.48 * middle_two_row[0]) + (0.88 * middle_box[0]) + (-1.06 * vulnerable_count[0]) + (1.06 * protected_count[0]) + (0 * black_agg_adv_pawn) + (0 * black_agg_safe_cnt)
        white_eval = (4.98 * num_pawns[1]) + (8.3 * num_kings[1]) + (2.1 * back_row[1]) + (0.48 * middle_two_row[1]) + (0.88 * middle_box[1]) + (-1.06 * vulnerable_count[1]) + (1.06 * protected_count[1]) + (0 * white_agg_adv_pawn) + (0 * white_agg_safe_cnt)

        if num_pawns[0] + num_kings[0] == 0:
            white_eval = float('inf')
        if num_pawns[1] + num_kings[1] == 0:
            black_eval = float('inf')

        if self.pColor == 'w':
            return white_eval - black_eval
        else:
            return black_eval - white_eval    
    
