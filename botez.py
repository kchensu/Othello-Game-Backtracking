from reversi import *
from copy import deepcopy
from time import time
from random import choice


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
                return 1
            if game.state == "Black wins": # if player wins 
                return -1
            if game.state == "In progress": # game has not ended
                game.switch_turn()

    def train(self, game, N, max_time):
        """ return total training score of N random playouts """
        score = 0
        start = time()
        for i in range(N): # do N number of random playouts
            if time() - start >= max_time: # if more than 5 seconds
                break
            temp_game = deepcopy(game)
            score += self.playout(temp_game)
        return score

    def find_best_move(self, board, turn):
        """ find the best move """
        game = Reversi(board=board, turn=turn)
        legal_moves = game.find_legal_positions()
        if len(legal_moves) == 1: # no reason to predict future moves when there is only one move left
            best_move = legal_moves[0]
            return best_move
        score_list = []
        for move in legal_moves: # for each legal move
            possible_game_state_after_legal_move = deepcopy(game) # make a copy of the current game
            possible_game_state_after_legal_move.place_tile(move) # play the legal move
            possible_game_state_after_legal_move.switch_turn() 
            score = self.train(possible_game_state_after_legal_move, N=1000, max_time=10) # ployout game N times
            score_list.append(score)
        highest_score_index = score_list.index(max(score_list)) # pick the score with the most wins, highest score
        best_move = legal_moves[highest_score_index]
        return best_move
