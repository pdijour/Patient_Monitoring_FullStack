# patient_GUI.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk


def design_window():

    root = tk.Tk()
    root.configure(background="#ececec")
    root.title("Patient GUI")

    root.mainloop()


if __name__ == '__main__':
    design_window()
