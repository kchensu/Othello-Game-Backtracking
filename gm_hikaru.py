from reversi import *
from copy import deepcopy
from time import time
from random import choice
# from multiprocessing.pool import Pool
import multiprocessing

a = (8, 8)
strategy_weights = np.zeros(a)
strategy_weights.astype(int)
strategy_weights[0, 0] = 100
strategy_weights[0, 1] = -20
strategy_weights[0, 2] = 20
strategy_weights[0, 3] = 5
strategy_weights[0, 4] = 5
strategy_weights[0, 5] = 20
strategy_weights[0, 6] = -20
strategy_weights[0, 7] = 100 

strategy_weights[1, 0] = -20
strategy_weights[1, 1] = -40
strategy_weights[1, 2] = -5
strategy_weights[1, 3] = -5
strategy_weights[1, 4] = -5
strategy_weights[1, 5] = -5
strategy_weights[1, 6] = -40
strategy_weights[1, 7] = -20 

strategy_weights[2, 0] = 20
strategy_weights[2, 1] = -5
strategy_weights[2, 2] = 15
strategy_weights[2, 3] = 3
strategy_weights[2, 4] = 3
strategy_weights[2, 5] = 15
strategy_weights[2, 6] = -5
strategy_weights[2, 7] = 20 

strategy_weights[3, 0] = 5
strategy_weights[3, 1] = -5
strategy_weights[3, 2] = 3
strategy_weights[3, 3] = 3
strategy_weights[3, 4] = 3
strategy_weights[3, 5] = 3
strategy_weights[3, 6] = -5
strategy_weights[3, 7] = 5 

strategy_weights[4, 0] = 5
strategy_weights[4, 1] = -5
strategy_weights[4, 2] = 3
strategy_weights[4, 3] = 3
strategy_weights[4, 4] = 3
strategy_weights[4, 5] = 3
strategy_weights[4, 6] = -5
strategy_weights[4, 7] = 5

strategy_weights[5, 0] = 20
strategy_weights[5, 1] = -5
strategy_weights[5, 2] = 15
strategy_weights[5, 3] = 3
strategy_weights[5, 4] = 3
strategy_weights[5, 5] = 15
strategy_weights[5, 6] = -5
strategy_weights[5, 7] = 20 

strategy_weights[6, 0] = -20
strategy_weights[6, 1] = -40
strategy_weights[6, 2] = -5
strategy_weights[6, 3] = -5
strategy_weights[6, 4] = -5
strategy_weights[6, 5] = -5
strategy_weights[6, 6] = -40
strategy_weights[6, 7] = -20 

strategy_weights[7, 0] = 100
strategy_weights[7, 1] = -20
strategy_weights[7, 2] = 20
strategy_weights[7, 3] = 5
strategy_weights[7, 4] = 5
strategy_weights[7, 5] = 20
strategy_weights[7, 6] = -20
strategy_weights[7, 7] = 100 


class GMHikaru:
    """ Botez is a Reversi AI that uses Monte Carlo Search """
    def __init__(self):
        pass

    def playout(self, game):
        """ playout a given game randomly, return a score of 1 if it results in a win or draw and a score of -1 it it is a loss """
        while game.state == "In progress":
            legal_moves = game.find_legal_positions()
            if len(legal_moves) != 0:
                random_position = choice(legal_moves)
                game.place_tile(random_position)
            game.update_state()
            if game.state == "Tie": # if draw 
                return 1
            if game.state == "White wins": # if GMHikaru (AI) wins 
                return 1
            if game.state == "Black wins": # if player wins 
                return -1
            if game.state == "In progress": # game has not ended
                game.switch_turn()
            
    def train(self, game, N):
        """ return total training score of N random playouts """
        score = 0
        playout_time_list = []
        start = time()
        pool = multiprocessing.Pool(processes= 12 )
        nums = []
        for i in range(N): # do N number of random playouts
            temp_game = deepcopy(game)
            nums.append(temp_game)
        score = pool.map(self.playout, nums)
        pool.close()
        pool.join()
        score = sum(score)
        return score

    def find_best_move(self, board, turn):
        """ find the best move """
        game = Reversi(board=board, turn=turn)
        legal_moves = game.find_legal_positions()
        if len(legal_moves) == 1: # no reason to predict future moves when there is only one move left
            best_move = legal_moves[0]
            return best_move
        score_list = []
        start = time()
        for move in legal_moves: # for each legal move
            if time() - start >= 5:
                print("Times up.....")
                break
            
            possible_game_state_after_legal_move = deepcopy(game) # make a copy of the current game
            possible_game_state_after_legal_move.place_tile(move) # play the legal move
            possible_game_state_after_legal_move.switch_turn() 
            score = self.train(possible_game_state_after_legal_move, N= 1) # ployout game N times
            score_list.append(score)
        new_score_list = []
        for i in range(len(score_list)):
            index = legal_moves[i]
            w1 = index[0]
            w2 = index[1]
            weights = strategy_weights[w1, w2]
            new_score = weights + i
            new_score_list.append(new_score)
        highest_score_index = new_score_list.index(max(new_score_list)) # pick the score with the most wins, highest score
        best_move = legal_moves[highest_score_index]
        print("Best move:", best_move)
        return best_move
