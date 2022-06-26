#Board object
import re
import random

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #Create the board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        #initicalize a set to keep track of which locations we've dug
        #it will be (row, col) tuples
        self.dug = set()

    def make_new_board(self):
        #construct a new board based on the dim size and num bombs
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                #this means we've actually planted a bomb there already so keep going 
                continue
            board[row][col] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        #assign a number 0-8 for all the empty spaces
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self, row, col):
        #top left: (row-1, col-1)
        #top middle: (row-1, col)
        #top right: (row-1, col+1)
        #left: (row, col-1)
        #right: (row, col+1)
        #bottom left: (row+1, col-1)
        #bottom middle: (row+1, col)
        #bottom right: (row+1, col+1)

        num_neighboring_boms = 0
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_boms += 1

        return num_neighboring_boms

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        #if self.board[row][col] == 0 then recursively dig neighbors!
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c) #don't dig where you've already dug

        return True

    def __str__(self):
        #return a string that shows the board to the player
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep            


#play the game 
def play(dim_size=10, num_bombs=10):
    #Step 1: create the board and plant the bombs 
    board = Board(dim_size, num_bombs)
    #Step 2: show the user the board and ask for where they want to dig
    #Step 3a: if location is a bomb, show gameover message
    #Step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    #Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True
    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invaild location. Try again")
            continue

        safe = board.dig(row, col)
        if not safe:
            #dug a bomb
            break

    if safe:
        print("Congratualtions! You won!")
    else:
        print("Sorry game over!")

        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()
    