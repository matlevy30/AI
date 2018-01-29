#!/usr/bin/env python
from isolation import Board, game_as_text
from random import randint
import platform
from time import time, sleep
from scipy.constants.constants import alpha
from numpy.random.mtrand import beta
#import resource
if platform.system() != 'Windows':
    import resource

# This file is your main submission that will be graded against. Do not
# add any classes or functions to this file that are not part of the classes
# that we want.


class OpenMoveEvalFn:

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state
        
        Evaluation function that outputs a score equal to how many 
        moves are open for AI player on the board minus how many moves 
	are open for Opponent's player on the board.

	Note:
		1. Be very careful while doing opponent's moves. You might end up 
		   reducing your own moves.
		2. Here if you add overlapping moves of both queens, you are considering one available square twice.
		   Consider overlapping square only once. In both cases- myMoves and in OppMoves. 
		3. If you think of better evaluation function, do it in CustomEvalFn below. 
            
        Args
            param1 (Board): The board and game state.
            param2 (bool): True if maximizing player is active.

        Returns:
            float: The current state's score. MyMoves-OppMoves.
            
        """
        #Get total number of moves of Opponent
        opt = game.get_opponent_moves().values()
        opponent_moves = set(opt[1]) - set(opt[0])
        number_opponent_moves = opt[0] + list(opponent_moves)

        #Get total of my moves removing overlapping
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        my_m = set(queen2) - set(queen1) #in second but not in first
        number_my_moves = queen1 + list(my_m) #total of number of my moves
        
        return len(number_my_moves) - len(number_opponent_moves)

class CustomEvalFn:

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state
        
        Custom evaluation function that acts however you think it should. This 
        is not required but highly encouraged if you want to build the best 
        AI possible.
        
        Args
            game (Board): The board and game state.
            maximizing_player_turn (bool): True if maximizing player is active.

        Returns:
            float: The current state's score, based on your own heuristic.
            
        """
        # odd opponent
        # even me
        
        #Get total number of moves of Opponent
        opt = game.get_opponent_moves().values()
        opponent_moves = set(opt[1]) - set(opt[0])
        number_my_moves = len(opt[0] + list(opponent_moves))
        #number_opponent_moves = len(opt[0] + list(opponent_moves))
        #Get total of my moves removing overlapping
        
        
        
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        my_m = set(queen2) - set(queen1) #in second but not in first
        number_opponent_moves = len(queen1 + list(my_m)) #total of number of my moves
        #number_my_moves = len(queen1 + list(my_m)) #total of number of my moves
        
        if len(opt[1]) == 0 or len(opt[0]) == 0:
            #number_my_moves += 100
            return -100
            #return 100
        
        if len(queen1) == 0 or len(queen2) == 0:
            #number_my_moves = 100
            return 100
            #return -100
        
        board_ends = [(0,0),(game.width - 1, 0) , (0, game.height - 1), (game.width - 1, game.height - 1)]
        playeer_location = game.__last_queen_move__
        q2 = playeer_location.values()[0]
        q1 = playeer_location.values()[3]
        
        #if q1 in board_ends:
         #   number_my_moves -=3
        
        #if q2 in board_ends:
         #z   number_my_moves -=3
        
        return  number_my_moves -  (2 * number_opponent_moves)


