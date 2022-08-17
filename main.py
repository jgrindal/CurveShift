import tkinter as tk
from tkinter import filedialog
import pandas as pd


def build_file_list():
    fl = []

    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames()
    for file in file_paths:
        fl.append(file)
    for file in fl:
        print("Extracting: " + file)
    return fl


def consolidate_files(in_files):
    li = []

    for file in in_files:
        df = pd.read_csv(file, index_col=None, header=0)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    return frame


def normalize(frame):
    return frame


def export_df(frame):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfile()
    frame.to_csv(file_path, index=False, line_terminator='\n')
    print(frame)


if __name__ == '__main__':
    file_list = build_file_list()
    df = consolidate_files(file_list)
    df = normalize(df)
    export_df(df)
