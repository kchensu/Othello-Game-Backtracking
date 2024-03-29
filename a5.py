from os import system
from reversi import *
from botez import *
from gm_hikaru import *
from random import choice
from time import sleep, time
import numpy as np


def clear_screen():
    """ clear terminal screen """
    try: 
        system("cls") # for windows
    except:
        system("clear") # for Unix


def print_main_menu():
    print("===============")
    print("|   REVERSI   |")
    print("===============")
    print("1. play against GM Hikaru")
    print("2. play against Botez")
    print("3. blind-folded GMHikaru vs Botez Sisters Showdown")
    print("4. exit")


def print_turn(turn, player_vs_ai_flag, GMHikaru_flag, Botez_flag, player_color):

    if player_vs_ai_flag:
        if turn == player_color:
            print("--------------------------")
            print("player's (%s) turn to play" %turn)
            print("--------------------------")
        else:
            if GMHikaru_flag:
                print("-----------------------------")
                print("GM Hikaru's (%s) turn to play" %turn)
                print("-----------------------------")
            elif Botez_flag:
                print("-------------------------")
                print("Botez's (%s) turn to play" %turn)
                print("-------------------------")
    elif GMHikaru_flag and Botez_flag:
        if turn == "w":
            print("-----------------------------")
            print("GM Hikaru's (%s) turn to play" %turn)
            print("-----------------------------")
        if turn == "b" :
            print("-------------------------")
            print("Botez's (%s) turn to play" %turn)
            print("-------------------------")


def print_black_wins():
    print("<><><><><><><>")
    print("| BLACK WINS |")
    print("<><><><><><><>")
    


def print_white_wins():
    print("<><><><><><><>")
    print("| WHITE WINS |")
    print("<><><><><><><>")


def print_draw_screen():
    print("<><><><>")
    print("| DRAW |")
    print("<><><><>")


def get_menu_input():
    while True:
        try:
            menu_input = int(input("menu input [0 - 4]:"))
        except ValueError:  # makes sure inputs are integers and within bounds 
            print("Please input a number.")
            continue
        if (menu_input < 0 or menu_input >= 5):
            print("Please try again.")
            continue
        return menu_input


def ask_for_player_color():
    while True:
        player_color = input("What do you want to be? [b/w]:")
        if player_color == "b" or player_color == "w":
            return player_color
        else:
            print("please input 'b' or 'w' ")

