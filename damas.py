from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import copy

class CheckersApp(App):
    def build(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'R'  # 'R' for Red, 'B' for Black
        self.selected_piece = None  # Initialize selected piece

        self.layout = GridLayout(cols=8)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                self.buttons[i][j] = Button(font_size=24,
                                            on_press=lambda x, row=i, col=j: self.on_button_press(row, col))
                if (i + j) % 2 == 0:
                    self.buttons[i][j].background_color = [0, 0, 0, 1]  # Black
                else:
                    self.buttons[i][j].background_color = [1, 1, 1, 1]  # White
                self.layout.add_widget(self.buttons[i][j])

                # Set up initial pieces
                if (i % 2 != j % 2):
                    if i < 3:
                        self.board[i][j] = 'B'
                        self.buttons[i][j].text = 'B'
                    elif i > 4:
                        self.board[i][j] = 'R'
                        self.buttons[i][j].text = 'R'

        return self.layout

    def on_button_press(self, row, col):
        if self.board[row][col] == self.current_player:
            self.selected_piece = (row, col)
        elif self.selected_piece:
            if self.is_valid_move(self.selected_piece, (row, col)):
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
                self.current_player = 'R' if self.current_player == 'B' else 'B'
                if not self.has_moves(self.current_player):
                    self.show_popup(f"Player {self.current_player} has no moves! Game over.")
                elif self.current_player == 'B':
                    self.ai_move()

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        if self.board[end_row][end_col] is not None:
            return False

        if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            return True

        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            if self.board[mid_row][mid_col] and self.board[mid_row][mid_col] != self.current_player:
                return True

        return False

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        self.buttons[end_row][end_col].text = self.buttons[start_row][start_col].text
        self.buttons[start_row][start_col].text = ''

        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.board[mid_row][mid_col] = None
            self.buttons[mid_row][mid_col].text = ''

    def has_moves(self, player):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == player:
                    for d_row in [-1, 1]:
                        for d_col in [-1, 1]:
                            if self.is_valid_move((row, col), (row + d_row, col + d_col)):
                                return True
                            if self.is_valid_move((row, col), (row + 2 * d_row, col + 2 * d_col)):
                                return True
        return False

    def ai_move(self):
        best_move = self.get_best_move(self.board, 'B')
        if best_move:
            self.move_piece(best_move[0], best_move[1])
            self.current_player = 'R' if self.current_player == 'B' else 'B'
            if not self.has_moves(self.current_player):
                self.show_popup(f"Player {self.current_player} has no moves! Game over.")

    def get_best_move(self, board, player):
        best_score = -float('inf')
        best_move = None
        for start_row in range(8):
            for start_col in range(8):
                if board[start_row][start_col] == player:
                    for d_row in [-1, 1]:
                        for d_col in [-1, 1]:
                            if self.is_valid_move((start_row, start_col), (start_row + d_row, start_col + d_col)):
                                new_board = copy.deepcopy(board)
                                self.simulate_move(new_board, (start_row, start_col), (start_row + d_row, start_col + d_col))
                                score = self.minimax(new_board, 3, False)
                                if score > best_score:
                                    best_score = score
                                    best_move = ((start_row, start_col), (start_row + d_row, start_col + d_row))
                            if self.is_valid_move((start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col)):
                                new_board = copy.deepcopy(board)
                                self.simulate_move(new_board, (start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col))
                                score = self.minimax(new_board, 3, False)
                                if score > best_score:
                                    best_score = score
                                    best_move = ((start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col))
        return best_move

    def simulate_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = None

        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            board[mid_row][mid_col] = None

    def minimax(self, board, depth, is_maximizing):
        if depth == 0 or not self.has_moves('R') or not self.has_moves('B'):
            return self.evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            for start_row in range(8):
                for start_col in range(8):
                    if board[start_row][start_col] == 'B':
                        for d_row in [-1, 1]:
                            for d_col in [-1, 1]:
                                if self.is_valid_move((start_row, start_col), (start_row + d_row, start_col + d_col)):
                                    new_board = copy.deepcopy(board)
                                    self.simulate_move(new_board, (start_row, start_col), (start_row + d_row, start_col + d_col))
                                    eval = self.minimax(new_board, depth - 1, False)
                                    max_eval = max(max_eval, eval)
                                if self.is_valid_move((start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col)):
                                    new_board = copy.deepcopy(board)
                                    self.simulate_move(new_board, (start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col))
                                    eval = self.minimax(new_board, depth - 1, False)
                                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for start_row in range(8):
                for start_col in range(8):
                    if board[start_row][start_col] == 'R':
                        for d_row in [-1, 1]:
                            for d_col in [-1, 1]:
                                if self.is_valid_move((start_row, start_col), (start_row + d_row, start_col + d_col)):
                                    new_board = copy.deepcopy(board)
                                    self.simulate_move(new_board, (start_row, start_col), (start_row + d_row, start_col + d_col))
                                    eval = self.minimax(new_board, depth - 1, True)
                                    min_eval = min(min_eval, eval)
                                if self.is_valid_move((start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col)):
                                    new_board = copy.deepcopy(board)
                                    self.simulate_move(new_board, (start_row, start_col), (start_row + 2 * d_row, start_col + 2 * d_col))
                                    eval = self.minimax(new_board, depth - 1, True)
                                    min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, board):
        score = 0
        for row in board:
            for piece in row:
                if piece == 'B':
                    score += 1
                elif piece == 'R':
                    score -= 1
        return score

    def show_popup(self, message):
        layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=message, font_size=24)
        close_button = Button(text='Close', size_hint=(1, 0.25), font_size=24)
        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title='Game Over', content=layout, size_hint=(0.75, 0.5))
        popup.open()

        close_button.bind(on_press=lambda x: self.reset_game(popup))

    def reset_game(self, popup):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'R'
        self.selected_piece = None  # Reset selected piece
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].text = ''
                if (i % 2 != j % 2):
                    if i < 3:
                        self.board[i][j] = 'B'
                        self.buttons[i][j].text = 'B'
                    elif i > 4:
                        self.board[i][j] = 'R'
                        self.buttons[i][j].text = 'R'
        popup.dismiss()

if __name__ == '__main__':
    CheckersApp().run()
