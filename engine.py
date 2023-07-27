import copy
import engine_classes


EMPTY = None

PAWN = 1
ROOK = 5
KNIGHT = 3
BISHOP = 3
QUEEN = 9
KING = 0.01


class game():
    def __init__(self):  
        self.moves_made = []
        self.board = [[EMPTY for i in range(8)] for _ in range(8)]
        self.black_army = []
        self.white_army = []
        self.squares_attacked_by_white = list()
        self.squares_attacked_by_black = list()
        self.team_to_make_a_move = 1
        self.white_king = None
        self.black_king = None
        self.Moves = 0

    def create_a_pice(self,
                      pice,
                      color,
                      gui_position,
                      white_army, 
                      white_king,
                      black_army,
                      black_king,
                      board):
        
        if color == "white":
            team = 1
        else:
            team = -1

        creator_dict=  {"pawn": engine_classes.Pawn,
                        "rook": engine_classes.Rook,
                        "knight": engine_classes.Knight,
                        "bishop": engine_classes.Bishop,
                        "queen": engine_classes.Queen,
                        "king": engine_classes.King
                        }

        position = [int(gui_position/8), gui_position- int(gui_position/8)*8]
        value = globals()[pice.upper()]
        new_pice= creator_dict[pice](position, value*team, pice)
        #new_pice = globals()[f"engine_classes.{pice.capitalize()}"](position, value*team)
        #new_pice = engine_classes.Pawn([1,2], 1*team)
        #new_pice = engine_classes.Rook(position, value*team)
        if color == "white":
            white_army.append(new_pice)
            if pice == "king":
                self.white_king = new_pice
        else:
            black_army.append(new_pice)
            if pice == "king":
                self.black_king = new_pice
        board[position[0]][position[1]] = new_pice
        
        return new_pice

    def move_a_pice(self, pice, new_position, board):
        
        white_army, black_army, white_king, black_king = self.get_pices_from_a_board(board)
        
        
        to_return = False
        #print(new_position)
        if len(new_position) > 2:
            #print("castling")
            king_r, king_f, rook_r, rook_f = new_position
            self.move_a_pice(pice, [king_r, king_f], board)
            rook_starting_file = 0 if rook_f < 4 else 7
            self.move_a_pice(board[king_r][rook_starting_file], [rook_r, rook_f], board)
        
        else:
            new_b_rank, new_b_file = new_position

            if board[new_b_rank][new_b_file]:
                if pice.value < 0:
                    white_army.remove(board[new_b_rank][new_b_file])
                else:
                    black_army.remove(board[new_b_rank][new_b_file])
                #print("kill")
            b_rank, b_file = pice.position
            board[b_rank][b_file]= None
            board[new_b_rank][new_b_file]= pice
            pice.position  = [new_b_rank, new_b_file]
            pice.on_starting_position = False

            if pice.name == "pawn":
                if pice.team == 1 and pice.position[0] == 0:
                    self.promote_a_pawn(pice, board)
                    to_return = True
                    #print("promote white pawn")
                elif pice.team == -1 and pice.position[0] == 7:
                    #print("promote black pawn")
                    self.promote_a_pawn(pice, board)
                    to_return = True
            #return False
        
        self.Moves += 1
        return to_return
        
    def move_a_pice_for_analysys(self,
                                 pice,
                                 new_position,
                                 board,
                                 moves):
        
        white_army, black_army, white_king, black_king = self.get_pices_from_a_board(board)
        
        to_return = False
        #print(new_position)
        if len(new_position) > 2:
            #print("castling")
            king_r, king_f, rook_r, rook_f = new_position
            self.move_a_pice_for_analysys(pice,
                                          [king_r, king_f],
                                          board,
                                          moves)
            
            rook_starting_file = 0 if rook_f < 4 else 7
            self.move_a_pice_for_analysys(board[king_r][rook_starting_file],
                                          [rook_r, rook_f],
                                          board,
                                          moves)
        
        else:
            new_b_rank, new_b_file = new_position
            
            if board[new_b_rank][new_b_file]:
                if pice.value < 0:
                    white_army.remove(board[new_b_rank][new_b_file])
                else:
                    black_army.remove(board[new_b_rank][new_b_file])
                #print("kill")
            b_rank, b_file = pice.position
            board[b_rank][b_file]= None
            board[new_b_rank][new_b_file]= pice
            pice.position  = [new_b_rank, new_b_file]
            pice.on_starting_position = False

            if pice.name == "pawn":
                if pice.team == 1 and pice.position[0] == 0:
                    self.promote_a_pawn(pice, board)
                    to_return = True
                    #print("promote white pawn")
                elif pice.team == -1 and pice.position[0] == 7:
                    #print("promote black pawn")
                    self.promote_a_pawn(pice, board)
                    to_return = True
            #return False
        
        
        friendly_king_is_attacked = self.check_if_king_is_attacked(board, moves) #checking if enemy king is attacked
      
        return not friendly_king_is_attacked
    


    def promote_a_pawn(self, pice, board):
        
        white_army, black_army, white_king, black_king = self.get_pices_from_a_board(board)
        
        if pice.value < 0:
            black_army.remove(board[pice.position[0]][pice.position[1]])
        else:
            white_army.remove(board[pice.position[0]][pice.position[1]])
            #print("kill")
    
        board[pice.position[0]][pice.position[1]]= None
        color = "black" if pice.value < 0 else "white"
        promoted_pawn = self.create_a_pice(pice = "queen",
                                           color = color,
                                           gui_position = pice.position[0]*8 + pice.position[1],
                                           white_army = white_army, 
                                           white_king = white_king,
                                           black_army = black_army,
                                           black_king = black_king,
                                           board = board
                                           )   
        promoted_pawn.on_starting_position = False
        #print(self.board)
        #print()
        #print()
        #print(self.white_army)
        
        
    def look_for_legal_moves(self, original_board, moves):
        
        team_to_move = self.player(moves)
        #print(f"team to move: {team_to_move}")
        legal_moves = list()
        
        original_white_army, original_black_army, original_white_king, original_black_king = self.get_pices_from_a_board(original_board)
        
        if team_to_move== 1: #white to make a move
            
            for original_white_pice in original_white_army:
                for move in original_white_pice.find_moves(original_board):
                    
                    white_army, black_army, white_king, black_king, board = self.copy_pices_and_board(original_board)
                    
                    white_pice = None
                    for pice in white_army:
                        if pice.position == original_white_pice.position:
                            white_pice = pice
                            break
                    
                    move_is_legal = self.move_a_pice_for_analysys(pice = white_pice,
                                                                  new_position = move,
                                                                  board =      board,
                                                                  moves = moves)
                    if move_is_legal:
                        legal_moves.append([original_white_pice, move])
                        #print(f"legal move found for white: {original_white_pice.name} -> {move}")
                        
        else:
            for original_black_pice in original_black_army:
                for move in original_black_pice.find_moves(original_board):
                    
                    white_army, black_army, white_king, black_king, board = self.copy_pices_and_board(original_board)
                            
                    black_pice = None
                    for pice in black_army:
                        if pice.position == original_black_pice.position:
                            black_pice = pice
                            break
                    
                    move_is_legal = self.move_a_pice_for_analysys(pice = black_pice,
                                                                  new_position = move,
                                                                  board =      board,
                                                                  moves= moves)
                    if move_is_legal:
                        legal_moves.append([original_black_pice, move])
                        #print(f"legal move found for black: {original_black_pice.name} -> {move}")
        #print(len(legal_moves))
        
        return legal_moves
        
        
    def check_if_king_is_attacked(self, board, moves):
        
        white_army, black_army, white_king, black_king = self.get_pices_from_a_board(board)
        
        #if white is to make a move
        
        if self.player(moves) == 1: #checking if the white king is attacked 
            squares_attacked_by_black = list()
            for black_pice in black_army: #taking one pice from the whole army
                for square_attacked in black_pice.find_moves(board): #finding which squares the pice attacks
                    squares_attacked_by_black.append(square_attacked)
            if white_king.position in squares_attacked_by_black:
                #print("white king is under attack!!!!!!!!!!!!")
                return True
            
                
        else: #blacks makes a move and checking if black king is attacked        
            squares_attacked_by_white = list()
            for white_pice in white_army:
                for square_attacked in white_pice.find_moves(board):
                    squares_attacked_by_white.append(square_attacked)
            if black_king.position in squares_attacked_by_white:
                #print("black king is under attack!!!!!!!!!!!!")
                return True
                
        return False
    
    def return_legal_moves_for_a_pice(self, pice, board, moves):

        legal_moves_for_pice = list()
        legal_moves = self.return_legal_moves(board, moves)
        for pice_legal, move_legal in legal_moves:
            if pice == pice_legal:
                legal_moves_for_pice.append(move_legal)
                
        return legal_moves_for_pice
        
    
    def return_legal_moves(self, board, moves):
        
        return self.look_for_legal_moves(original_board = board, moves = self.Moves)
    
    
    def copy_pices_and_board(self, original_board):
        
        
        board_copy = copy.deepcopy(original_board)
        white_army_copy, black_army_copy, white_king_copy, black_king_copy = self.get_pices_from_a_board(board_copy)
        
                 
        return white_army_copy, black_army_copy, white_king_copy, black_king_copy, board_copy
    
    def get_pices_from_a_board(self, board):
        
        white_army = list()
        black_army = list()
        
        for i in range(8):
            for j in range(8):
                
                if not board[i][j]:
                    continue
                
                elif board[i][j].team == 1:
                    white_army.append(board[i][j])
                    if board[i][j].name == "king":
                        white_king = board[i][j]
                        
                elif board[i][j].team == -1:
                    black_army.append(board[i][j])
                    if board[i][j].name == "king":
                        black_king = board[i][j] 
        
        return white_army, black_army, white_king, black_king
    
    def compare_armies(self, board):
        
        all_pices = list()
        white_army, black_army, white_king, black_king = self.get_pices_from_a_board(board)
        
        all_pices = white_army + black_army
        
        pices_balance = 0 #value used to compare who has more material
        for pice in all_pices:
            pices_balance += pice.value
            
        return pices_balance
        
    
    def player(self, Moves):
        """
        Returns player who has the next turn on a board.
        """
        return -1 if Moves % 2 == 1 else 1

    def actions(self, board, moves):
        """
        Returns set of all possible actions (pice, move) available on the board.
        """
        return self.look_for_legal_moves(original_board = board, moves = moves)

    def result(self, board, action):
        """
        Returns the board that results from taking action (pice, move) on the board.
        """
        pice, new_position = action 
        
        white_army_copy, black_army_copy, white_king_copy, black_king_copy, board_copy = self.copy_pices_and_board(board)
        pice_copy = board_copy[pice.position[0]][pice.position[1]]
        self.Moves -= 1
        self.move_a_pice(pice_copy, new_position, board_copy)
        
        
        return board_copy


    def winner(self, board, moves):
        """
        Returns the winner of the game, if there is one.
        """
        
        if self.terminal(board, moves): #no legal moves for the current player
            if self.check_if_king_is_attacked(board, moves): #checking if game ended by a checkmate
                if self.player(moves) == -1: #it is now black's move
                    return 1 #white won
                else: #it is now white's move
                    return -1 #black won

        return 0 #stalemate or game in progress
    
    
    
    def terminal(self, board, moves):
        """
        Returns True if game is over, False otherwise.
        """
        if len(self.actions(board, moves)) == 0:
            return True
        
        return False 


    def utility(self, board, moves):
        """
        Returns 1 if white has won the game, -1 if black has won, 0 otherwise.
        """
        if self.winner(board, moves)== 1: #white won
            return 10000
        elif self.winner(board, moves)== -1: #black won
            return -10000
        else:#self.winner(board, moves)== 0: #stalemate or game in progress
            return 0
        

    def MAX(self, board, moves, depth_max, depth_current_depth):
        
        
        if self.terminal(board, moves):
        #print("terminal is reached"+ str(utility(board)))
            return ((self.utility(board, moves), None))
        
        #if depth_max:
        if depth_current_depth >= depth_max:
            return ((self.compare_armies(board), None))
        
        v_max = -20000    
        for action in self.actions(board, moves):
            new_board = self.result(board, action)
            v= self.MIN(
                    new_board,
                    moves + 1,
                    depth_max,
                    depth_current_depth + 1
                   )[0]
            del new_board
            
            if v== 10000:
                return (v, action)
            if v>v_max:
                v_max= v
                act= action
        return ((v_max, act))

    def MIN(self, board, moves, depth_max, depth_current_depth):
        
        
        
        if self.terminal(board, moves):
        #print("terminal is reached"+ str(utility(board)))
            return ((self.utility(board, moves), None))
        
        #if depth_max:
        if depth_current_depth >= depth_max:
            return ((self.compare_armies(board), None))
        
        v_min = 20000
        for action in self.actions(board, moves):
            new_board = self.result(board, action)
            v= self.MAX(
                    new_board,
                    moves + 1,
                    depth_max,
                    depth_current_depth + 1
                   )[0]
            del new_board
            
            if v== -10000:
               return (v, action)
            if v_min>v:
                v_min= v
                act= action
        return ((v_min, act))
   
    def minimax(self, board, moves, depth_max= 1, depth_current_depth= 0):
        """
        Returns the optimal action for the current player on the board.
        """
        if self.player(moves)== 1: #white moves and we want to maximise a score
            #print(self.MAX(board, moves, depth_max, depth_current_depth)[1])
            #print(f"AI white move: {self.MAX(board, moves, depth_max, depth_current_depth)[1]}")
            return self.MAX(board, moves, depth_max, depth_current_depth)[1]
        elif self.player(moves)== -1: #black moves and we want to minimise a score
            #print(f"AI black move: {self.MIN(board, moves, depth_max, depth_current_depth)[1]}")
            return self.MIN(board, moves, depth_max, depth_current_depth)[1]