def print_board(board):
    print("    0   1   2   3   4   5   6   7 ")
    print("0 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], board[0][6], board[0][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("1 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[1][0], board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], board[1][6], board[1][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("2 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[2][0], board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], board[2][6], board[2][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("3 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[3][0], board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], board[3][6], board[3][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("4 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[4][0], board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], board[4][6], board[4][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("5 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[5][0], board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], board[5][6], board[5][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("6 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[6][0], board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], board[6][6], board[6][7]))
    print("  - - - - - - - - - - - - - - - - - " )
    print("7 | %s | %s | %s | %s | %s | %s | %s | %s |" %(board[7][0], board[7][1], board[7][2], board[7][3], board[7][4], board[7][5], board[7][6], board[7][7]))


def get_board_coordinate():
    """ get board coordinate from user """
    while True:
        try:
            x = int(input("coordinate x [0 - 7]:"))
            y = int(input("coordinate y [0 - 7]:"))
        except ValueError:  # makes sure inputs are integers and within bounds 
            print("Please input a number.")
            continue
        if (x < 0 or x >= 8) or (y < 0 or y >= 8):
            print("Please try again.")
            continue
        break
    return np.array([x, y])


def print_legal_moves(legal_moves):
    """ print available legal moves """
    print("Available legal moves:")
    for elem in legal_moves:
        print("x: %d y: %d" %(elem[0], elem[1]))


def main():
    print("initializing.............")
    
    initial_board = np.array([  [" ", " ", " ", " ", " ", " ", " ", " "], 
                                [" ", " ", " ", " ", " ", " ", " ", " "], 
                                [" ", " ", " ", " ", " ", " ", " ", " "], 
                                [" ", " ", " ", "b", "w", " ", " ", " "], 
                                [" ", " ", " ", "w", "b", " ", " ", " "], 
                                [" ", " ", " ", " ", " ", " ", " ", " "], 
                                [" ", " ", " ", " ", " ", " ", " ", " "], 
                                [" ", " ", " ", " ", " ", " ", " ", " "]])
    sleep(1)
    clear_screen()

    while True:
        player_vs_ai_flag = False
        GMHikaru_flag = False
        Botez_flag = False
        player_color = None
        menu_input = None
        print_main_menu()
        menu_input = get_menu_input()
        if menu_input != 4:
            starts_first = choice(np.array(["b", "w"])) 
            if menu_input == 1:
                player_vs_ai_flag = True
                player_color = ask_for_player_color()
                GMHikaru_flag = True
                gm_hikaru_ai = GMHikaru()
                if player_color == "b":
                    game = Reversi(board=initial_board, turn=starts_first, white="gm_hikaru")
                elif player_color == "w":
                    game = Reversi(board=initial_board, turn=starts_first, black="gm_hikaru")
            elif menu_input == 2:
                player_vs_ai_flag = True
                player_color = ask_for_player_color()
                Botez_flag = True
                botez_ai = Botez()
                if player_color == "b":
                    game = Reversi(board=initial_board, turn=starts_first, white="botez")
                elif player_color == "w":
                    game = Reversi(board=initial_board, turn=starts_first, black="botez")
            elif menu_input == 3:
                GMHikaru_flag = True
                gm_hikaru_ai = GMHikaru()
                Botez_flag = True
                botez_ai = Botez()
                game = Reversi(board=initial_board, turn=starts_first, black="gm_hikaru", white="botez")
            game_time = time()
            while True:
                print_turn(game.turn, player_vs_ai_flag, GMHikaru_flag, Botez_flag, player_color)
                print_board(game.board)
                legal_moves = game.find_legal_positions()
                if len(legal_moves) != 0:
                    if player_vs_ai_flag: 
                        if game.turn == player_color:
                            while True:
                                print_legal_moves(legal_moves)
                                board_coordinate = get_board_coordinate()
                                if game.is_move_valid(board_coordinate):
                                    break
                                else:
                                    print("please pick a legal move coordinate")
                        else:
                            if Botez_flag:
                                start = time()
                                board_coordinate = botez_ai.find_best_move(board=game.board, turn=game.turn, white=game.white, black=game.black)
                                print("Botez played:", board_coordinate) 
                                print("Botez took %.2f to make a move" %(time() - start))
                            if GMHikaru_flag:
                                start = time()
                                board_coordinate = gm_hikaru_ai.find_best_move(board=game.board, turn=game.turn, white=game.white, black=game.black)
                                print("Hikaru played:", board_coordinate)      
                                print("GMHikaru took %.2f to make a move" %(time() - start))
                        game.place_tile(board_coordinate)
                    elif GMHikaru_flag and Botez_flag: # ai vs ai
                        if game.turn == "w": # GM Hikaru plays
                            start = time()
                            board_coordinate = gm_hikaru_ai.find_best_move(board=game.board, turn=game.turn, white=game.white, black=game.black)
                            print("Hikaru played:", board_coordinate)   
                            print("GMHikaru took %.2f to make a move" %(time() - start))
                            game.place_tile(board_coordinate)
                        if game.turn == "b": # Botez plays
                            start = time()
                            board_coordinate = botez_ai.find_best_move(board=game.board, turn=game.turn, white=game.white, black=game.black)
                            print("Botez played:", board_coordinate)
                            print("Botez took %.2f to make a move" %(time() - start))
                            game.place_tile(board_coordinate)       
                game.update_state()
                if game.state == "In progress":
                    game.switch_turn()
                    continue
                elif game.state == "Black wins":
                    print_black_wins()
                    print_board(game.board)
                    print("Black:", game.black_count)
                    print("White:", game.white_count)
                    print("Game time: %.2f" %(time() - game_time))
                    break
                elif game.state == "White wins":
                    print_white_wins()
                    print_board(game.board)
                    print("Black:", game.black_count)
                    print("White:", game.white_count)
                    print("Game time: %.2f" %(time() - game_time))
                    break
                elif game.state == "Tie":
                    print_draw_screen()
                    print_board(game.board)
                    print("Black:", game.black_count)
                    print("White:", game.white_count)
                    print("Game time: %.2f" %(time() - game_time))
                    break     
        else:
            break
        break


if __name__ == "__main__":
    main()
