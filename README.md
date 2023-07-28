The project is currently under development.
Most of the chess rules have been implemented. There is a possipility to play against an AI player but the quiality of the moves played is very low. Moreover, it takes quite a lot of time to calculate which move should be made.
It is planned to imlement the missing chess rule (en passant), optimise the minimax player and try different methods for an AI player and compare there performances.


Updates done to the project:
1. castling (both sides and checking if castling is legal, i.e. kink is not attacked and squares between the king and a rook are not attacked)
2. checks and checkmate (the checkmate is when a team has no legal moves and king is attacked)
3. stalemate (when there are no legal moves and king is not attacked)
4. AI/minimax player (currently the depth is set to 2 and it is very slow (about 25 seconds for a move))


To do:
1. Optimize minimax to enable increasing the depth (in theory depth can be increased but it will take a lot of time for the AI player to make a move)
2. Show the common openings to the AI/minimax to follow them to not waste a time for calculations for the first moves
3. Implement the en passant move
4. Add a choice for a pawn promotion instead of promoting to a queen
5. Try implementing different methods for an AI player
6. Add a draw when:
   neither player has material to checkmate
   there is a repetition (one position occours 3 times)
   there were 50 moves with no pawn or no capture
7. Add comments in the code and remove redundant lines


Requirements:
1. everyting that is in the branch
2. pygame (python library)
3. cv2 (python library)
4. numpy (python library)
5. copy (python library)
