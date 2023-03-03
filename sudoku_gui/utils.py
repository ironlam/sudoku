import tkinter as tk
from PIL import Image, ImageTk
import os
import json


def load_config():
    with open('config.json') as f:
        return json.load(f)


def get_board_cell_size(board_size):
    return 50 if board_size < 10 else 35


def get_board_canvas_size(board_size):
    cell_size = get_board_cell_size(board_size)
    return board_size * cell_size + 4, board_size * cell_size + 4


def load_icon(icon_name):
    config = load_config()
    script_dir = os.path.dirname(__file__)
    icon_path = os.path.join(script_dir, 'images', config['images'][icon_name])
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    return icon_photo


def get_canvas_coords(row, col, board_size, cell_size):
    x0 = col * cell_size + 2
    y0 = row * cell_size + 2
    x1 = x0 + cell_size
    y1 = y0 + cell_size
    return x0, y0, x1, y1


def get_cell_coords(x, y, board_size, cell_size):
    row = (y - 2) // cell_size
    col = (x - 2) // cell_size
    if row >= board_size or col >= board_size:
        return None
    return row, col


def create_dropdown_menu(master, options, command, current_option=None):
    var = tk.StringVar(value=current_option)
    menu = tk.OptionMenu(master, var, *options, command=command)
    menu.config(width=4)
    return var, menu
