import tkinter as tk
from tkinter import messagebox
from sudoku import Sudoku


class SudokuGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.sudoku = Sudoku(board_size)
        self.solution = [[self.sudoku.board[i][j] for j in range(board_size)] for i in range(board_size)]
        self.num_cells_to_fill = sum([row.count(0) for row in self.sudoku.board])
        self.num_cells_filled = self.board_size ** 2 - self.num_cells_to_fill
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title(f"{self.board_size}x{self.board_size} Sudoku")
        self.root.geometry("600x600")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame_board = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_board.pack(side="top", padx=5, pady=5)
        self.create_board()
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(side="top", padx=5, pady=5)
        tk.Button(self.frame_buttons, text="Solve", command=self.solve).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame_buttons, text="Clear", command=self.clear).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.frame_buttons, text="New Game", command=self.new_game).grid(row=0, column=2, padx=5, pady=5)
        self.var_board = tk.StringVar(value=f"{self.board_size}x{self.board_size}")
        tk.OptionMenu(self.frame_buttons, self.var_board, f"{self.board_size}x{self.board_size}", "4x4", "6x6",
                      command=self.select_board_size).grid(row=0, column=3, padx=5, pady=5)

    def create_board(self):
        self.cells = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                cell_value = self.sudoku.board[i][j]
                if cell_value == 0:
                    cell = tk.Entry(self.frame_board, width=2, font=("Arial", 16), justify="center", validate="key",
                                    validatecommand=(self.root.register(self.is_valid), "%P"))
                    cell.insert(0, "")
                    cell.bind("<FocusIn>", lambda event, row=i, col=j: self.on_click(row, col))
                    cell.bind("<FocusOut>", lambda event, row=i, col=j: self.on_leave(row, col))
                    cell.bind("<KeyRelease>", lambda event, row=i, col=j: self.on_key_release(row, col))
                    cell.grid(row=i, column=j, padx=1, pady=1)
                    row.append(cell)
                else:
                    cell = tk.Label(self.frame_board, text=cell_value, font=("Arial", 16), bg="white", relief="solid")
                    cell.grid(row=i, column=j, padx=1, pady=1)
                    row.append(cell)
            self.cells.append(row)

    def select_board_size(self, event):
        self.root.destroy()
        if self.var_board.get() == "4x4":
            game = SudokuGame(4)
        elif self.var_board.get() == "6x6":
            game = SudokuGame(6)
        elif self.var_board.get() == "9x9":
            game = SudokuGame(9)
        else:
            game = SudokuGame(9)
        game.root.mainloop()

    def is_valid(self, value):
        if value == "":
            return True
        if not value.isdigit():
            return False
        if int(value) < 1 or int(value) > self.board_size:
            return False
        return True

    def on_click(self, row, col):
        cell = self.cells[row][col]
        cell.config(bg="light blue")

    def on_leave(self, row, col):
        cell = self.cells[row][col]
        cell.config(bg="white")

    def on_key_release(self, row, col):
        cell = self.cells[row][col]
        value = cell.get()
        if self.is_valid(value):
            self.sudoku.board[row][col] = int(value)
        else:
            self.sudoku.board[row][col] = 0

    def solve(self):
        self.solution = [[self.sudoku.board[i][j] for j in range(self.board_size)] for i in range(self.board_size)]
        if self.sudoku.solve(self.solution):
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.cells[i][j].winfo_class() == "Entry":
                        self.cells[i][j].delete(0, tk.END)
                        self.cells[i][j].insert(0, str(self.solution[i][j]))
                        self.cells[i][j].config(fg="red")
            self.num_cells_filled = self.board_size ** 2
        else:
            messagebox.showwarning("Sudoku Solver", "The puzzle cannot be solved.")

    def clear(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.cells[i][j].winfo_class() == "Entry":
                    self.cells[i][j].delete(0, tk.END)
                    self.sudoku.board[i][j] = 0
            self.num_cells_filled = 0

    def new_game(self):
        self.root.destroy()
        if self.board_size == 4:
            game = SudokuGame(4)
        elif self.board_size == 6:
            game = SudokuGame(6)
        else:
            game = SudokuGame(9)
        game.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Sudoku", "Do you want to quit?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()
