class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player('yellow')
        self.player2 = Player('red')
        self.winner = False
class Player:
    def __init__(self, color):
        self.color = color
class Board:
    def __init__(self):
        self.board = [[0 for x in range(6)] for y in range(5)]
    def show_board(self):
        output = ""
        for i in range(len(self.board)):
            row = ", ".join(map(str, self.board[i]))
            output += row + '\n'
        return output
    def insert_piece(self, row, col):
        r = int(row) - 1
        c = int(col) -1
        if r > len(self.board) or c > len(self.board[0]) or self.board[r][c] != 0:
            return "illegal move, try again"
        self.board[r][c] = 'y'
        return "successful move, showing board"


game = Game()

while game.winner is False:
    row = input("enter row")
    col = input("enter column")
    print(game.board.insert_piece(row, col))
    print(game.board.show_board())
