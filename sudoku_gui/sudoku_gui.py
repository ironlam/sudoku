import tkinter as tk
from tkinter import messagebox
from sudoku_board import SudokuBoard

# Define constants for grid sizes
GRID_SIZES = {
    '4x4': 4,
    '6x6': 6,
    '9x9': 9,
    '12x12': 12,
    '16x16': 16
}


class SudokuGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Sudoku')
        self.board = None
        self.buttons = []

        self.create_menu()
        self.create_board()
        self.create_buttons()

        self.window.mainloop()

    def create_menu(self):
        # Create a menu for selecting the grid size
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        grid_size_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Grid Size', menu=grid_size_menu)

        for size in GRID_SIZES:
            grid_size_menu.add_command(label=size, command=lambda s=size: self.change_grid_size(s))

        # Add a button for solving the puzzle
        menu.add_command(label='Solve', command=self.show_solution)

        # Add a button for resetting the puzzle
        menu.add_command(label='Reset', command=self.reset_board)

    def create_board(self):
        # Create the Sudoku board
        self.board = SudokuBoard(GRID_SIZES['9x9'])

        # Create a grid of Entry widgets for inputting the numbers
        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                e = tk.Entry(self.window, width=2, font=('Arial', 16, 'bold'), justify='center')
                e.grid(row=i, column=j)
                row.append(e)
            self.buttons.append(row)

    def create_buttons(self):
        # Add a button for showing the solution
        solve_button = tk.Button(self.window, text='Show Solution', command=self.show_solution, bg='red', fg='white')
        solve_button.grid(row=self.board.size, column=0, columnspan=self.board.size, sticky='ew')

        # Add a button for resetting the board
        reset_button = tk.Button(self.window, text='Reset', command=self.reset_board)
        reset_button.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, sticky='ew')

    def change_grid_size(self, size):
        # Reset the board and create a new board with the selected size
        self.reset_board()
        self.board = SudokuBoard(GRID_SIZES[size])

        # Remove the existing buttons and create new buttons for the new board
        for button_row in self.buttons:
            for button in button_row:
                button.destroy()
        self.buttons = []

        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                e = tk.Entry(self.window, width=2, font=('Arial', 16, 'bold'), justify='center')
                e.grid(row=i, column=j)
                row.append(e)
            self.buttons.append(row)

    def reset_board(self):
        self.board.reset()
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.buttons[i][j].delete(0, 'end')

    def get_board_values(self):
        # Convert the values in the Entry widgets to a 2D list of integers
        values = []
        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                e = self.buttons[i][j]
                try:
                    value = int(e.get())
                    if value < 0 or value > self.board.size:
                        raise ValueError
                    row.append(value)
                except ValueError:
                    row.append(0)
            values.append(row)
        return values

    def set_board_values(self, values):
        # Set the values in the Entry widgets from a 2D list of integers
        for i in range(self.board.size):
            for j in range(self.board.size):
                value = values[i][j]
                if value != 0:
                    self.buttons[i][j].delete(0, 'end')
                    self.buttons[i][j].insert(0, str(value))

    def show_solution(self):
        # Get the current values in the Entry widgets
        values = self.get_board_values()

        # Solve the Sudoku puzzle
        self.board.solve()
        solution = self.board.solution

        # Check if the solution matches the current values
        for i in range(self.board.size):
            for j in range(self.board.size):
                if solution[i][j] != values[i][j]:
                    messagebox.showerror('Incorrect Solution', 'The solution is incorrect.')
                    return

        # Show the solution in the Entry widgets
        self.set_board_values(solution)
