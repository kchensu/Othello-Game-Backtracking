import numpy as np

class Reversi:
    GAME_STATES = {
        "IN_PROGRESS": 'In progress',
        "BLACK_WINS": 'Black wins',
        "WHITE_WINS": 'White wins',
        "TIE": 'Tie'
    }
    
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
        self.state = self.GAME_STATES['IN_PROGRESS']
    
    def find_legal_positions(self):
        # valid = ([  [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "], 
        #             [" ", " ", " ", " ", " ", " ", " ", " "]])
        valid = [] 

     
        for row in range(8):
            for col in range(8):
                if (self.board[row][col] == " "):
                    north_west = self.check_valid_moves(self.turn, -1, -1, row, col, self.board)
                    north_east = self.check_valid_moves(self.turn, -1,  1, row, col, self.board)
                    north      = self.check_valid_moves(self.turn, -1,  0, row, col, self.board)

                    south_west = self.check_valid_moves(self.turn,  1, -1, row, col, self.board)
                    south_east = self.check_valid_moves(self.turn,  1,  1, row, col, self.board)
                    south      = self.check_valid_moves(self.turn,  1,  0, row, col, self.board)

                    west       = self.check_valid_moves(self.turn,  0, -1, row, col, self.board)
                    east       = self.check_valid_moves(self.turn,  0,  1, row, col, self.board)
                
                    if (north_west or north_east or north or south_east or south_west or south or west or east):
                        valid.append(np.array([row, col]))
                        # valid[row][col] = self.turn

                        # for i in range(8):
                        #     for j in range(8):
                        #         print(valid[i][j], end= " ")
                        #     print(end= '\n')
        # print(valid)
        return valid

    def check_valid_moves(self, turn, delta_row, delta_col, row , col, board): 

        other = None
        if (turn == 'b'):
            other = 'w'
        elif(turn == 'w'):
            other = 'b'
        else:
            return False
        
        # check for bounds in the board
        if (row + delta_row < 0) or (row + delta_row >= 8):
            return False

        if (col  + delta_col < 0) or (col + delta_col >= 8):
            return False
        
        # check if position at row, col contains the opposite of "turn" on the board
        if board[row + delta_row][col + delta_col] != other :
            return False
        # check if two position away doesn't end up outside bounds
        if (row + delta_row + delta_row < 0) or (row + delta_row + delta_row >= 8):
            return False
        if (col + delta_col + delta_col < 0) or (col + delta_col + delta_col >= 8):
            return False
        return self.check_line(turn, delta_row, delta_col, row + delta_row + delta_row, col + delta_col + delta_col, board)        
        # check if the line matches the color

    def check_line(self, turn, delta_row, delta_col, row, col, board):

        if (self.board[row][col] == turn):
            return True
        if row + delta_row < 0 or row + delta_row >= 8:
            return False
        if col + delta_col < 0 or col + delta_col >= 8:
            return False

        return self.check_line(turn, delta_row, delta_col, row + delta_row, col + delta_col, board)
    
    def flip_token(self, turn, row, col, board):

        flip_line(self.turn, -1, -1, row, col, self.board)
        flip_line(self.turn, -1,  1, row, col, self.board)
        flip_line(self.turn, -1,  0, row, col, self.board)
        flip_line(self.turn,  1, -1, row, col, self.board)
        flip_line(self.turn,  1,  1, row, col, self.board)
        flip_line(self.turn,  1,  0, row, col, self.board)
        flip_line(self.turn,  0, -1, row, col, self.board)
        flip_line(self.turn,  0,  1, row, col, self.board)
    
    def flip_line(self, turn, delta_row, delta_col, row, col, board):
        if row + delta_row < 0 or row + delta_row >= 8:
            return False
        if col + delta_col < 0 or col + delta_col >= 8:
            return False
        if board[row + delta_row][col + delta_col] != " ":
            return False
        if board[row + delta_row][col + delta_col] == turn:
            return True
        else:
            if self.flip_line(turn, delta_row, delta_col, row + delta_row, col + delta_col, board):
                board[row + delta][col + delta_col] = turn
                return True
            else:
                return False

def print_board(board):
    print("   0 1 2 3 4 5 6 7")
    print("0 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], board[0][6], board[0][7]))
    print("  -- ---- ---- ---- ---" )
    print( "1 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[1][0], board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], board[1][6], board[1][7]))
    print("  -- ---- ---- ---- ---" )
    print( "2 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[2][0], board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], board[2][6], board[2][7]))
    print("  -  ---  ---  ---  ---  ---  -")  
    print("3 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[3][0], board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], board[3][6], board[3][7]))
    print("  -  ---  ---  ---  ---  ---  -")  
    print("4 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[4][0], board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], board[4][6], board[4][7]))
    print("  -  ---  ---  ---  ---  ---  -")  
    print("5 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[5][0], board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], board[5][6], board[5][7]))
    print("  -  ---  ---  ---  ---  ---  -")  
    print("6 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[6][0], board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], board[6][6], board[6][7]))
    print("  -  ---  ---  ---  ---  ---  -")  
    print("7 |  %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s|" %(board[7][0], board[7][1], board[7][2], board[7][3], board[7][4], board[7][5], board[7][6], board[7][7]))
            


        

        
    
    



      




        
       

    



def main():
    initial_board = np.array([              [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", "b", "w", " ", " ", " "], 
                                            [" ", " ", " ", "w", "b", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "]])
    
    test = Reversi(initial_board, 'b')
    test.find_legal_positions()
    print_board(initial_board)


if __name__ == "__main__":
    main()




    



