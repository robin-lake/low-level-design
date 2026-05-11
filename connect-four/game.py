class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player('yellow')
        self.player2 = Player('red')
        self.winner = False
        self.current_player = self.player1
    def increment_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
    def make_move(self, row, col):
        val = self.current_player.color[0]
        result = self.board.insert_piece(row, col, val)
        if result == False:
           return "illegal move, try again" 
        else:
            self.increment_player()
            return "successful move, showing board"

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
    def insert_piece(self, row, col, val):
        r = int(row) - 1
        c = int(col) -1
        if r > len(self.board) or c > len(self.board[0]) or self.board[r][c] != 0:
            return False
        self.board[r][c] = val 
        return True


game = Game()

while game.winner is False:
    row = input("enter row")
    col = input("enter column")
    print(game.make_move(row, col))
    print(game.board.show_board())
    print(f"{game.current_player.color}'s turn")
