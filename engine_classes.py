class Pice():
    def __init__(self, position, value, name):
        self.position= position
        self.value = value
        self.team = int(value/abs(value)) # 1 if white 0 if black
        self.moves = None
        self.on_starting_position = True
        self.name = name
        
    def find_moves(self, board= None):
        pass

    def convert_moves_for_GUI(self):
        moves= []
        for move in self.moves:
            F, R = move
            GUI_move = F*8+R
            moves.append(GUI_move)
        return moves 

class Pawn(Pice):


    def find_moves(self, board= None):
        moves = []
        b_rank, b_file = self.position
        #print(b_file, "  ", b_rank)
        if self.on_starting_position:
            forward = [1, 2]
        else:
            forward = [1]
        for f in forward:
            if (b_rank - f*self.team) in range(0,8) and b_file in range(0,8) and board[b_rank - f*self.team][b_file] == None:
                moves.append([b_rank - f*self.team, b_file])

        for i in (-1, 1):
            if (b_rank - self.team) in range(0,8) and (b_file+ i) in range(0,8) and board[b_rank - self.team][b_file+ i] != None:
                if board[b_rank - self.team][b_file+ i].value*self.value < 0 :
                    moves.append([b_rank - self.team, b_file+i])
                    #print(0)

        self.moves= moves
        print(self.moves)

class Rook(Pice):
   
    def find_moves(self, board):
        moves = []
        b_rank, b_file = self.position
        
        for i in range(b_rank-1, -1, -1):
            if board[i][b_file] == None:
                moves.append([i, b_file])
            else:
                if board[i][b_file].value*self.value < 0:
                    moves.append([i, b_file])
                break
        
        for i in range(b_rank+1, 8):
            if board[i][b_file] == None:
                moves.append([i, b_file])
            else:
                if board[i][b_file].value*self.value < 0:
                    moves.append([i, b_file])
                break
            
        for i in range(b_file-1, -1, -1):
            if board[b_rank][i] == None:
                moves.append([b_rank, i])
            else:
                if board[b_rank][i].value*self.value < 0:
                    moves.append([b_rank, i])
                break
            
        for i in range(b_file+1, 8):
            if board[b_rank][i] == None:
                moves.append([b_rank, i])
            else:
                if board[b_rank][i].value*self.value < 0:
                    moves.append([b_rank, i])
                break

        self.moves= moves
    
class Knight(Pice):

   def find_moves(self, board):
        moves = []
        b_rank, b_file = self.position
        candidates = [[b_rank-2, b_file-1],
                      [b_rank-2, b_file+1],
                      [b_rank-1, b_file-2],
                      [b_rank-1, b_file+2],
                      [b_rank+1, b_file-2],
                      [b_rank+1, b_file+2],
                      [b_rank+2, b_file-1],
                      [b_rank+2, b_file+1],
                    ]
        candidates = [[row, column] for row, column in candidates if row in range(0,8) and column in range(0,8)]
        for j, i in candidates:
            if board[j][i] == None or board[j][i].value*self.value < 0:
                moves.append([j, i])
            

        self.moves= moves
class Bishop(Pice):
    
    def find_moves(self, board):
        moves = []
        b_rank, b_file = self.position

        for i in range(1, min(b_rank, b_file)+1):
            if board[b_rank-i][b_file-i] == None:
                moves.append([b_rank-i, b_file-i])
            else:
                if board[b_rank-i][b_file-i].value*self.value < 0:
                    moves.append([b_rank-i, b_file-i])
                break
        
        for i in range(1, min(b_rank, 7-b_file)+1):
            if board[b_rank-i][b_file+i] == None:
                moves.append([b_rank-i, b_file+i])
            else:
                if board[b_rank-i][b_file+i].value*self.value < 0:
                    moves.append([b_rank-i, b_file+i])
                break
            
        for i in range(1, min(7-b_rank,b_file)+1):
            if board[b_rank+i][b_file-i] == None:
                moves.append([b_rank+i, b_file-i])
            else:
                if board[b_rank+i][b_file-i].value*self.value < 0:
                    moves.append([b_rank+i, b_file-i])
                break
        
        for i in range(1, min(7-b_rank, 7-b_file)+1):
            if board[b_rank+i][b_file+i] == None:
                moves.append([b_rank+i, b_file+i])
            else:
                if board[b_rank+i][b_file+i].value*self.value < 0:
                    moves.append([b_rank+i, b_file+i])
                break
        
        self.moves= moves

class Queen(Pice):
    
    def find_moves(self, board=  None):
        
        moves = []
        b_rank, b_file = self.position
        
        for i in range(b_rank-1, -1, -1):
            if board[i][b_file] == None:
                moves.append([i, b_file])
            else:
                if board[i][b_file].value*self.value < 0:
                    moves.append([i, b_file])
                break
        
        for i in range(b_rank+1, 8):
            if board[i][b_file] == None:
                moves.append([i, b_file])
            else:
                if board[i][b_file].value*self.value < 0:
                    moves.append([i, b_file])
                break
            
        for i in range(b_file-1, -1, -1):
            if board[b_rank][i] == None:
                moves.append([b_rank, i])
            else:
                if board[b_rank][i].value*self.value < 0:
                    moves.append([b_rank, i])
                break
            
        for i in range(b_file+1, 8):
            if board[b_rank][i] == None:
                moves.append([b_rank, i])
            else:
                if board[b_rank][i].value*self.value < 0:
                    moves.append([b_rank, i])
                break

        for i in range(1, min(b_rank, b_file)+1):
            if board[b_rank-i][b_file-i] == None:
                moves.append([b_rank-i, b_file-i])
            else:
                if board[b_rank-i][b_file-i].value*self.value < 0:
                    moves.append([b_rank-i, b_file-i])
                break
        
        for i in range(1, min(b_rank, 7-b_file)+1):
            if board[b_rank-i][b_file+i] == None:
                moves.append([b_rank-i, b_file+i])
            else:
                if board[b_rank-i][b_file+i].value*self.value < 0:
                    moves.append([b_rank-i, b_file+i])
                break
            
        for i in range(1, min(7-b_rank,b_file)+1):
            if board[b_rank+i][b_file-i] == None:
                moves.append([b_rank+i, b_file-i])
            else:
                if board[b_rank+i][b_file-i].value*self.value < 0:
                    moves.append([b_rank+i, b_file-i])
                break
        
        for i in range(1, min(7-b_rank, 7-b_file)+1):
            if board[b_rank+i][b_file+i] == None:
                moves.append([b_rank+i, b_file+i])
            else:
                if board[b_rank+i][b_file+i].value*self.value < 0:
                    moves.append([b_rank+i, b_file+i])
                break
    
        self.moves= moves

class King(Pice):

    def find_moves(self, board):
        moves = []
        b_rank, b_file = self.position
        for i in range(max(0, b_file-1), min(7, b_file+1)+1):
            for j in range(max(0, b_rank-1), min(7, b_rank+1)+1):
                if board[j][i] == None or board[j][i].value*self.value < 0:
                    moves.append([j, i])
            

        self.moves= moves
