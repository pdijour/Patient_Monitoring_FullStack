# patient_GUI.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Scrollbar
from PIL import Image, ImageTk
from ecg_analysis import overall_plotting, overall_rate
from datetime import datetime
import os
import requests
import base64


server = "http://127.0.0.1:5000"


def load_and_resize_image(filename):
    pil_image = Image.open(filename)
    original_size = pil_image.size
    adj_factor = 0.5
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image, filename


def change_file(starting, type):
    filename = filedialog.askopenfilename(initialdir="{}".format(starting),
                                          filetypes=type)
    return filename


def add_files_to_server(patient_name, id_no, medical_files,
                        medical_files_b64, ecg_files, ecg_files_b64,
                        bpms, timestamps):
    """ Makes request to server to add specified patient information
    """
    id_no = id_no
    patient1 = {"patient_name": patient_name,
                "record_number": id_no,
                "medical_image_files": medical_files,
                "medical_images_b64": medical_files_b64,
                "ECG_image_files": ecg_files,
                "ECG_images_b64": ecg_files_b64,
                "heartrates": bpms,
                "datetimes": timestamps}
    r = requests.post(server + "/api/add_files", json=patient1)
    print(r.status_code)
    print(r.text)
    return r.text


def convert_image_file_to_b64_string(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def design_window():

    def upload_button_cmd():
        name = name_data.get()
        record_number = record_data.get()
        medical_filename = os.path.basename(medical_file_label.name)
        medical_b64 = convert_image_file_to_b64_string(medical_file_label.name)
        ecg_filename = os.path.basename(ecg_file_label.name)
        ecg_b64 = convert_image_file_to_b64_string(ecg_file_label.name)
        heart_rate = bpm_label.hr
        time = datetime.now()
        timestamp = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        answer = add_files_to_server(name,
                                     record_number,
                                     medical_filename,
                                     medical_b64,
                                     ecg_filename,
                                     ecg_b64,
                                     heart_rate,
                                     timestamp)
        output_string.configure(text=answer)

    def cancel_cmd():
        root.destroy()

    def change_ecg_picture_cmd():
        filename = change_file("test_data", [("CSV Files", ".csv")])
        filename_png = "{}.png".format(filename.strip(".csv"))
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the file selection")
            return
        overall_plotting(filename)
        hr = overall_rate(filename)
        tk_image, filename = load_and_resize_image(filename_png)
        ecg_image_label.configure(image=tk_image)
        ecg_image_label.image = tk_image
        ecg_file_label.configure(text=filename_png)
        ecg_file_label.name = filename
        bpm_label.configure(text=hr)
        bpm_label.hr = hr

    def change_medical_picture_cmd():
        filename = change_file("images",
                               [("Picture files", ".png .jpg .jpeg")])
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the image load")
            return
        tk_image, filename = load_and_resize_image(filename)
        medical_image_label.configure(image=tk_image)
        medical_image_label.image = tk_image
        medical_file_label.configure(text=filename)
        medical_file_label.name = filename

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

    tk_medical_image = ""
    medical_filename = ""
    medical_image_label = ttk.Label(root, image=tk_medical_image)
    medical_image_label.grid(column=0, row=4, columnspan=2, padx=20, pady=20)

    medical_file_label = ttk.Label(root, text=medical_filename, wraplength=200)
    medical_file_label.grid(column=1, row=3, sticky='w', padx=20)

    change_picture_btn = ttk.Button(root, text="Change Picture",
                                    command=change_medical_picture_cmd)
    change_picture_btn.grid(column=1, row=2, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="ECG Image")\
        .grid(column=3, row=2, sticky='w', padx=20, pady=20)

    tk_ecg_image = ""
    ecg_filename = ""
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.grid(column=3, row=4, columnspan=2, padx=20, pady=20)

    ecg_file_label = ttk.Label(root, text=ecg_filename, wraplength=200)
    ecg_file_label.grid(column=4, row=3, sticky='w', padx=20)

    change_picture_btn = ttk.Button(root, text="Choose ECG Data to Display",
                                    command=change_ecg_picture_cmd)
    change_picture_btn.grid(column=4, row=2, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Heart Rate:")\
        .grid(column=3, row=5, sticky='w', padx=20, pady=20)

    hr = ""

    bpm_label = ttk.Label(root, text=hr)
    bpm_label.grid(column=4, row=5, sticky='w', padx=20, pady=20)

    upload_button = ttk.Button(root, text="Upload",
                               command=upload_button_cmd)
    upload_button.grid(column=3, row=6, columnspan=2)

    output_string = ttk.Label(root)
    output_string.grid(column=3, row=7)

    cancel_button = ttk.Button(root, text="Cancel",
                               command=cancel_cmd)
    cancel_button.grid(column=5, row=6)

    root.mainloop()


if __name__ == '__main__':
    design_window()
