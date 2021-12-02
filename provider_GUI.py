import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk
import requests
import json


server = "http://127.0.0.1:5000"


def load_and_resize_image(filename):
    pil_image = Image.open(filename)
    original_size = pil_image.size
    adj_factor = 0.5
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def Save_button_cmd():
    return "Saved!"


def design_window():

    def cancel_cmd():
        root.destroy()

    root = tk.Tk()
    root.configure(background="#ececec")
    root.title("Monitoring Station GUI")

    ttk.Label(root, text="Select Patient Medical Record Number")\
        .grid(column=0, row=0, sticky='w', padx=20, pady=20)
    r = requests.get(server + "/api/record_numbers")
    medical_record_options = json.loads(r.text)
    variable = tk.StringVar(root)
    variable.set("1")
    record_selector = tk.OptionMenu(root, variable, *medical_record_options)
    record_selector.grid(column=1, row=0, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Patient Name") \
        .grid(column=0, row=2, sticky='w', padx=20, pady=20)

    name_data = tk.StringVar()
    name_display_box = ttk.Entry(root, textvariable=name_data)
    name_display_box.insert(0, "Yume Choi")
    name_display_box.config(state='readonly')
    name_display_box.grid(column=1, row=2, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Medical Record Number")\
        .grid(column=0, row=3, sticky='w', padx=20, pady=20)

    number_data = tk.StringVar()
    number_display_box = ttk.Entry(root, textvariable=number_data)
    number_display_box.insert(0, "1")
    number_display_box.config(state='readonly')
    number_display_box.grid(column=1, row=3, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Latest Heart Rate")\
        .grid(column=0, row=4, sticky='w', padx=20, pady=20)

    hr_data = tk.StringVar()
    hr_display_box = ttk.Entry(root, textvariable=hr_data)
    hr_display_box.insert(0, "60")
    hr_display_box.config(state='readonly')
    hr_display_box.grid(column=1, row=4, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Latest ECG Trace")\
        .grid(column=0, row=6, sticky='w', padx=20, pady=20)

    datetime_data = tk.StringVar()
    datetime_display_box = ttk.Entry(root, textvariable=datetime_data)
    datetime_display_box.insert(0, "11-14-2021")
    datetime_display_box.config(state='readonly')
    datetime_display_box.grid(column=1, row=6, sticky='w', padx=20, pady=20)

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

    tk_image = load_and_resize_image("images/acl1.jpg")
    image_label = ttk.Label(root, image=tk_image)
    image_label.grid(column=3, row=1, rowspan=4, columnspan=2)

    tk_image2 = load_and_resize_image("images/test_ECG.jpg")
    image_label2 = ttk.Label(root, image=tk_image2)
    image_label2.grid(column=0, row=7, columnspan=2)

    tk_image3 = load_and_resize_image("images/test_ECG.jpg")
    image_label3 = ttk.Label(root, image=tk_image3)
    image_label3.grid(column=3, row=7, columnspan=2)

    save_last_ecg_button = ttk.Button(root, text="Save",
                                      command=Save_button_cmd)
    save_last_ecg_button.grid(column=0, row=8, columnspan=2)

    save_selected_ecg_button = ttk.Button(root, text="Save",
                                          command=Save_button_cmd)
    save_selected_ecg_button.grid(column=3, row=8, columnspan=2)

    save_medical_image_button = ttk.Button(root, text="Save",
                                           command=Save_button_cmd)
    save_medical_image_button.grid(column=3, row=5, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    design_window()
