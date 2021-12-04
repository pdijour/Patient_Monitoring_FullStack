import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk
import requests
import json
from cloud_server import b64_to_ndarray, read_file_as_b64


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


def display_ndarray(nd):
    img = ImageTk.PhotoImage(image=Image.fromarray(nd))
    return img


def design_window():

    def cancel_cmd():
        root.destroy()

    def save_button_cmd():
        return "Saved!"

    def update_info(event):
        patient_id = int(variable.get())
        r = requests.post(server + "/api/get_info", json=patient_id)
        patient_info = json.loads(r.text)

        namelabel.set(patient_info["name"])
        idlabel.set(patient_info["medical_record_number"])
        hrlabel.set(patient_info["heart_rates"][-1])
        dtlabel.set(patient_info["datetimes"][-1])

        variable2.set(patient_info["medical_images"][0])
        variable3.set(patient_info["ecg_images"][0])
        image_selector['values'] = patient_info["medical_images"]
        ecg_selector['values'] = patient_info["ecg_images"]

        new_ecg_nd = b64_to_ndarray(patient_info["ecg_images_b64"][-1])

    root = tk.Tk()
    root.configure(background="#ececec")
    root.title("Monitoring Station GUI")

    ttk.Label(root, text="Select Patient Medical Record Number")\
        .grid(column=0, row=0, sticky='w', padx=20, pady=20)

    r = requests.get(server + "/api/record_numbers")
    medical_record_options = json.loads(r.text)

    variable = tk.StringVar(root)
    variable.set(json.loads(r.text)[1])
    record_selector = ttk.Combobox(root, textvariable=variable)
    record_selector['values'] = medical_record_options
    record_selector['state'] = 'readonly'
    record_selector.grid(column=1, row=0, sticky='w', padx=20, pady=20)

    record_selector.bind('<<ComboboxSelected>>', update_info)

    # Read Selected option and use post request to get all the info
    patient_id = int(variable.get())
    r = requests.post(server + "/api/get_info", json=patient_id)
    patient_info = json.loads(r.text)

    ttk.Label(root, text="Patient Name") \
        .grid(column=0, row=2, sticky='w', padx=20, pady=20)

    namelabel = tk.StringVar()
    namelabel.set(patient_info["name"])
    ttk.Label(textvariable=namelabel)\
        .grid(column=1, row=2, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Medical Record Number")\
        .grid(column=0, row=3, sticky='w', padx=20, pady=20)

    idlabel = tk.StringVar()
    idlabel.set(patient_info["medical_record_number"])
    ttk.Label(textvariable=idlabel)\
        .grid(column=1, row=3, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Latest Heart Rate")\
        .grid(column=0, row=4, sticky='w', padx=20, pady=20)

    hrlabel = tk.StringVar()
    hrlabel.set(patient_info["heart_rates"][-1])
    ttk.Label(textvariable=hrlabel)\
        .grid(column=1, row=4, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Latest ECG Trace")\
        .grid(column=0, row=6, sticky='w', padx=20, pady=20)

    dtlabel = tk.StringVar()
    dtlabel.set(patient_info["datetimes"][-1])
    ttk.Label(textvariable=dtlabel)\
        .grid(column=1, row=6, sticky='w', padx=20, pady=20)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=6, row=12)

    ttk.Label(root, text="Display Medical Image")\
        .grid(column=3, row=0, sticky='w', padx=20, pady=20)
    medical_image_options = patient_info["medical_images"]
    variable2 = tk.StringVar(root)
    variable2.set(medical_image_options[0])
    image_selector = ttk.Combobox(root, textvariable=variable2)
    image_selector['values'] = medical_image_options
    image_selector['state'] = 'readonly'
    image_selector.grid(column=4, row=0, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Display Historical ECG") \
        .grid(column=3, row=6, sticky='w', padx=20, pady=20)
    ecg_image_options = patient_info["ecg_images"]
    variable3 = tk.StringVar(root)
    variable3.set(ecg_image_options[0])
    ecg_selector = ttk.Combobox(root, textvariable=variable3)
    ecg_selector['values'] = ecg_image_options
    ecg_selector['state'] = 'readonly'
    ecg_selector.grid(column=4, row=6, sticky='w', padx=20, pady=20)

    tk_image = load_and_resize_image("images/acl1.jpg")
    image_label = ttk.Label(root, image=tk_image)
    image_label.grid(column=3, row=1, rowspan=4, columnspan=2)

    latest_ecg_nd = b64_to_ndarray(patient_info["ecg_images_b64"][-1])
    tk_image2 = display_ndarray(latest_ecg_nd)
    image_label2 = ttk.Label(root, image=tk_image2)
    image_label2.grid(column=0, row=7, columnspan=2)

    tk_image3 = load_and_resize_image("images/test_ECG.jpg")
    image_label3 = ttk.Label(root, image=tk_image3)
    image_label3.grid(column=3, row=7, columnspan=2)

    save_last_ecg_button = ttk.Button(root, text="Save",
                                      command=save_button_cmd)
    save_last_ecg_button.grid(column=0, row=8, columnspan=2)

    save_selected_ecg_button = ttk.Button(root, text="Save",
                                          command=save_button_cmd)
    save_selected_ecg_button.grid(column=3, row=8, columnspan=2)

    save_medical_image_button = ttk.Button(root, text="Save",
                                           command=save_button_cmd)
    save_medical_image_button.grid(column=3, row=5, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    design_window()
