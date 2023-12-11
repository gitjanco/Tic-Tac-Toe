import time

class TicTacToe:
    def __init__(self):
        self.size = 5 
        self.board = [' '] * self.size**2
        self.current_winner = None
        self.winning_length = 4  

    def print_board(self):
        horizontal_sep = ("---+" * (self.size - 1)) + "---"
        for row in range(self.size):
            row_cells = ' | '.join(self.board[row*self.size:(row+1)*self.size])
            print(' ' + row_cells)
            if row < self.size - 1:
                print(horizontal_sep)

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
        # Horizontal
        row_start = (square // self.size) * self.size
        if all(self.board[row_start + i] == letter for i in range(self.winning_length)):
            return True

        # Vertical
        col_start = square % self.size
        if all(self.board[col_start + self.size * i] == letter for i in range(self.winning_length)):
            return True

        # Diagonal/top-left to bottom-right
        if square % (self.size + 1) == 0:
            if all(self.board[i] == letter for i in range(0, self.size * self.size, self.size + 1)):
                return True

        # Diagonal/top-right to bottom-left
        if square % (self.size - 1) == 0 and square != 0 and square != self.size**2 - 1:
            if all(self.board[i] == letter for i in range(self.size - 1, self.size**2 - 1, self.size - 1)):
                return True

        # No win
        return False

    def evaluate(self):
        score = 0
        # Evaluate rows
        for row in range(self.size):
            for col in range(self.size - self.winning_length + 1):
                line = self.board[row*self.size+col:row*self.size+col+self.winning_length]
                score += self.evaluate_line(line)

        # Evaluate columns
        for col in range(self.size):
            for row in range(self.size - self.winning_length + 1):
                line = [self.board[row*self.size+col+i*self.size] for i in range(self.winning_length)]
                score += self.evaluate_line(line)

        # Evaluate diagonals (top-left to bottom-right)
        for row in range(self.size - self.winning_length + 1):
            for col in range(self.size - self.winning_length + 1):
                line = [self.board[(row+i)*self.size + col+i] for i in range(self.winning_length)]
                score += self.evaluate_line(line)

        # Evaluate diagonals (top-right to bottom-left)
        for row in range(self.size - self.winning_length + 1):
            for col in range(self.winning_length - 1, self.size):
                line = [self.board[(row+i)*self.size + col-i] for i in range(self.winning_length)]
                score += self.evaluate_line(line)

        return score

    def evaluate_line(self, line):
        if line.count('O') == 3 and line.count(' ') == 1:
            return 10 
        elif line.count('X') == 3 and line.count(' ') == 1:
            return -10
        return 0
    
    def minimax(self, state, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or not self.available_moves() or self.current_winner:
            return self.evaluate()

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.available_moves():
                state[move] = 'O'
                eval = self.minimax(state, depth - 1, False, alpha, beta)
                state[move] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.available_moves():
                state[move] = 'X'
                eval = self.minimax(state, depth - 1, True, alpha, beta)
                state[move] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, max_depth=3):
        best_value = float('-inf')
        best_move = None

        # Use heuristic to pre-filter moves
        moves = self.heuristic_move_selection(self.available_moves())

        for move in moves:
            self.board[move] = 'O'
            move_value = self.minimax(self.board, max_depth, False, float('-inf'), float('inf'))
            self.board[move] = ' '

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move

    def heuristic_move_selection(self, moves):
        # Prioritize moves that can win the game or block opponent
        win_moves = []
        block_moves = []
        for move in moves:
            self.board[move] = 'O'
            if self.check_win(move, 'O'):
                win_moves.append(move)
            self.board[move] = 'X'
            if self.check_win(move, 'X'):
                block_moves.append(move)
            self.board[move] = ' '

        if win_moves:
            return win_moves
        elif block_moves:
            return block_moves

        # prioritize center and corners
        center_and_corners = [move for move in moves if move in [24, 0, 6, 42, 48]]
        if center_and_corners:
            return center_and_corners

        return moves

def play():
    game = TicTacToe()
    game.print_board()
    while game.available_moves() and not game.current_winner:
        move = None
        while move not in game.available_moves():
            move_input = input(f'Enter position (1-{game.size**2}): ')
            try:
                move = int(move_input) - 1
                if move not in game.available_moves():
                    print("Invalid move. Try again.")
            except ValueError:
                print(f"Invalid input. Please enter a number between 1 and {game.size**2}.")
        game.make_move(move, 'X')
        game.print_board()
        if game.current_winner:
            print('X wins!')
            break

        print('\nAI is thinking...')
        start_time = time.time()
        o_move = game.find_best_move()
        end_time = time.time()
        print(f"AI took {end_time - start_time:.2f} seconds to make a move.")
        if o_move is not None:
            game.make_move(o_move, 'O')
            game.print_board()
            if game.current_winner:
                print('O wins!')
                break

    if not game.current_winner:
        print("It's a tie!")

play()
