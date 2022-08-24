import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from pandastable import Table, TableModel, config


class curve_app:
    def __init__(self):
        self.frame = None
        self.input_file_paths = []
        self._create_base_window()
        self._create_menubar()
        self.ui_root.mainloop()

    def _create_base_window(self):
        self.ui_root = tk.Tk()
        self.ui_root.title("CurveShift")
        self.ui_root.configure(width=768, height=512)

        # file display frame
        ui_file_frame = LabelFrame(self.ui_root, text='Files', labelanchor=NW, width=400, height=700)
        ui_file_frame.pack(side=LEFT, fill=Y, expand=FALSE, anchor=NW, padx=10, pady=6)

        # file list
        self.ui_file_list = Listbox(ui_file_frame, width=70, selectmode='multiple')
        self.ui_file_list.pack(side=TOP, fill=Y, expand=TRUE, anchor=N)

        # file panel control buttons
        # create a holder frame for the bottom area
        ui_button_frame = Frame(ui_file_frame)
        ui_button_frame.pack(side=BOTTOM, expand=FALSE, anchor=S)
        # then add buttons to it.
        ui_label_add = tk.Button(ui_button_frame, text='Add', command=lambda: self.add_files())
        ui_label_add.pack(side=LEFT, expand=FALSE, padx=5, pady=6)
        ui_label_delete = tk.Button(ui_button_frame, text='Delete', command=lambda: self.remove_files())
        ui_label_delete.pack(side=LEFT, expand=FALSE, padx=5, pady=6)
        ui_label_exec = tk.Button(ui_button_frame, text='Execute', command=lambda: self.execute_on_files())
        ui_label_exec.pack(side=LEFT, expand=FALSE, padx=5, pady=6)

        # display frame
        self.ui_display_frame = Frame(self.ui_root, width=700, height=700, bg='white')
        self.ui_display_frame.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=NW)

    def _create_menubar(self):
        # create the menubar
        self.menubar = tk.Menu(self.ui_root)
        self.ui_root.configure(menu=self.menubar)

        # File menu
        fileMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Exit", command=lambda: self.ui_root.destroy)

        # View menu
        viewMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="View", menu=viewMenu)
        viewMenu.add_command(label="Add Files", command=lambda: self.add_files())

    def add_files(self):
        file_paths_to_add = filedialog.askopenfilenames(filetypes=[('CSV files', '*.csv')])
        for file in file_paths_to_add:
            if not self.input_file_paths.__contains__(file):  # check for duplicates
                self.input_file_paths.append(file)
                self.ui_file_list.insert(END, file)  # update UI

    def remove_files(self):
        selection_indices = self.ui_file_list.curselection()
        print(selection_indices)
        for index in selection_indices[::-1]:
            self.input_file_paths.remove(self.input_file_paths[index])
            self.ui_file_list.delete(index)

    def execute_on_files(self):
        self.concatenate_files_to_frame()
        self.create_pivot_table()

    def concatenate_files_to_frame(self):
        # Start by creating a blank list.  This will be the vessel for all our dataframes in a minute
        li = []

        # Open each file in the list of files
        for file in self.input_file_paths:
            #TODO: Add data validation
            current_df = pd.read_csv(file, index_col=None, header=0)  # Read the CSV into a pandas dataframe
            li.append(current_df)  # Put the dataframe into a list.  Each file is going to be a separate one
        self.frame = pd.concat(li, axis=0, ignore_index=True)  # concatenate all the dataframes into a single dataframe

    def create_pivot_table(self):
        table = pd.pivot_table(self.frame, values='Impact Delta', index=['Risk Type','Index'],
                               columns='Contract Month', aggfunc=np.sum, fill_value=0)
        display_table = Table(self.ui_display_frame, dataframe=table, showtoolbar=True, showstatusbar=True)
        display_table.show()
        print(table)
