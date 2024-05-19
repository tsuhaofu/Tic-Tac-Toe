# Tic-Tac-Toe

The environment is an n×n grid, the rules are that you may place a piece on any unoccupied square, and the goal is to get k of your pieces in a row.
Cmd line instructions: python ttt.py n k [x] or python ttt.py n k [o]  - if x, my ai go first, if o my ai go second.
It will automically create, write my moves into xmoves.txt or omoves.txt(seperated by \n).
Also, read the opponent's moves from xmoves.txt or omoves.txt. As long as all the codes and txt files are stored in the same folder.
You can use play_game() function to play against itself,  

play_game_txt() to play with a opponent, 
play_game_heuristic() to play against itself by alternative strategy, 
play_game_txt_heuristic() to play with a opponent by alternative strategy
