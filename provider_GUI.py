import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk


def design_window():

    def cancel_cmd():
        root.destroy()

    root = tk.Tk()
    root.title("Monitoring Station GUI")

    ttk.Label(root, text="Select Patient Medical Record Number")\
        .grid(column=0, row=0, sticky='w', padx=20, pady=20)
    medical_record_options = ["1", "2", "3", "4", "5", "6"]
    variable = tk.StringVar(root)
    variable.set("1")
    record_selector = tk.OptionMenu(root, variable, *medical_record_options)
    record_selector.grid(column=1, row=0, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Patient Name") \
        .grid(column=0, row=3, sticky='w', padx=20, pady=20)

    name_data = tk.StringVar()
    name_display_box = ttk.Entry(root, textvariable=name_data)
    name_display_box.insert(0, "Yume Choi")
    name_display_box.config(state='readonly')
    name_display_box.grid(column=1, row=3, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Medical Record Number")\
        .grid(column=0, row=4, sticky='w', padx=20, pady=20)

    number_data = tk.StringVar()
    number_display_box = ttk.Entry(root, textvariable=number_data)
    number_display_box.insert(0, "1")
    number_display_box.config(state='readonly')
    number_display_box.grid(column=1, row=4, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Latest Heart Rate")\
        .grid(column=0, row=5, sticky='w', padx=20, pady=20)

    HR_data = tk.StringVar()
    HR_display_box = ttk.Entry(root, textvariable=HR_data)
    HR_display_box.insert(0, "60")
    HR_display_box.config(state='readonly')
    HR_display_box.grid(column=1, row=5, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Latest ECG Trace")\
        .grid(column=0, row=6, sticky='w', padx=20, pady=20)

    Datetime_data = tk.StringVar()
    Datetime_display_box = ttk.Entry(root, textvariable=Datetime_data)
    Datetime_display_box.insert(0, "11-14-2021")
    Datetime_display_box.config(state='readonly')
    Datetime_display_box.grid(column=1, row=6, sticky='w', padx=20, pady=20)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=6, row=12)

    ttk.Label(root, text="Display Medical Image")\
        .grid(column=3, row=0, sticky='w', padx=20, pady=20)
    medical_image_options = ["X-ray", "MRI", "CT", "PET"]
    variable2 = tk.StringVar(root)
    variable2.set("X-ray")
    record_selector = tk.OptionMenu(root, variable2, *medical_image_options)
    record_selector.grid(column=4, row=0, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Display Historical ECG") \
        .grid(column=3, row=6, sticky='w', padx=20, pady=20)
    medical_image_options = ["tachycardic 11-01-2021",
                             "normal 11-05-2021",
                             "normal 11-10-2021"]
    variable3 = tk.StringVar(root)
    variable3.set("tachycardic 11-01-2021")
    record_selector = tk.OptionMenu(root, variable3, *medical_image_options)
    record_selector.grid(column=4, row=6, sticky='w', padx=20, pady=20)

    root.mainloop()


if __name__ == '__main__':
    design_window()

