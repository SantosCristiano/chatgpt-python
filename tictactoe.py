from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class TicTacToeApp(App):
    def build(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

        self.layout = GridLayout(cols=3)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = Button(font_size=32,
                                            on_press=lambda x, row=i, col=j: self.on_button_press(row, col))
                self.layout.add_widget(self.buttons[i][j])

        return self.layout

    def on_button_press(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].text = self.current_player
            if self.check_winner(self.current_player):
                self.show_popup(f"Player {self.current_player} wins!")
            elif self.check_draw():
                self.show_popup("It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.ai_move()

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.on_button_press(best_move[0], best_move[1])

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        if self.check_winner('X'):
            return -1
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for row in self.board:
            if all(s == player for s in row):
                return True
        for col in range(3):
            if all(row[col] == player for row in self.board):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(cell != ' ' for row in self.board for cell in row)

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
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].text = ''
        popup.dismiss()


if __name__ == '__main__':
    TicTacToeApp().run()
