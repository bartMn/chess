import pygame
import temporary_pices
import os
import classes
import engine
import time

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_WIDTH = 700

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)
pygame.init()

RED = (237, 92, 103)
DARK_RED = (233, 56, 69)
BLUE = (66, 86, 113)
GREEN = (89, 179, 0)
DARK_GREEN = (78, 155, 0)

# set the pygame window name
pygame.display.set_caption('chess_BM')

all_sprites = pygame.sprite.Group()
all_squares = pygame.sprite.Group()
all_pices =  pygame.sprite.Group()
black_pices =  pygame.sprite.Group()
white_pices =  pygame.sprite.Group()
squares_cliced = pygame.sprite.Group()
occupied_squares = pygame.sprite.Group()
pices_clicked = pygame.sprite.Group()
extras =  pygame.sprite.Group()

board_sqares= dict()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_board(bottom):
    
    rank = 56
    file_num = 97
    change= 1
    square_ID= 0
    if bottom == "black":
        change *= -1
        rank -= 7
        file_num += 7 
        square_ID= 63
        
    black= False
    
    for i in range(8):
        for j in range(8):
            new_square= classes.Square((black, None), BOARD_WIDTH/8, j*BOARD_WIDTH/8, i*BOARD_WIDTH/8, square_ID)
            board_sqares[square_ID]= new_square
            if j != 7:
                black =  not black
                if j == 0:
                    new_extra = classes.Coordinates((0,0), square_ID, chr(rank), new_square.color)
                    extras.add(new_extra)
                    rank -= change
                    
            if i == 7:
                new_extra = classes.Coordinates((new_square.size-20, new_square.size-20), square_ID, chr(file_num), new_square.color)
                extras.add(new_extra)
                file_num += change
            all_sprites.add(new_square)
            all_squares.add(new_square)
            square_ID += change 

def create_pices(FEN_input, path_to_read_pices, Game):
    placement= FEN_input.replace('/', '') 
    sqare_id= 0
    pices_dict = {
                    ord('p'): "pawn",
                    ord('r'): "rook",
                    ord('n'): "knight",
                    ord('b'): "bishop",
                    ord('q'): "queen",
                    ord('k'): "king"
                }

    for char in placement:
        if ord(char) >=49 and ord(char) <= 57:
            sqare_id += (ord(char) - 48)
        else:
    
            if ord(char) >=97 and ord(char) <= 122:
                color = "black"
                creator_key= ord(char)
            else:
                color = "white"
                creator_key= ord(char) + 32

            #p= globals()[pices_dict[creator_key]](color, path_to_read_pices, sqare_id)
            eng_pice = Game.create_a_pice(pice = pices_dict[creator_key],
                                          color = color,
                                          gui_position = sqare_id,
                                          white_army = Game.white_army, 
                                          white_king = Game.white_king,
                                          black_army = Game.black_army,
                                          black_king = Game.black_king,
                                          board = Game.board 
                                          )
            #print(eng_pice)
            p= classes.Pice(color, path_to_read_pices, sqare_id, pices_dict[creator_key], eng_pice)
            board_sqares[sqare_id].occupied_by = p
            occupied_squares.add(board_sqares[sqare_id])
            sqare_id += 1
            all_pices.add(p)
            all_sprites.add(p)
            globals()[f"{color}_pices"].add(p)

        
def move_a_pice(pice, new_position):
    #print(len(occupied_squares))
    occupied_squares.remove(board_sqares[pice.sqare_id])
    #print(len(occupied_squares))
    if board_sqares[new_position] in occupied_squares:
        board_sqares[new_position].occupied_by.kill()
    pice.make_a_move(new_position)
    occupied_squares.add(board_sqares[new_position])
    board_sqares[new_position].occupied_by = pice
    #print(len(Game.white_army))


def promote_a_pawn(pawn, path, eng_obj):

    p= classes.Pice(pawn.color, path, pawn.sqare_id, "queen", eng_obj)
    board_sqares[pawn.sqare_id].occupied_by = p
    all_pices.add(p)
    all_sprites.add(p)
    globals()[f"{pawn.color}_pices"].add(p)
    pawn.kill()

