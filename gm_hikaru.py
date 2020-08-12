from reversi import *
from copy import deepcopy
from time import time
from random import choice
# from multiprocessing.pool import Pool
import multiprocessing

class GMHikaru:
    """ GMHikaru is a Reversi AI that uses Monte Carlo Search """
    def __init__(self):
          self.strategy_weights = np.array([[1000, 50,   100,   100,  100,  100,  50, 1000],
                                           [  50,  -20,  -10,  -10,  -10,  -10,  -20,   50], 
                                           [ 100,  -10,    0,    0,    0,    0,  -10,  100], 
                                           [ 100,  -10,    0,    0,    0,    0,  -10,  100],
                                           [ 100,  -10,    0,    0,    0,    0,  -10,  100], 
                                           [ 100,  -10,    0,    0,    0,    0,  -10,  100], 
                                           [  50,  -20,  -10,  -10,  -10,  -10,  -20,   50], 
                                           [1000,   50,  100,  100,  100,  100,   50, 1000]])
    
    def eval_fn(self, board, turn):
        score = 0
        rest = 0
        opp = None
        if turn == "b":
            opp = 'w'
        elif turn == "w":
            opp = 'b'
        for i in range(8):
            for j in range(8):
                test = board[i][j]
                if test == turn:
                    score += self.strategy_weights[i][j]
                elif test == opp:
                    score -= self.strategy_weights[i][j]
                else:
                    rest +=1
        if score >= 0:
            score += (128-rest*2)
        else:
            score -= (128-rest*2)
        return score
    
    def min_max(self, depth, alpha, beta, game):
        maximizing_color = game.turn
        if depth ==0:
            temp_game = deepcopy(game)
            score = self.eval_fn(game.board, maximizing_color)
            return score
        
        legal_moves = game.find_legal_positions()
        if len(legal_moves) == 0:
            temp_game = deepcopy(game)
            score = self.min_max(depth -1, alpha, beta, temp_game)
            return score
        else:
            for move in legal_moves:
                temp_game = deepcopy(game)
                temp_game.place_tile(move)
                temp_game.switch_turn()
                temp_game.update_state()
                test = self.min_max(depth -1,  alpha, beta, temp_game)

                if maximizing_color == game.turn:
                    if alpha == None or test > alpha:
                        alpha = test
                else:
                    if beta == None or test < beta:
                        beta = test
                if alpha != None and beta != None and beta <= alpha:
                    break

        if maximizing_color == game.turn:
            score = alpha
        else:
            score = beta
        return score

    def find_best_move(self, board, turn, black, white):
        alpha = None
        beta = None
        best_move = None
        depth = 6

        game = Reversi(board=board, turn= turn, black=black, white=white)
        legal_moves = game.find_legal_positions()
        for move in legal_moves:
            if alpha is not None:
                beta = -1*alpha

            temp_game = deepcopy(game)
            temp_game.place_tile(move)
            temp_game.switch_turn()
            temp_game.update_state()    
            test = self.min_max(depth-1, alpha, beta, temp_game)

            if alpha == None or test > alpha:
                alpha = test
                bestmove = move
        return bestmove