class CustomPlayer:
    """Player that chooses a move using 
    your evaluation function and 
    a minimax algorithm 
    with alpha-beta pruning.
    You must finish and test this player
    to make sure it properly uses minimax
    and alpha-beta to return a good move."""

    def __init__(self, search_depth = 5, eval_fn=CustomEvalFn()):
        """Initializes your player.
        
        if you find yourself with a superior eval function, update the default 
        value of `eval_fn` to `CustomEvalFn()`
        
        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Utility function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, legal_moves, time_left):
        """Called to determine one move by your agent
        
	Note:
		1. Do NOT change the name of this 'move' function. We are going to call 
		the this function directly. 
		2. Change the name of minimax function to alphabeta function when 
		required. Here we are talking about 'minimax' function call,
		NOT 'move' function name.

        Args:
            game (Board): The board and game state.
            legal_moves (dict): Dictionary of legal moves and their outcomes
            time_left (function): Used to determine time left before timeout
            
        Returns:
            (tuple, tuple): best_move_queen1, best_move_queen2
        """
        best_move_queen1,best_move_queen2 = self.alphabeta(game, time_left, depth=self.search_depth)
        #best_move_queen1,best_move_queen2 = self.minimax(game, time_left, depth=self.search_depth) 
            
        return best_move_queen1,best_move_queen2

    def utility(self, game, maximizing_player):
        """Can be updated if desired. Not compulsory. """
        return self.eval_fn.score(game)


    def minimax(self, game, time_left, depth, maximizing_player=True):
        """Implementation of the minimax algorithm
        
        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple,tuple, int): best_move_queen1,best_move_queen2, val
        """
        print game.print_board()
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        best_move_queen1 = queen1[0]
        best_move_queen2 = queen2[0] 
     
        
        if len(queen1) == 0 | len(queen2) == 0:
            return (None,None)
        
        best_val = float('-inf')
        for queen1_move in queen1:
            for queen2_move in queen2:
                if queen1_move != queen2_move:
                    forecast_board = game.forecast_move(queen1_move,queen2_move)
                    u = self.min_p(forecast_board, depth-1, time_left)
                    if u > best_val:
                        best_move_queen1 = queen1_move
                        best_move_queen2 = queen2_move
                        best_val = u
                    if time_left() <= 3:
                        return best_move_queen1,best_move_queen2
        
        # finish this function!
        return best_move_queen1,best_move_queen2

    def min_p(self,game, depth, time_left):
        if depth == 0 or time_left() < 3:
            return self.eval_fn.score(game)
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        
        if len(queen1) == 0 | len(queen2) == 0:
            return None
        
        score = float('inf')
        for queen1_move in queen1:
            for queen2_move in queen2:
                if queen1_move != queen2_move:
                    forecast_board = game.forecast_move(queen1_move,queen2_move)
                    u = self.max_p(forecast_board, depth-1, time_left)
                    if u < score:
                        score = u 
                    if time_left() <= 3:
                        return score
        
        return score
    
    def max_p(self,game, depth, time_left):
        if depth == 0 or time_left() < 2:
            return self.eval_fn.score(game)
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        
        if len(queen1) == 0 | len(queen2) == 0:
            return None
        
        score = float('-inf')
        for queen1_move in queen1:
            for queen2_move in queen2:
                if queen1_move != queen2_move:
                    forecast_board = game.forecast_move(queen1_move,queen2_move)
                    u = self.min_p(forecast_board, depth-1, time_left)
                    if u > score:
                        score = u
                    if time_left() <= 5:
                        return score
                    
        return score 
        
        
    def alphabeta(self, game, time_left, depth, alpha=float("-inf"), beta=float("inf"),maximizing_player=True):
        """Implementation of the alphabeta algorithm
        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple,tuple, int): best_move_queen1,best_move_queen2, val
        """
        # finish this function!
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        
        if len(queen1) == 0 or len(queen2) == 0:
            return (None, None)
        
        
        #If no legal Moves
        best_move_queen1 = None
        best_move_queen2 = None
        best_score = float('-inf')
        for queen1_move in queen1:
            for queen2_move in queen2:
                if queen1_move != queen2_move:
                    forecast_board = game.forecast_move(queen1_move,queen2_move)
                    score = self.min_value(forecast_board,depth-1,time_left,alpha,beta)
                    #print "Score: " + str(score)
                    #print game.print_board()
                    if score > best_score:
                        #print "Best ? " + str(score) 
                        #print time_left()
                        best_move_queen1 = queen1_move
                        best_move_queen2 = queen2_move
                        best_score = score
                    if time_left() < 10:
                        #print best_move_queen1
                        #print best_move_queen2
                        return best_move_queen1,best_move_queen2
        
        #print best_move_queen1
        #print best_move_queen2
        #print best_score
        return best_move_queen1,best_move_queen2
    
    
    def max_value(self,game, depth, time_left, alpha, beta):
        if depth == 0 or time_left() < 10:
            return self.eval_fn.score(game)
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        #print "Max Depth:" + str(depth)+ " " + str(queen1)
        #print queen2
        v = float('-inf')
        for queen1_move in queen1:
            for queen2_move in queen2:
                if queen1_move != queen2_move:
                    forecast_board = game.forecast_move(queen1_move,queen2_move)
                    v = max(v, self.min_value(forecast_board, depth-1, time_left,alpha,beta))
                    if v >= beta: return v
                    alpha = max(alpha,v)
                    if time_left() < 10:
                        #print "Max Dept:" + str(depth) + " "+ str(v) 
                        return v
       
        return v
    

    def min_value(self,game, depth, time_left, alpha, beta):
        if depth == 0 or time_left() < 10:
            return self.eval_fn.score(game)
        queen1 = game.get_legal_moves_of_queen1()
        queen2 = game.get_legal_moves_of_queen2()
        v = float('inf')
        for queen1_move in queen1:
            for queen2_move in queen2:
                if queen1_move != queen2_move:
                    forecast_board = game.forecast_move(queen1_move,queen2_move)
                    v =  min(v,self.max_value(forecast_board, depth-1, time_left,alpha,beta))
                    if v <= alpha: return v
                    beta = min(v,beta)
                    if time_left() < 10:
                        return v
     
        return v
