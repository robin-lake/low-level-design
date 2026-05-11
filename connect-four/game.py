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
    def make_move(self, col):
        val = self.current_player.color[0]
        result = self.board.insert_piece(int(col) - 1, val)
        if result == False:
           return "illegal move, try again" 
        else:
            print(result)
            win = self.board.check_for_win(result[0], result[1], game.current_player.color)
            print('win: ', win)
            if win:
                self.winner = self.current_player
                return print(f"{self.current_player.color} player won the match")
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
    def insert_piece(self, col, val) -> bool or [int, int]:
        row = len(self.board) - 1
        while row > 0:
            if self.board[row][col] == 0:
                break
            else:
                row -= 1

        if row > len(self.board) or col > len(self.board[0]) or self.board[row][col] != 0:
            return False
        self.board[row][col] = val 
        return [row, col] 
    def check_for_win(self, row, col, color) -> bool:
        directions = [[0,1], [1,0], [1,1], [-1,1]]
        print('row, col, color: ', row, col, color)
        for rd, rc in directions:
            count = 1
            count += self.count_direction(row, col, rd, rc, color)
            count += self.count_direction(row, col, -rd, -rc, color)
            if count >= 4:
                return True
            print('count: ', count)
        return False
    def count_direction(self, row, col, rd, cd, color) -> int:
        count = 0
        r = row + rd
        c = col + cd
        # print('r, c: ', r, c)
        while self.in_bounds(r, c) and self.board[r][c] == color[0]:
        # print('self.board[r][c]: ', self.board[r][c])
        # print('color[0]: ', color[0])
            # print('foo')
            count += 1
            r += rd
            c += cd
        # print('internal count: ', count)
        return count
    def in_bounds(self, row, col) -> bool:
        if row >= len(self.board) or col >= len(self.board[0]) or row < 0 or col < 0:
            return False
        return True


game = Game()

while game.winner is False:
    print(f"{game.current_player.color}'s turn")
    col = input("enter column")
    try:
        val = int(col)
        print(game.make_move(col))
    except:
        print("invalid move, try again")
        continue

    print(game.board.show_board())
