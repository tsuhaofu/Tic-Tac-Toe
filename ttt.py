#!/usr/bin/env python
# coding: utf-8

# In[123]:


from random import choice
from math import inf
import time
import sys
from statistics import mean

"""

Cmd line instructions: python ttt.py n k [x] or python ttt.py n k [o]  - if x, my ai go first, if o my ai go second.
It will automically create, write my moves into xmoves.txt or omoves.txt(seperated by \n).
Also, read the opponent's moves from xmoves.txt or omoves.txt.
As long as all the codes and txt files are stored in the same folder.
You can use play_game() function to play against itself,  
play_game_txt() to play with a opponent, 
play_game_heuristic() to play against itself by alternative strategy, 
play_game_txt_heuristic() to play with a opponent by alternative strategy

"""



# if k<2 or k>n: 
if int(sys.argv[2]) < 2 or int(sys.argv[2]) > int(sys.argv[1]):
    sys.exit("k should not be smaller than 2 or larger than n") 

n = int(sys.argv[1])
k = int(sys.argv[2])
player = str(sys.argv[3])[1]


class Game():
    def __init__(self):
        self.initialize_game()
        
    def empty_board(self, n):
        brd = []
        while len(brd) < n:
            brd.append([])
            while len(brd[-1]) < n:
                brd[-1].append('.')
        return brd
    
    def center_board(self, brd):
        centerx_x = []
        centerx_y = []
        centero_x = []
        centero_y = []
        for i, row in enumerate(brd):
            for j, col in enumerate(row):
                if brd[i][j] == 'X':
                    centerx_x.append(i)
                    centerx_y.append(j)
                elif brd[i][j] == 'O':
                    centero_x.append(i)
                    centero_y.append(j)
                if centero_x == [] and centero_x == []:
                    centero_x = centerx_x
                    centero_y = centerx_y
        return round(mean(centerx_x)), round(mean(centerx_y)), round(mean(centero_x)), round(mean(centero_y))
    
    def unempty_board(self, brd):
        all_x = []
        all_y = []
        for i, row in enumerate(brd):
            for j, col in enumerate(row):
                if brd[i][j] != '.':
                    all_x.append(i)
                    all_y.append(j)
                    
        return min(all_x), max(all_x), min(all_y), max(all_y)


    def initialize_game(self):
        self.current_state = self.empty_board(n)

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print('-----'*n)
        for i in range(0, n):
            for j in range(0, n):
                print(f'| {self.current_state[i][j]} |', end='')
            print('\n' + '-----'*n)
        print()
        
    def empty_squares(self, brd):
        emptys = []
        for i, row in enumerate(brd):
            for j, col in enumerate(row):
                if brd[i][j] == '.':
                    emptys.append([i, j])
        return emptys
               
        
    # Determines if the made move is a legal move
    def is_valid(self, px, py):
        if px < 0 or px > n-1 or py < 0 or py > n-1: # can't place outside the board
            return False
        elif self.current_state[px][py] != '.': # can't place on an occupied square
            return False
        else:
            return True
        
        
    # Checks if the game has ended and returns the winner in each case
    def is_terminal(self):
        
        # Column win           
        colwin = []
        for col in range(0, n):
            tmp = []
            for row in range(0, n):   
                tmp.append(self.current_state[row][col])
            colwin.append(tmp)
        
        # Row win
        rowwin = []
        for row in range(0, n):
            tmp = []
            for col in range(0, n):   
                tmp.append(self.current_state[row][col])
            rowwin.append(tmp)
        
        # Main diagonal win
        diagwin = []
        tmp1 = []
        tmp2 = []
        for diag in range(0, n):
            tmp1.append(self.current_state[diag][diag])
            tmp2.append(self.current_state[diag][-diag+(n-1)])
        diagwin.append(tmp1)
        diagwin.append(tmp2)
        
        # k X in a row

        # only empty squares
        kX = []
        for i in range(0, n-k+1):
            tmp = ['.']*n
            tmp[i:(i+k)] = ['X']*k
            kX.append(tmp)
        
        # k O in a row

        # only empty squares
        kO = []
        for i in range(0, n-k+1):
            tmp = ['.']*n
            tmp[i:(i+k)] = ['O']*k
            kO.append(tmp)


        #is_win
        for i, win in enumerate(kX):
            for j, row in enumerate(rowwin):
                if len(win) == len(row):
 
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == row[l] and win[l] == 'X':
                            count = count+1
                        if count == k:
                            return 'X'
                    
                    
        for i, win in enumerate(kX):
            for j, col in enumerate(colwin):
                if len(win) == len(col):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == col[l] and win[l] == 'X':
                            count = count+1
                        if count == k:
                            return 'X'
                    
        for i, win in enumerate(kX):
            for j, diag in enumerate(diagwin):
                if len(win) == len(diag):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == diag[l] and win[l] == 'X':
                            count = count+1
                        if count == k:
                            return 'X'
                    
        for i, win in enumerate(kO):
            for j, row in enumerate(rowwin):
                if len(win) == len(row):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == row[l] and win[l] == 'O':
                            count = count+1
                        if count == k:
                            return 'O'
                    
                    
        for i, win in enumerate(kO):
            for j, col in enumerate(colwin):
                if len(win) == len(col):
                 
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == col[l] and win[l] == 'O':
                            count = count+1
                        if count == k:
                            return 'O'
                    
        for i, win in enumerate(kO):
            for j, diag in enumerate(diagwin):
                if len(win) == len(diag):
               
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == diag[l] and win[l] == 'O':
                            count = count+1
                        if count == k:
                            return 'O'        

        # Non-main diagonal win
        
        # upper right to lower left non-main diagonals in upper left triangle
        uldiagwin = []
        for i in range(k, n):
            tmp = []
            x = 0
            y = i-1
            for j in range(0, i):
                tmp.append(self.current_state[x][y])
                x = x+1
                y = y-1
            uldiagwin.append(tmp)

        # upper right to lower left non-main diagonals in lower right triangle
        lrdiagwin = []
        for i in range(k, n):
            tmp = []
            x = n-i 
            y = n-1
            for j in range(0, i):
                tmp.append(self.current_state[x][y])
                x = x+1
                y = y-1
            lrdiagwin.append(tmp)
            
        # upper right to lower left non-main diagonals in lower triangles
        lowdiagwin = []
        for i in range(k, n):
            tmp1 = []
            tmp2 = []
            x = n-i  # start at lower left triangle
            y = 0
            for j in range(0, i):
                tmp1.append(self.current_state[x][y])
                tmp2.append(self.current_state[y][x]) # symmertic
                x = x+1
                y = y+1
            lowdiagwin.append(tmp1)
            lowdiagwin.append(tmp2)
                
        # k X in a row on non-main diagonals
        kX_nonmain = []
        for i in range(0, n-k):
            len_diag = i+k
            for j in range(0, len_diag-k+1):
                tmp = ['.']*len_diag
                tmp[j:(j+k)] = ['X']*k
                kX_nonmain.append(tmp)
        
        # k O in a row on non-main diagonals
        kO_nonmain = []
        for i in range(0, n-k):
            len_diag = i+k
            for j in range(0, len_diag-k+1):
                tmp = ['.']*len_diag
                tmp[j:(j+k)] = ['O']*k
                kO_nonmain.append(tmp)
        
        #is_win_non-main diagonals
        
        for i, win in enumerate(kX_nonmain):
            for j, uldiag in enumerate(uldiagwin):
                if len(win) == len(uldiag):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == uldiag[l] and win[l] == 'X':
                            count = count+1
                        if count == k:
                            return 'X'
                    
                    
        for i, win in enumerate(kX_nonmain):
            for j, lrdiag in enumerate(lrdiagwin):
                if len(win) == len(lrdiag):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == lrdiag[l] and win[l] == 'X':
                            count = count+1
                        if count == k:
                            return 'X'
                    
        for i, win in enumerate(kX_nonmain):
            for j, lowdiag in enumerate(lowdiagwin):
                if len(win) == len(lowdiag):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == lowdiag[l] and win[l] == 'X':
                            count = count+1
                        if count == k:
                            return 'X'
                    
        for i, win in enumerate(kO_nonmain):
            for j, uldiag in enumerate(uldiagwin):
                if len(win) == len(uldiag):
                   
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == uldiag[l] and win[l] == 'O':
                            count = count+1
                        if count == k:
                            return 'O'
                    
                    
        for i, win in enumerate(kO_nonmain):
            for j, lrdiag in enumerate(lrdiagwin):
                if len(win) == len(lrdiag):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == lrdiag[l] and win[l] == 'O':
                            count = count+1
                        if count == k:
                            return 'O'
                    
        for i, win in enumerate(kO_nonmain):
            for j, lowdiag in enumerate(lowdiagwin):
                if len(win) == len(lowdiag):
                    
                    count = 0
                    for l in range(0, len(win)):
                        if win[l] == lowdiag[l] and win[l] == 'O':
                            count = count+1
                        if count == k:
                            return 'O'        

        
        
        # Is whole board full?
        for i in range(0, n):
            for j in range(0, n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None

        # It's a tie!
        return '.'
    
    
    
    # Player 'X' is max
    def max_alpha_beta_heuristic(self, alpha, beta):
    
        # Possible values for maxv are:
        # -1 - loss
        # 0  - draw
        # 1  - win
        # We're initially setting it to -inf worse than the worst case:
        maxv = -inf
        px = None
        py = None

        result = self.is_terminal()

        if result == 'X':
            return (1, 0, 0)
        elif result == 'O':
            return (-1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        
        #meanx_x, meanx_y, meano_x, meano_y = self.center_board(self.current_state)         
        min_x, max_x, min_y, max_y = self.unempty_board(self.current_state)
        
        
        for i in range(max(0,min_x), min(max_x, n-1)+1):
            for j in range(max(0,min_y), min(max_y, n-1)+1):

                if self.current_state[i][j] == '.':

                    # On the empty field player 'X' makes a move and calls Min
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 'X'
                    (v, min_i, min_j) = self.min_alpha_beta_heuristic(alpha, beta)
                    # Fixing the maxv value if needed
                    if v > maxv:
                        maxv = v
                        px = i
                        py = j

                        if maxv > alpha:
                            alpha = maxv
                    # Setting back the square to empty
                    self.current_state[i][j] = '.'

                    if maxv >= beta:
                        return (maxv, px, py)
                        
        if px == None or py == None:
            for i in range(0, n):
                for j in range(0, n):
                    if self.current_state[i][j] == '.':

                        # On the empty field player 'X' makes a move and calls Min
                        # That's one branch of the game tree.
                        self.current_state[i][j] = 'X'
                        (v, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                        # Fixing the maxv value if needed
                        if v > maxv:
                            maxv = v
                            px = i
                            py = j

                            if maxv > alpha:
                                alpha = maxv
                        # Setting back the square to empty
                        self.current_state[i][j] = '.'

                        # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                        if maxv >= beta:
                            return (maxv, px, py)

            
       
        return (maxv, px, py)
    
    
    
    # Player 'O' is min
    def min_alpha_beta_heuristic(self, alpha, beta):

        minv = inf

        qx = None
        qy = None

        result = self.is_terminal()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        if result == 'X':
            return (1, 0, 0)
        elif result == 'O':
            return (-1, 0, 0)
        elif result == '.':
            return (0, 0, 0)



        #meanx_x, meanx_y, meano_x, meano_y = self.center_board(self.current_state)
        min_x, max_x, min_y, max_y = self.unempty_board(self.current_state)

        for i in range(max(0,min_x), min(max_x, n-1)+1):
            for j in range(max(0,min_y), min(max_y, n-1)+1):

                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'

                    (v, max_i, max_j) = self.max_alpha_beta_heuristic(alpha, beta)

                    if v < minv:
                        minv = v
                        qx = i
                        qy = j

                        if minv < beta:
                            beta = minv
                    # Setting back the square to empty
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

        if qx == None or qy == None:
            for i in range(0, n):
                for j in range(0, n):
                    if self.current_state[i][j] == '.':
                        self.current_state[i][j] = 'O'
                        (v, max_i, max_j) = self.max_alpha_beta(alpha, beta)

                        if v < minv:
                            minv = v
                            qx = i
                            qy = j

                            if minv < beta:
                                beta = minv
                        self.current_state[i][j] = '.'
                        if minv <= alpha:
                            return (minv, qx, qy)
                        
        return (minv, qx, qy)
    
    # Player 'X' is max
    def max_alpha_beta(self, alpha, beta):
    
        # Possible values for maxv are:
        # -1 - loss
        # 0  - draw
        # 1  - win
        # We're initially setting it to -inf worse than the worst case:
        maxv = -inf
        px = None
        py = None

        result = self.is_terminal()

        if result == 'X':
            return (1, 0, 0)
        elif result == 'O':
            return (-1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    
                    # On the empty field player 'X' makes a move and calls Min
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 'X'
                    (v, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    # Fixing the maxv value if needed
                    if v > maxv:
                        maxv = v
                        px = i
                        py = j
                        
                        if maxv > alpha:
                            alpha = maxv
                    # Setting back the square to empty
                    self.current_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return (maxv, px, py)

        return (maxv, px, py)
    
    # Player 'O' is min
    def min_alpha_beta(self, alpha, beta):

        minv = inf

        qx = None
        qy = None

        result = self.is_terminal()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        if result == 'X':
            return (1, 0, 0)
        elif result == 'O':
            return (-1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (v, max_i, max_j) = self.max_alpha_beta(alpha, beta)

                    if v < minv:
                        minv = v
                        qx = i
                        qy = j

                        if minv < beta:
                            beta = minv
                    self.current_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if minv <= alpha:
                        return (minv, qx, qy)

        return (minv, qx, qy)
                
    def play_game(self):
        
        while True:
            self.draw_board()
            self.result = self.is_terminal()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("Draw!")


                self.initialize_game()
                return

            if self.player_turn == 'X':

                
                if len(self.empty_squares(self.current_state)) == n*n:
                    choices = []
                    for i in range(n):
                        choices.append(i)
                    px = choice(choices)
                    py = choice(choices) 

                else:   
                    start = time.time()
                    (v, px, py) = self.max_alpha_beta(-inf, inf)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 4)))
                    print('Recommended move: X = {}, Y = {}'.format(px, py))
                

                self.current_state[px][py] = 'X'
                self.player_turn = 'O'
                    
                    

            else:
                if len(self.empty_squares(self.current_state)) == n*n:
                        choices = []
                        for i in range(n):
                            choices.append(i)
                        qx = choice(choices)
                        qy = choice(choices) 
                        
                else:   
                    start = time.time()
                    (v, qx, qy) = self.min_alpha_beta(-inf, inf)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 4)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                
                self.current_state[qx][qy] = 'O'
                self.player_turn = 'X'      
                
    def play_game_heuristic(self):
        
            #global latestX_x 
            #global latestX_y
            #global latestO_x
            #global latestO_y
            
            #latestO_x = round((n-1)/2)
            #latestO_y = round((n-1)/2)
            while True:
                self.draw_board()
                self.result = self.is_terminal()

                if self.result != None:
                    if self.result == 'X':
                        print('The winner is X!')
                    elif self.result == 'O':
                        print('The winner is O!')
                    elif self.result == '.':
                        print("Draw!")


                    self.initialize_game()
                    return

                if self.player_turn == 'X':
                    
                    
                    
                    if len(self.empty_squares(self.current_state)) == n*n:
                        choices = []
                        for i in range(n):
                            choices.append(i)
                        #px = choice(choices)
                        #py = choice(choices) 
                        px = round((n-1)/2)
                        py = round((n-1)/2)
                    else:   
                        start = time.time()
                        (v, px, py) = self.max_alpha_beta_heuristic(-inf, inf)
                        if px == None or py == None:
                            (v, px, py) = self.max_alpha_beta(-inf, inf)
                        end = time.time()
                        print('Evaluation time: {}s'.format(round(end - start, 4)))
                        print('Recommended move: X = {}, Y = {}'.format(px, py))
                
                    #latestX_x = px
                    #latestX_y = py
                    self.current_state[px][py] = 'X'
                    self.player_turn = 'O'



                else:
                    if len(self.empty_squares(self.current_state)) == n*n-1:
                            choices = []
                            for i in range(n):
                                choices.append(i)
                            #qx = choice(choices)
                            #qy = choice(choices) 
                            qx = round((n-1)/2)-1
                            qy = round((n-1)/2)-1

                    else:   
                        start = time.time()
                        (v, qx, qy) = self.min_alpha_beta_heuristic(-inf, inf)
                       
                        if qx == None or qy == None:
                            (v, qx, qy) = self.min_alpha_beta(-inf, inf)
                        end = time.time()
                        print('Evaluation time: {}s'.format(round(end - start, 4)))
                        print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    #latestO_x = qx
                    #latestO_y = qy
                    
                    self.current_state[qx][qy] = 'O'
                    self.player_turn = 'X'


    def play_game_txt(self): # play with opponent
        
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
                    'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
        
        inv_col_dict = {v: k for k, v in col_dict.items()}
        
        while True:
            self.draw_board()
            self.result = self.is_terminal()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("Draw!")


                self.initialize_game()
                return

            if self.player_turn == 'X':

                if player == 'x': # we play first (X)
                            
                    start = time.time()
                    (v, px, py) = self.max_alpha_beta(-inf, inf)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 4)))
                    print('Recommended move: X = {}, Y = {}'.format(px, py)) 
                    self.current_state[px][py] = 'X'
                    self.player_turn = 'O'
                    
                    with open("xmoves.txt","a+") as xfile:
                        xfile.write('x%s%s\n'%(str(px+1), inv_col_dict[py]))
                        xfile.close()
                        
                else: #player == 'o'
                     
                    while True:
                        # Opponent
                        while True:
                            
                            with open("xmoves.txt","r") as xfile:
                                xmoves = xfile.readlines()
                                xfile.close()
                                xmoves = xmoves[-1]
                            
                            if len(xmoves) != 0:
                                if xmoves[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    xmoves_x = int(xmoves[1])*10 + int(xmoves[2])-1
                                    xmoves_y = col_dict[xmoves[3]]
                                else:
                                    xmoves_x = int(xmoves[1])-1
                                    xmoves_y = col_dict[xmoves[2]]
                                break 
                                
                            else:
                                print("Please make your move!")
                                time.sleep(10)
                                
                            
                            
                        px = xmoves_x
                        py = xmoves_y

                        if self.is_valid(px, py):
                            self.current_state[px][py] = 'X'
                            self.player_turn = 'O'
                            break
                        else:
                            print('Invalid move! Try again.')  
                            time.sleep(10)
                    

            else: #self.player_turn == 'O'
                
                if player == 'o': # we play second (O)
                    
                    start = time.time()
                    (v, qx, qy) = self.min_alpha_beta(-inf, inf)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 4)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                    self.current_state[qx][qy] = 'O'
                    self.player_turn = 'X'
                    
                    with open("omoves.txt","a+") as ofile:
                        ofile.write('o%s%s\n'%(str(qx+1), inv_col_dict[qy]))
                        ofile.close()
                    
                    
                        
                else: #player == 'x'
                     
                    while True:
                        # Opponent
                        while True:
                             
                            with open("omoves.txt","r") as ofile:
                                omoves = ofile.readlines()
                                ofile.close()
                                omoves = omoves[-1]
                            
                            if len(omoves) != 0:
                                if omoves[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    omoves_x = int(omoves[1])*10 + int(omoves[2])-1
                                    omoves_y = col_dict[omoves[3]]
                                else:
                                    omoves_x = int(omoves[1])-1
                                    omoves_y = col_dict[omoves[2]]
                                break 
                                
                            else:
                                print("Please make your move!")
                                time.sleep(10)
                                
                        qx = omoves_x
                        qy = omoves_y

                        if self.is_valid(qx, qy):
                            self.current_state[qx][qy] = 'O'
                            self.player_turn = 'X'
                            break
                        else:
                            print('Invalid move! Try again.')
                            time.sleep(10)
        
    def play_game_txt_heuristic(self): # play with opponent
        
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
                    'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
        
        inv_col_dict = {v: k for k, v in col_dict.items()}
        
        while True:
            self.draw_board()
            self.result = self.is_terminal()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("Draw!")


                self.initialize_game()
                return

            if self.player_turn == 'X':

                if player == 'x': # we play first (X)
                            
                    start = time.time()
                    (v, px, py) = self.max_alpha_beta_heuristic(-inf, inf)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 4)))
                    print('Recommended move: X = {}, Y = {}'.format(px, py)) 
                    self.current_state[px][py] = 'X'
                    self.player_turn = 'O'
                    
                    with open("xmoves.txt","a+") as xfile:
                        xfile.write('x%s%s\n'%(str(px+1), inv_col_dict[py]))
                        xfile.close()
                        
                else: #player == 'o'
                     
                    while True:
                        # Opponent
                        while True:
                            
                            with open("xmoves.txt","r") as xfile:
                                xmoves = xfile.readlines()
                                xfile.close()
                                xmoves = xmoves[-1]
                            
                            if len(xmoves) != 0:
                                if xmoves[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    xmoves_x = int(xmoves[1])*10 + int(xmoves[2])-1
                                    xmoves_y = col_dict[xmoves[3]]
                                else:
                                    xmoves_x = int(xmoves[1])-1
                                    xmoves_y = col_dict[xmoves[2]]
                                break 
                                
                            else:
                                print("Please make your move!")
                                time.sleep(10)
                                
                            
                            
                        px = xmoves_x
                        py = xmoves_y

                        if self.is_valid(px, py):
                            self.current_state[px][py] = 'X'
                            self.player_turn = 'O'
                            break
                        else:
                            print('Invalid move! Try again.')  
                            time.sleep(10)
                    

            else: #self.player_turn == 'O'
                
                if player == 'o': # we play second (O)
                    
                    start = time.time()
                    (v, qx, qy) = self.min_alpha_beta_heuristic(-inf, inf)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 4)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                    self.current_state[qx][qy] = 'O'
                    self.player_turn = 'X'
                    
                    with open("omoves.txt","a+") as ofile:
                        ofile.write('o%s%s\n'%(str(qx+1), inv_col_dict[qy]))
                        ofile.close()
                    
                    
                        
                else: #player == 'x'
                     
                    while True:
                        # Opponent
                        while True:
                             
                            with open("omoves.txt","r") as ofile:
                                omoves = ofile.readlines()
                                ofile.close()
                                omoves = omoves[-1]
                            
                            if len(omoves) != 0:
                                if omoves[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    omoves_x = int(omoves[1])*10 + int(omoves[2])-1
                                    omoves_y = col_dict[omoves[3]]
                                else:
                                    omoves_x = int(omoves[1])-1
                                    omoves_y = col_dict[omoves[2]]
                                break 
                                
                            else:
                                print("Please make your move!")
                                time.sleep(10)
                                
                        qx = omoves_x
                        qy = omoves_y

                        if self.is_valid(qx, qy):
                            self.current_state[qx][qy] = 'O'
                            self.player_turn = 'X'
                            break
                        else:
                            print('Invalid move! Try again.')
                            time.sleep(10)
        


# In[ ]:



def main():
    g = Game()
    g.play_game_txt()

if __name__ == "__main__":
    main()


# In[ ]:




