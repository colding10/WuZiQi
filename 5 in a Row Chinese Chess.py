import tkinter as tk
from tkinter import font
import tkinter.messagebox as msg
import random

class Bot:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        return

    def checkWonDiagonalLeft(self, current_color, location):
        diagonal_left = 1
        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                up_left_x = current_index_x - 1
                up_left_y = current_index_y - 1

                if up_left_x < 0 or up_left_y < 0:
                    break

                next_color = self.board_array[up_left_y][up_left_x].cget('fg')
                
                if next_color == 'blue':
                    break
                
                if next_color == current_color:
                    diagonal_left += 1
                    
                    current_index_x -= 1
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_right_x = current_index_x + 1
                down_right_y = current_index_y + 1

                if down_right_x < 0 or down_right_y < 0:
                    break

                next_color = self.board_array[down_right_y][down_right_x].cget('fg')
                
                if next_color == current_color:
                    diagonal_left += 1
                    
                    current_index_x -= 1
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        return diagonal_left

    def checkWonDiagonalRight(self, current_color, location):
        diagonal_right = 1
        current_index_x, current_index_y = location

        for _ in range(self.dimensions ** 2):
            try:
                up_right_x = current_index_x + 1
                up_right_y = current_index_y - 1

                if up_right_x < 0 or up_right_y < 0:
                    break

                next_color = self.board_array[up_right_y][up_right_x].cget('fg')
                
                if next_color == current_color:
                    diagonal_right += 1
                    
                    current_index_x += 1
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_right_x = current_index_x - 1
                down_right_y = current_index_y + 1

                if down_right_x < 0 or down_right_y < 0:
                    break

                next_color = self.board_array[down_right_y][down_right_x].cget('fg')
                
                if next_color == current_color:
                    diagonal_right += 1
                    
                    current_index_x -= 1
                    current_index_y += 1
                else:
                    break
                    
            except IndexError:
                break

        return diagonal_right

    def checkWonUpDown(self, current_color, location):
        up_down = 1
        current_index_x, current_index_y = location

        for _ in range(self.dimensions ** 2):
            try:
                up_x = current_index_x + 0
                up_y = current_index_y - 1

                if up_x < 0 or up_y < 0:
                    break

                next_color = self.board_array[up_y][up_x].cget('fg')
                
                if next_color == current_color:
                    up_down += 1
                    
                    current_index_x += 0
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_x = current_index_x + 0
                down_y = current_index_y + 1

                if down_x < 0 or down_y < 0:
                    break

                next_color = self.board_array[down_y][down_x].cget('fg')
                
                if next_color == current_color:
                    up_down += 1
                    
                    current_index_x += 0
                    current_index_y += 1
                else:
                    break
                    
            except IndexError:
                break

        return up_down

    def checkWonLeftRight(self, current_color, location):
        left_right = 1
        current_index_x, current_index_y = location

        for _ in range(self.dimensions ** 2):
            try:
                left_x = current_index_x - 1
                left_y = current_index_y - 0

                if left_x < 0 or left_y < 0:
                    break

                next_color = self.board_array[left_y][left_x].cget('fg')
                
                if next_color == current_color:
                    left_right += 1
                    
                    current_index_x -= 1
                    current_index_y += 0
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_x = current_index_x + 1
                down_y = current_index_y - 0

                if down_x < 0 or down_y < 0:
                    break

                next_color = self.board_array[down_y][down_x].cget('fg')
                
                if next_color == current_color:
                    left_right += 1
                    
                    current_index_x += 1
                    current_index_y -= 0
                else:
                    break
                    
            except IndexError:
                break

        return left_right
    
    def checkWon(self, piece_location):
        x_index, y_index = piece_location
        
        current_color = self.board_array[y_index][x_index].cget('fg')

        diagonal_left = self.checkWonDiagonalLeft(current_color, piece_location)
        diagonal_right = self.checkWonDiagonalRight(current_color, piece_location)
        up_down = self.checkWonUpDown(current_color, piece_location)
        left_right = self.checkWonLeftRight(current_color, piece_location)

        #print(diagonal_left, diagonal_right, up_down, left_right)
        
        if diagonal_left >= self.required_in_a_row:
            return (True, 'dl')
        if diagonal_right >= self.required_in_a_row:
            return (True, 'dr')
        if up_down >= self.required_in_a_row:
            return (True, 'ud')
        if left_right >= self.required_in_a_row:
            return (True, 'lr')
        
        return (False, 'j')

    def calculateMove(self, board, last_placed):
        self.board_array = board
        for num in range(4, 1, -1):
            self.required_in_a_row = num

            res = self.checkWon(last_placed)

            if res[0]:
                type = res[1]
                print(res)
                if type == 'dl':
                    try:
                        next_spot = [last_placed[0] + 1, last_placed[1] + 1]
                        if '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            next_spot = [last_placed[0] - 1, last_placed[1] - 1]
                        if not '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            return next_spot
                    except IndexError:
                        pass
                if type == 'dr':
                    try:
                        next_spot = [last_placed[0] + 1, last_placed[1] - 1]
                        if '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            next_spot = [last_placed[0] - 1, last_placed[1] + 1]
                        if not '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            return next_spot
                    except IndexError:
                        pass
                if type == 'ud':
                    try:
                        next_spot = [last_placed[0] - 1, last_placed[1] + 0]
                        if '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            next_spot = [last_placed[0] + 1, last_placed[1] - 0]
                        if not '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            return next_spot
                    except IndexError:
                        pass
                if type == 'lr':
                    try:
                        print(last_placed)
                        next_spot = [last_placed[0] - 0, last_placed[1] + 1]
                        if '*' in board[next_spot[0]][next_spot[1]].cget('text'):
                            next_spot = [last_placed[0] + 0, last_placed[1] - 1]
                        if '*' not in board[next_spot[0]][next_spot[1]].cget('text'):
                            print(next_spot)
                            return next_spot
                    except IndexError:
                        pass
        
        while True:
            out = [random.randint(0, self.dimensions-1), random.randint(0, self.dimensions-1)]
            if '*' not in self.board_array[out[0]][out[1]].cget('text'):
                return out
        
