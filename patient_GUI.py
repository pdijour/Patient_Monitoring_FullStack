# patient_GUI.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk

def load_and_resize_image(filename):
    pil_image = Image.open(filename)
    original_size = pil_image.size
    adj_factor = 0.5
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def change_pic():
    filename = filedialog.askopenfilename(initialdir="images")
    if filename == "":
        messagebox.showinfo("Cancel", "You cancelled the image load")
        return
    tk_image = load_and_resize_image(filename)
    return tk_image


def design_window():

    def change_ecg_picture_cmd():
        tk_image = change_pic()
        ecg_image_label.configure(image=tk_image)
        ecg_image_label.image = tk_image

    def change_medical_picture_cmd():
        tk_image = change_pic()
        medical_image_label.configure(image=tk_image)
        medical_image_label.image = tk_image


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

    ttk.Label(root, text="Medical Image")\
        .grid(column=0, row=2, sticky='w', padx=20, pady=20)

    tk_medical_image = load_and_resize_image("images/acl1.jpg")
    medical_image_label = ttk.Label(root, image=tk_medical_image)
    medical_image_label.grid(column=0, row=3, columnspan=2, padx=20, pady=20)

    tk_ecg_image = load_and_resize_image("images/test_ECG.jpg")
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.grid(column=3, row=3, columnspan=2, padx=20, pady=20)

    change_picture_btn = ttk.Button(root, text="Change Picture",
                                    command=change_ecg_picture_cmd)
    change_picture_btn.grid(column=4, row=2, sticky='w', padx=20, pady=20)

    root.mainloop()


if __name__ == '__main__':
    design_window()
