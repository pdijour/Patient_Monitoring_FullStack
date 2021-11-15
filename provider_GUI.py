import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk


def design_window():

    def cancel_cmd():
        root.destroy()

    root = tk.Tk()
    root.title("Monitoring Station GUI")

    # ttk.Label(root, text="Name").grid(column=0, row=1, sticky='e')
    # name_data = tk.StringVar()
    # name_entry_box = ttk.Entry(root, width=50, textvariable=name_data)
    # name_entry_box.grid(column=1, row=1, sticky='w', padx=20, pady=20)
    #
    # ttk.Label(root, text="ID").grid(column=0, row=2)
    # id_data = tk.StringVar()
    # id_entry_box = ttk.Entry(root, width=10, textvariable=id_data)
    # id_entry_box.grid(column=1, row=2, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Select Patient Medical Record Number")\
        .grid(column=0, row=0, sticky='w', padx=20, pady=20)
    medical_record_options = ["1", "2", "3", "4", "5", "6"]
    variable = tk.StringVar(root)
    variable.set("1")
    record_selector = tk.OptionMenu(root, variable, *medical_record_options)
    record_selector.grid(column=1, row=0, sticky='w', padx=20, pady=20)

    root.mainloop()


if __name__ == '__main__':
    design_window()

