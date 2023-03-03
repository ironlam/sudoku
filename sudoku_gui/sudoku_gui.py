import tkinter as tk
from tkinter import messagebox
from .utils import load_icon, create_dropdown_menu, get_board_canvas_size, get_board_cell_size, load_config
from sudoku_board import SudokuBoard


class SudokuGUI:

    def __init__(self, master=None):
        self.board_canvas = None
        self.master = master
        self.master.title("Sudoku")
        self.master.geometry("500x550")
        self.config = load_config()
        self.board_size = self.config["board_size"]
        self.cell_size = self.config["cell_size"]
        self.board_canvas_size = (self.cell_size * self.board_size + 4, self.cell_size * self.board_size + 4)
        self.board = SudokuBoard(self.board_size, self.config["puzzle_difficulty"])
        self.create_board()
        self.create_buttons()

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="New", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_toolbar(self):
        toolbar = tk.Frame(self.master)

        new_icon = load_icon("new")
        new_button = tk.Button(toolbar, image=new_icon, command=self.reset_board)
        new_button.image = new_icon
        new_button.pack(side=tk.LEFT, padx=2, pady=2)

        reset_icon = load_icon("reset")
        reset_button = tk.Button(toolbar, image=reset_icon, command=self.reset_board)
        reset_button.image = reset_icon
        reset_button.pack(side=tk.LEFT, padx=2, pady=2)

        solution_icon = load_icon("solution")
        solution_button = tk.Button(toolbar, image=solution_icon, command=self.show_solution)
        solution_button.image = solution_icon
        solution_button.pack(side=tk.LEFT, padx=2, pady=2)

        board_size_options = list(map(str, self.board_size_options))
        self.board_size_var, board_size_menu = create_dropdown_menu(toolbar, board_size_options, self.change_grid_size,
                                                                     str(self.board_size))
        board_size_menu.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_board(self):
        self.board_canvas = tk.Canvas(self.master, width=self.board_canvas_size[0], height=self.board_canvas_size[1])
        self.board_canvas.pack(side=tk.TOP)

        for row in range(self.board_size + 1):
            x0, y0, x1, y1 = 2, row * self.cell_size + 2, self.board_canvas_size[0] - 2, row * self.cell_size + 2
            self.board_canvas.create_line(x0, y0, x1, y1)

        for col in range(self.board_size + 1):
            x0, y0, x1, y1 = col * self.cell_size + 2, 2, col * self.cell_size + 2, self.board_canvas_size[1] - 2
            self.board_canvas.create_line(x0, y0, x1, y1)

        for row in range(self.board_size):
            for col in range(self.board_size):
                cell_value = self.board.get_value(row, col)
                if cell_value != 0:
                    x, y = self.get_cell_position(row, col)
                    self.board_canvas.create_text(x + self.cell_size // 2, y + self.cell_size // 2, text=cell_value,
                                                  font=("Arial", 16), tags="value")

        self.board_canvas.bind("<Button-1>", self.handle_mouse_click)


