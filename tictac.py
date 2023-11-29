class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None

    def print_board(self):
        for i in range(3):
            print(' ' + self.board[i*3] + ' | ' + self.board[i*3 + 1] + ' | ' + self.board[i*3 + 2])
            if i < 2:
                print('---+---+---')

    def available_moves(self):
        moves = []
        for i in range(len(self.board)):
            if self.board[i] == ' ':
                moves.append(i)
        return moves

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_win(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_win(self, square, letter):
        row_ind = square // 3
        row_win = True
        for i in range(row_ind * 3, (row_ind + 1) * 3):
            if self.board[i] != letter:
                row_win = False
                break
        if row_win:
            return True

        col_ind = square % 3
        col_win = True
        for i in range(col_ind, col_ind + 7, 3):
            if self.board[i] != letter:
                col_win = False
                break
        if col_win:
            return True

        if square % 2 == 0:  
            diagonal1_win = True
            diagonal2_win = True
            for i in [0, 4, 8]:
                if self.board[i] != letter:
                    diagonal1_win = False
                    break
            for i in [2, 4, 6]:
                if self.board[i] != letter:
                    diagonal2_win = False
                    break
            if diagonal1_win or diagonal2_win:
                return True

        return False

    def minimax(self, state, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        for square in range(9):
            if self.check_win(square, 'X'):
                return -10 + depth
            elif self.check_win(square, 'O'):
                return 10 - depth
        if ' ' not in state:
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in self.available_moves():
                state[i] = 'O'
                eval = self.minimax(state, depth + 1, False, alpha, beta)
                state[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i in self.available_moves():
                state[i] = 'X'
                eval = self.minimax(state, depth + 1, True, alpha, beta)
                state[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self):
        best_value = -1000
        best_move = -1

        for i in self.available_moves():
            self.board[i] = 'O'
            move_value = self.minimax(self.board, 0, False, float('-inf'), float('inf'))
            self.board[i] = ' '

            if move_value > best_value:
                best_value = move_value
                best_move = i

        return best_move


def play():
    game = TicTacToe()
    game.print_board()  # Print blank board before first turn
    while game.available_moves() and not game.current_winner:
        move = None
        while move not in game.available_moves():
            move_input = input('Enter position (1-9): ')
            try:
                move = int(move_input) - 1  # Adjust for 0-indexed board
                if move not in game.available_moves():
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")

        game.make_move(move, 'X')
        game.print_board()

        if game.current_winner:
            print('X wins!')
            return

        if game.available_moves() and not game.current_winner:
            print('\nAI is thinking...')
            o_move = game.find_best_move()
            if o_move != -1:
                game.make_move(o_move, 'O')
                game.print_board()

                if game.current_winner:
                    print('O wins!')
                    return

    print("It's a tie!")


play()
