# patient_GUI.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk


def design_window():

    root = tk.Tk()
    root.configure(background="#ececec")
    root.title("Patient GUI")

    ttk.Label(root, text="Patient Name") \
        .grid(column=0, row=0, sticky='w', padx=20, pady=20)

    name_data = tk.StringVar()
    name_entry_box = ttk.Entry(root, textvariable=name_data)
    name_entry_box.grid(column=1, row=0, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Patient Medical Record Number")\
        .grid(column=0, row=1, sticky='w', padx=20, pady=20)

    record_data = tk.StringVar()
    record_entry_box = ttk.Entry(root, textvariable=record_data)
    record_entry_box.grid(column=1, row=1, sticky='w', padx=20, pady=20)

    root.mainloop()


if __name__ == '__main__':
    design_window()
