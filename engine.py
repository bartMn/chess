import copy
import engine_classes

EMPTY = None

PAWN = 1
ROOK = 5
KNIGHT = 3
BISHOP = 3
QUEEN = 9
KING = 100


class game():
    def __init__(self):  
        self.moves_made = []
        self.board = [[EMPTY for i in range(8)] for _ in range(8)]
        self.black_army = []
        self.white_army = []

    def create_a_pice(self, pice, color, gui_position):
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
            self.white_army.append(new_pice)
        else:
            self.black_army.append(new_pice)
        self.board[position[0]][position[1]] = new_pice

        return new_pice

    def move_a_pice(self, pice, new_position, previous_position):
        
        if self.board[int(new_position/8)][new_position- int(new_position/8)*8]:
            if pice.color == "black":
                self.white_army.remove(self.board[int(new_position/8)][new_position- int(new_position/8)*8])
            else:
                self.black_army.remove(self.board[int(new_position/8)][new_position- int(new_position/8)*8])
            #print("kill")
    
        self.board[int(previous_position/8)][previous_position- int(previous_position/8)*8]= None
        self.board[int(new_position/8)][new_position- int(new_position/8)*8]= pice.pice_type
        pice.pice_type.position  = [int(new_position/8), new_position- int(new_position/8)*8]
        pice.pice_type.on_starting_position = False

        if pice.pice_type.name == "pawn":
            if pice.pice_type.team == 1 and pice.pice_type.position[0] == 0:
                self.promote_a_pawn(pice)
                return True
                #print("promote white pawn")
            elif pice.pice_type.team == -1 and pice.pice_type.position[0] == 7:
                #print("promote black pawn")
                self.promote_a_pawn(pice)
                return True
        return False

    def promote_a_pawn(self, pice):
        if pice.color == "black":
            self.black_army.remove(self.board[int(pice.sqare_id/8)][pice.sqare_id- int(pice.sqare_id/8)*8])
        else:
            self.white_army.remove(self.board[int(pice.sqare_id/8)][pice.sqare_id- int(pice.sqare_id/8)*8])
            #print("kill")
    
        self.board[int(pice.sqare_id/8)][pice.sqare_id- int(pice.sqare_id/8)*8]= None
        promoted_pawn = self.create_a_pice("queen", pice.color, pice.sqare_id)
        promoted_pawn.on_starting_position = False
        #print(self.board)
        #print()
        #print()
        #print(self.white_army)
        
        

    def player(self, Moves):
        """
        Returns player who has the next turn on a board.
        """
        return "black" if len(Moves)%2 == 1 else "wite"

    def actions(self, board):
        """
        Returns set of all possible actions (pice, move) available on the board.
        """
        pass

    def result(self, board, action):
        """
        Returns the board that results from making move (pice, move) on the board.
        """
        pass


    def winner(self, board):
        """
        Returns the winner of the game, if there is one.
        """
        pass
    def terminal(self, board):
        """
        Returns True if game is over, False otherwise.
        """
        pass


    def utility(self, board):
        """
        Returns 1 if white has won the game, -1 if blabk has won, 0 otherwise.
        """
        pass

    def MAX(self, board):
        pass

    def MIN(self, board):
       pass
    def minimax(self, board):
        """
        Returns the optimal action for the current player on the board.
        """
        pass