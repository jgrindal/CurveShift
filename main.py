import tkinter as tk
from tkinter import *
from tkinter import filedialog

import pandas as pd

import curve_shift.curve_app


def build_file_list():
    # Don't worry much about this - this is GUI stuff to select the files.  All that matters is we make a list of
    # file locations called file_paths
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(filetypes=[('CSV files','*.csv')])

    # We're going to print to console a list of all the files we're extracting from.
    for file in file_paths:
        print("Extracting: " + file)
    return file_paths


def consolidate_files(in_files):
    # Start by creating a blank list.  This will be the vessel for all our dataframes in a minute
    li = []

    # Open each file in the list of files
    for file in in_files:
        df = pd.read_csv(file, index_col=None, header=0) # Read the CSV into a pandas dataframe
        li.append(df) # Put the dataframe into a list.  Each file is going to be a separate one
    frame = pd.concat(li, axis=0, ignore_index=True) # concatenate all the dataframes into a single dataframe
    return frame


def normalize(frame):
    return frame


def export_df(frame):
    # Don't worry much about this - this is GUI stuff to select the export destination.
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfile(filetypes=[('CSV files','*.csv')])

    # We're going to export to the selected path now.
    frame.to_csv(file_path, index=False, line_terminator='\n')
    print(frame)


if __name__ == '__main__':
    # This is our main function that will be executed
    # It's a simple process, we're going to build a file list, consolidate the files in a dataframe and export it

    window = curve_shift.curve_app()
'''
    file_list = build_file_list()
    df = consolidate_files(file_list)
    df = normalize(df)
    export_df(df)
'''