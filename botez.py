from reversi import *
from copy import deepcopy
from random import choice
# from multiprocessing.pool import Pool
import multiprocessing
from time import time

class Botez:
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
            if game.state == "White wins": # if Botez (AI) wins 
                if game.white == 'player' or game.white == 'gm_hikaru':
                    return -1
                else:
                    return 1
            if game.state == "Black wins": # if player wins 
                if game.black == 'player' or game.black == 'gm_hikaru':
                    return -1
                else:
                    return 1
            if game.state == "In progress": # game has not ended
                game.switch_turn()
            
    def train(self, game, N):
        """ return total training score of N random playouts """
        score = 0
        playout_time_list = []
        pool = multiprocessing.Pool(processes= 4 )
        nums = []
        for i in range(N): # do N number of random playouts
            temp_game = deepcopy(game)
            nums.append(temp_game)
        score = pool.map(self.playout, nums)
        pool.close()
        pool.join()
        score = sum(score)
        return score

    def find_best_move(self, board, turn, black, white):
        """ find the best move """
        game = Reversi(board=board, turn=turn, black=black, white=white)
        legal_moves = game.find_legal_positions()
        if len(legal_moves) == 1: # no reason to predict future moves when there is only one move left
            best_move = legal_moves[0]
            return best_move
        score_list = []
        start = time()
        for move in legal_moves: # for each legal move
            if len(legal_moves) <= 2:
                N = 1000
            elif len(legal_moves) > 3 and len(legal_moves) <= 6:
                N = 200
            else:
                N = 50
            possible_game_state_after_legal_move = deepcopy(game) # make a copy of the current game
            possible_game_state_after_legal_move.place_tile(move) # play the legal move
            possible_game_state_after_legal_move.update_state()
            possible_game_state_after_legal_move.switch_turn() 
            score = self.train(possible_game_state_after_legal_move, N) # ployout game N times
            score_list.append(score)
        highest_score_index = score_list.index(max(score_list)) # pick the score with the most wins, highest score
        best_move = legal_moves[highest_score_index]
        return best_move