def main():
    Game= engine.game()
    path_to_read_pices= os.path.abspath(os.getcwd())+ os.sep + "pices" + os.sep + "temp"
    starting_position= "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    temporary_pices.create_pices(BOARD_WIDTH/8)
    
    running= True
    clicked_pice = None
    clock = pygame.time.Clock()

    draw_board("white")
    create_pices(starting_position, path_to_read_pices, Game)
    
    Players = {1: "white", -1: "black"}
    player_key = 1
    Player = Players[player_key]
    ai_turn = False
    
    while running:
        
        if ai_turn:
            
            action = Game.minimax(board=Game.board, moves=Game.Moves, depth_max= 2, depth_current_depth= 0)
            pice, move = action
            
            #board = Game.result(board, move)
            ai_turn = False
            R, F = move[0], move[1]
            gui_move = R*8+F
            
            clicked_pice = None
            R_current, F_current = pice.position[0], pice.position[1]
            gui_current_position = R_current*8+F_current
            for p in all_pices:
                if p.sqare_id == gui_current_position:
                    clicked_pice = p
                    
            if len(move)> 2:
                R, F = move[2], move[3]
                gui_move_1 = R*8+F
                if move[1]> 4:
                    pos_f = 7
                else:
                    pos_f = 0
                pos_r = int(clicked_pice.sqare_id/8)
                gui_id = pos_r*8+ pos_f
                move_a_pice(board_sqares[gui_id].occupied_by, gui_move_1)
                board_sqares[gui_current_position].change_color(squares_cliced, BLUE)
                
            move_a_pice(clicked_pice, gui_move)
            board_sqares[gui_current_position].change_color(squares_cliced, BLUE)
                
            if Game.move_a_pice(clicked_pice.pice_type,
                                move, Game.board):
                temp = Game.board[int(clicked_pice.sqare_id/8)][clicked_pice.sqare_id- int(clicked_pice.sqare_id/8)*8]
                promote_a_pawn(clicked_pice, path_to_read_pices, temp)
            
            player_key *= -1
            clicked_pice = None 
            
                    
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                left_button, _, right_button = pygame.mouse.get_pressed()
                position = pygame.mouse.get_pos()
                if right_button:
                    
                    for square in all_squares:
                        test = True if square.occupied_by != clicked_pice or clicked_pice == None else False
                        if square.rect.collidepoint(position) and test:
                            if square.color == (153, 76, 0):
                                square.change_color(squares_cliced, DARK_GREEN)
                            else:
                                square.change_color(squares_cliced, GREEN)
                            break

                if left_button:
                    for sq in squares_cliced:
                        sq.change_color(squares_cliced)
                    squares_cliced.empty()
                    
                        #break
                    #print(clicked_pice)
                    if clicked_pice:
                        #print("1231231")
                        for move in Game.return_legal_moves_for_a_pice(clicked_pice.pice_type, Game.board, Game.Moves):
                            #print(move)
                            R, F = move[0], move[1]
                            gui_move = R*8+F
                            
                            #gui_move = clicked_pice.pice_type.convert_moves_for_GUI(move[:2])
                            if board_sqares[gui_move].rect.collidepoint(position):
                                previous_position = clicked_pice.sqare_id
                                
                                if len(move)> 2:
                                    R, F = move[2], move[3]
                                    gui_move_1 = R*8+F
                                    if move[1]> 4:
                                        pos_f = 7
                                    else:
                                        pos_f = 0
                                    pos_r = int(clicked_pice.sqare_id/8)
                                    gui_id = pos_r*8+ pos_f
                                    move_a_pice(board_sqares[gui_id].occupied_by, gui_move_1)
                                    board_sqares[gui_id].change_color(squares_cliced)
                                move_a_pice(clicked_pice, gui_move)
                                
                                    
                                if Game.move_a_pice(clicked_pice.pice_type,
                                                    move, Game.board):
                                    temp = Game.board[int(clicked_pice.sqare_id/8)][clicked_pice.sqare_id- int(clicked_pice.sqare_id/8)*8]
                                    promote_a_pawn(clicked_pice, path_to_read_pices, temp)
                                
                                clicked_pice= None
                                ai_turn = True
                                player_key *= -1
                            #break
                    pice_hit = False
                    for sq_wp in occupied_squares: 
                        if sq_wp.rect.collidepoint(position):
                            clicked_pice = sq_wp.occupied_by
                            pice_hit = True
                            Player = Players[player_key]
                            if clicked_pice in globals()[f"{Player}_pices"]:
                                #print('pice pressed')
                                sq_wp.change_color(squares_cliced, BLUE)
                                #print(sq_wp.occupied_by.pm(Game.board))
                                for move in Game.return_legal_moves_for_a_pice(sq_wp.occupied_by.pice_type, Game.board, Game.Moves):
                                #sq_wp.occupied_by.pice_type.find_moves(Game.board):
                                    move = sq_wp.occupied_by.pice_type.convert_moves_for_GUI(move)
                                    #if move not in Game.return_legal_moves():
                                    #    continue
                                    if board_sqares[move].color == (153, 76, 0):
                                        board_sqares[move].change_color(squares_cliced, DARK_RED)
                                    else:
                                        board_sqares[move].change_color(squares_cliced, RED)
                                        
                            else:
                                clicked_pice = None
                    if not pice_hit:
                        clicked_pice = None
                        #else:
                        #    clicked_pice = None     
        
        for square in all_squares:
            screen.blit(square.surf, square.rect)

        for sq in squares_cliced:
            board_sqares[sq.ID].surf.blit(sq.surf, sq.rect)

        for pice in all_pices:
            board_sqares[pice.sqare_id].surf.blit(pice.surf, pice.rect)

        for e in extras:
            board_sqares[e.ID].surf.blit(e.text, e.location)

        pygame.display.flip()
        #clock.tick(30)

    temporary_pices.delete_all_images()

if __name__ == "__main__":
    # execute only if run as a script
    main()