class Main:
    def __init__(self, dimensions=50, required_in_a_row=5, bot=True, theme=['gray', 'dark gray']):
        self.theme = theme[:-1]
        self.dimensions = dimensions
        self.required_in_a_row = required_in_a_row
        
        self.window = tk.Tk()
        self.window.aspect(1, 1, 1, 1)
        self.window.resizable(True, True)
        self.window.geometry('700x700')
        self.window.config(bg=theme[-1])
        self.window.title('5 in a Row Chinese Chess | It\'s White\'s turn!') 
        #self.window.bind('<Configure>', self.windowResized)

        self.board_array = [[_ for _ in range(dimensions)] for _ in range(dimensions)]

        self.gameover = False
        self.move = 0

        self.bot = bot
        self.bot_class = Bot(dimensions)

    def run(self):
        for rows in range(self.dimensions):
            tk.Grid.rowconfigure(self.window, rows, weight=1)
            tk.Grid.columnconfigure(self.window, rows, weight=1)

        self.window.protocol('WM_DELETE_WINDOW', self.onClosing)
        self.createGrid()
        self.window.after(250, self.windowResized)
        self.window.mainloop()

    def windowResized(self, event=None):
        if not event:
            for widget in self.window.winfo_children():
                widget.config(font = ('Courier', 18))
            return

        for widget in self.window.winfo_children():
            widget.config(font = ('Courier', int((event.width/700)*18)))

    def onClosing(self):
        if not self.gameover:
            self.window.destroy()

        if not msg.askyesno(title='5 in a Row Chinese Chess', message='Play again?'):
            self.window.destroy()
        else:
            app = Main(dimensions=self.dimensions, required_in_a_row=self.required_in_a_row)
            app.run()
                  
    def createGrid(self):
        colors = self.theme
        index = 0
        
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                button_widget = tk.Label(self.window, text='   ', font=('Courier', 18), bg = colors[index % 2], fg = 'blue')
                button_widget.bind('<Button-1>', self.handleClick)
                button_widget.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
                self.board_array[row][col] = button_widget

                index += 1
                    
            index += 1

    def botMove(self, location):
        self.window.title(f'5 in a Row Chinese Chess | Bot is thinking...')
        next_move = self.bot_class.calculateMove(self.board_array, location)
        next_move.reverse()
        self.board_array[next_move[0]-1][next_move[1]-1].config(text=' * ', fg='black')
        self.move += 1
        self.window.title(f'5 in a Row Chinese Chess | It\'s your turn!')

        if self.checkWon(location):
            person_won = 'Black' if not self.move % 2 else 'White'
            won_string = f'5 in a Row Chinese Chess | {person_won} won!'

            self.window.title(won_string)
            
            self.window.unbind_all('<Button-1>')
            for child in self.window.winfo_children():
                child.unbind('<Button-1>')

            self.gameover = True
            return

    def handleClick(self, event=None):
        if self.gameover:
            return

        location = [0, 0]

        done = False
        for row_index, row in enumerate(self.board_array):
            for item_index, item in enumerate(row):
                if item == event.widget:
                    location = [row_index, item_index]
                    done = True
                    break
                if done:
                    break
        

        if event.widget.cget('text') != '   ':
            return
        
        if not self.move % 2:
            fg = 'white'
        else:
            fg = 'black'

        location.reverse()
        event.widget.config(text=' * ', fg=fg)
        self.move += 1

        if self.checkWon(location):
            person_won = 'Black' if not self.move % 2 else 'White'
            won_string = f'5 in a Row Chinese Chess | {person_won} won!'

            self.window.title(won_string)
            
            self.window.unbind_all('<Button-1>')
            for child in self.window.winfo_children():
                child.unbind('<Button-1>')

            self.gameover = True
            return
        
        if self.bot:
            self.botMove(location)

        if self.checkWon(location):
            person_won = 'Black' if not self.move % 2 else 'White'
            won_string = f'5 in a Row Chinese Chess | {person_won} won!'

            self.window.title(won_string)
            
            self.window.unbind_all('<Button-1>')
            for child in self.window.winfo_children():
                child.unbind('<Button-1>')

            self.gameover = True
            return

    def checkWonDiagonalLeft(self, current_color, location):
        diagonal_left = 1
        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                up_left_x = current_index_x - 1
                up_left_y = current_index_y - 1

                if up_left_x < 0 or up_left_y < 0:
                    break

                next_color = self.board_array[up_left_y][up_left_x].cget('fg')
                
                if next_color == 'blue':
                    break
                
                if next_color == current_color:
                    diagonal_left += 1
                    
                    current_index_x -= 1
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_right_x = current_index_x + 1
                down_right_y = current_index_y + 1

                if down_right_x < 0 or down_right_y < 0:
                    break

                next_color = self.board_array[down_right_y][down_right_x].cget('fg')
                
                if next_color == current_color:
                    diagonal_left += 1
                    
                    current_index_x -= 1
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        return diagonal_left

    def checkWonDiagonalRight(self, current_color, location):
        diagonal_right = 1
        current_index_x, current_index_y = location

        for _ in range(self.dimensions ** 2):
            try:
                up_right_x = current_index_x + 1
                up_right_y = current_index_y - 1

                if up_right_x < 0 or up_right_y < 0:
                    break

                next_color = self.board_array[up_right_y][up_right_x].cget('fg')
                
                if next_color == current_color:
                    diagonal_right += 1
                    
                    current_index_x += 1
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_right_x = current_index_x - 1
                down_right_y = current_index_y + 1

                if down_right_x < 0 or down_right_y < 0:
                    break

                next_color = self.board_array[down_right_y][down_right_x].cget('fg')
                
                if next_color == current_color:
                    diagonal_right += 1
                    
                    current_index_x -= 1
                    current_index_y += 1
                else:
                    break
                    
            except IndexError:
                break

        return diagonal_right

    def checkWonUpDown(self, current_color, location):
        up_down = 1
        current_index_x, current_index_y = location

        for _ in range(self.dimensions ** 2):
            try:
                up_x = current_index_x + 0
                up_y = current_index_y - 1

                if up_x < 0 or up_y < 0:
                    break

                next_color = self.board_array[up_y][up_x].cget('fg')
                
                if next_color == current_color:
                    up_down += 1
                    
                    current_index_x += 0
                    current_index_y -= 1
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_x = current_index_x + 0
                down_y = current_index_y + 1

                if down_x < 0 or down_y < 0:
                    break

                next_color = self.board_array[down_y][down_x].cget('fg')
                
                if next_color == current_color:
                    up_down += 1
                    
                    current_index_x += 0
                    current_index_y += 1
                else:
                    break
                    
            except IndexError:
                break

        return up_down

    def checkWonLeftRight(self, current_color, location):
        left_right = 1
        current_index_x, current_index_y = location

        for _ in range(self.dimensions ** 2):
            try:
                left_x = current_index_x - 1
                left_y = current_index_y - 0

                if left_x < 0 or left_y < 0:
                    break

                next_color = self.board_array[left_y][left_x].cget('fg')
                
                if next_color == current_color:
                    left_right += 1
                    
                    current_index_x -= 1
                    current_index_y += 0
                else:
                    break
                    
            except IndexError:
                break

        current_index_x, current_index_y = location
        for _ in range(self.dimensions ** 2):
            try:
                down_x = current_index_x + 1
                down_y = current_index_y - 0

                if down_x < 0 or down_y < 0:
                    break

                next_color = self.board_array[down_y][down_x].cget('fg')
                
                if next_color == current_color:
                    left_right += 1
                    
                    current_index_x += 1
                    current_index_y -= 0
                else:
                    break
                    
            except IndexError:
                break

        return left_right
    
    def checkWon(self, piece_location):
        x_index, y_index = piece_location
        
        current_color = self.board_array[y_index][x_index].cget('fg')

        diagonal_left = self.checkWonDiagonalLeft(current_color, piece_location)
        diagonal_right = self.checkWonDiagonalRight(current_color, piece_location)
        up_down = self.checkWonUpDown(current_color, piece_location)
        left_right = self.checkWonLeftRight(current_color, piece_location)

        #print(diagonal_left, diagonal_right, up_down, left_right)
        
        if diagonal_left >= self.required_in_a_row or diagonal_right >= self.required_in_a_row:
            return True
        if up_down >= self.required_in_a_row or left_right >= self.required_in_a_row:
            return True
        
        return False
    
if __name__ == '__main__':
    themes = \
           {
               'theme1': ['gray', 'dark gray', 'black'],
               'theme2': ['blue', 'red', 'yellow']
            }
    
    app = Main(dimensions=20, required_in_a_row=5, bot=True, theme=themes['theme1'])
    app.run()
