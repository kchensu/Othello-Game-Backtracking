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
        self.legal_moves = None
    
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
                          
                    north_west = self.check_valid_moves(-1, -1, row, col)
                    north_east = self.check_valid_moves(-1,  1, row, col)
                    north      = self.check_valid_moves(-1,  0, row, col)

                    south_west = self.check_valid_moves( 1, -1, row, col)
                    south_east = self.check_valid_moves( 1,  1, row, col)
                    south      = self.check_valid_moves( 1,  0, row, col)

                    west       = self.check_valid_moves( 0, -1, row, col)
                    east       = self.check_valid_moves( 0,  1, row, col)
                
                    if (north_west or north_east or north or south_east or south_west or south or west or east):
                        valid.append(np.array([row, col]))
                        # valid[row][col] = self.turn

                        # for i in range(8):
                        #     for j in range(8):
                        #         print(valid[i][j], end= " ")
                        #     print(end= '\n')
        self.legal_moves = np.array(valid)
        return valid

    def check_valid_moves(self, delta_row, delta_col, row , col): 

        other = None
        if (self.turn == 'b'):
            other = 'w'
        elif(self.turn == 'w'):
            other = 'b'
        else:
            return False
        
        # check for bounds in the board
        if (row + delta_row < 0) or (row + delta_row >= 8):
            return False

        if (col  + delta_col < 0) or (col + delta_col >= 8):
            return False
        
        # check if position at row, col contains the opposite of "turn" on the board
        if self.board[row + delta_row][col + delta_col] != other :
            return False
        # check if two position away doesn't end up outside bounds
        if (row + delta_row + delta_row < 0) or (row + delta_row + delta_row >= 8):
            return False
        if (col + delta_col + delta_col < 0) or (col + delta_col + delta_col >= 8):
            return False
       
        return self.check_line(delta_row, delta_col, row + delta_row + delta_row, col + delta_col + delta_col)        
        # check if the line matches the color

    def check_line(self, delta_row, delta_col, row, col):
        
        if (self.board[row][col] == self.turn):
            return True
        if row + delta_row < 0 or row + delta_row >= 8:
            return False
        if col + delta_col < 0 or col + delta_col >= 8:
            return False
        if self.board[row][col] == " ":
            return False

        return self.check_line(delta_row, delta_col, row + delta_row, col + delta_col)
    
    def flip_token(self, row, col):
      
        self.flip_line(-1, -1, row, col)
        self.flip_line(-1,  1, row, col)
        self.flip_line(-1,  0, row, col)
        self.flip_line( 1, -1, row, col)
        self.flip_line( 1,  1, row, col)
        self.flip_line( 1,  0, row, col)
        self.flip_line( 0, -1, row, col)
        self.flip_line( 0,  1, row, col)
     
    
    def flip_line(self, delta_row, delta_col, row, col):
  
        if row + delta_row < 0 or row + delta_row >= 8:
            return False
        if col + delta_col < 0 or col + delta_col >= 8:
            return False
        if self.board[row + delta_row][col + delta_col] == " ":
            return False
        if self.board[row + delta_row][col + delta_col] == self.turn:
            return True
        else:
            if self.flip_line(delta_row, delta_col, row + delta_row, col + delta_col):
                self.board[row + delta_row][col + delta_col] = self.turn
                return True
            else:
                return False
    
    def is_move_valid(self, coords):
        legal_moves = self.find_legal_positions()
        if coords in legal_moves:
            return True
        else:
            return False

    def place_tile(self, coords):
        self.board[coords[0]][coords[1]] = self.turn
        
        self.flip_token(coords[0], coords[1])

    def switch_turn(self):
        if self.turn == 'b':
            self.turn = 'w'
        elif self.turn == 'w':
            self.turn = 'b'
    
    def update_state(self):
        if len(self.legal_moves) != 0:
            self.state = self.GAME_STATES['IN_PROGRESS']
        else:
            black_count = 0
            white_count = 0

            for tile in self.board:
                if tile == " ":
                    continue
                elif tile == 'b':
                    black_count += 1
                elif tile == 'w':
                    white_count += 1
            if black_count > white_count:
                self.state = self.GAME_STATES['BLACK_WINS']
            elif white_count > black_count:
                self.state = self.GAME_STATES['WHITE_WINS']
            elif white_count == black_count:
                self.state = self.GAME_STATES['TIE']
    
    def is_move_valid(self, coords):
        for valid_coord in self.legal_moves:
            if coords[0] == valid_coord[0]:
                if coords[1] == valid_coord[1]:
                    return True
                else:
                    continue
            else:
                continue
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
    initial_board = np.array([              [" ", " ", " ", " ", " ", " ", "b", "w"], 
                                            [" ", " ", " ", " ", " ", " ", "b", " "], 
                                            [" ", " ", " ", " ", " ", "w", "b", " "], 
                                            [" ", " ", " ", "w", "w", "w", "w", "w"], 
                                            [" ", " ", "w", "w", "w", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "], 
                                            [" ", " ", " ", " ", " ", " ", " ", " "]])
    
    test = Reversi(initial_board, 'b')
    test.find_legal_positions()
    print(test.find_legal_positions())
    print(test.is_move_valid([0 ,0]))
    test.place_tile([5, 2])
    print_board(test.board)
    test.switch_turn()
   
    # test.place_tile([0,5])
    # print_board(test.board)
    # test.switch_turn()
    # test.place_tile([4,5])
    # print_board(test.board)
    # print(test.find_legal_positions())

   


if __name__ == "__main__":
    main()




    



