import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk
import requests
import json
from cloud_server import b64_to_ndarray, get_index, \
    resize_image, b64_string_to_file

server = "http://127.0.0.1:5000"


def display_ndarray(nd):
    img = ImageTk.PhotoImage(image=Image.fromarray(nd))
    return img


def design_window():

    def cancel_cmd():
        root.destroy()

    def refresh():
        patient_info = update_patient_info()

        namelabel.set(patient_info["name"])
        idlabel.set(patient_info["medical_record_number"])
        hrlabel.set(patient_info["heart_rates"][-1])
        dtlabel.set(patient_info["datetimes"][-1])

        variable2.set(patient_info["medical_images"][0])
        variable3.set(patient_info["datetimes"][0])
        image_selector['values'] = patient_info["medical_images"]
        ecg_selector['values'] = patient_info["datetimes"]

        new_medical_b64 = patient_info["medical_images_b64"][0]
        new_medical_nd = b64_to_ndarray(new_medical_b64)
        resized_medical_nd = resize_image(new_medical_nd)
        tk_medical_image = display_ndarray(resized_medical_nd)
        medical_image_label.configure(image=tk_medical_image)
        medical_image_label.image = tk_medical_image

        new_ecg_b64 = patient_info["ecg_images_b64"][0]
        new_ecg_nd = b64_to_ndarray(new_ecg_b64)
        resized_ecg_nd = resize_image(new_ecg_nd)
        tk_ecg_image = display_ndarray(resized_ecg_nd)
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image

        latest_ecg_nd = b64_to_ndarray(patient_info["ecg_images_b64"][-1])
        resized_ecg_nd = resize_image(latest_ecg_nd)
        tk_latest_ecg = display_ndarray(resized_ecg_nd)
        latest_ecg_image_label.configure(image=tk_latest_ecg)
        latest_ecg_image_label.image = tk_latest_ecg
        root.after(10000, refresh)

    def update_patient_info():
        patient_id = int(variable.get())
        r = requests.post(server + "/api/get_info", json=patient_id)
        patient_info = json.loads(r.text)
        return patient_info

    def update_info(event):
        patient_info = update_patient_info()

        patient_info = update_patient_info()
        namelabel.set(patient_info["name"])
        idlabel.set(patient_info["medical_record_number"])
        hrlabel.set(patient_info["heart_rates"][-1])
        dtlabel.set(patient_info["datetimes"][-1])

        variable2.set(patient_info["medical_images"][0])
        variable3.set(patient_info["datetimes"][0])
        image_selector['values'] = patient_info["medical_images"]
        ecg_selector['values'] = patient_info["datetimes"]

        new_medical_b64 = patient_info["medical_images_b64"][0]
        new_medical_nd = b64_to_ndarray(new_medical_b64)
        resized_medical_nd = resize_image(new_medical_nd)
        tk_medical_image = display_ndarray(resized_medical_nd)
        medical_image_label.configure(image=tk_medical_image)
        medical_image_label.image = tk_medical_image

        new_ecg_b64 = patient_info["ecg_images_b64"][0]
        new_ecg_nd = b64_to_ndarray(new_ecg_b64)
        resized_ecg_nd = resize_image(new_ecg_nd)
        tk_ecg_image = display_ndarray(resized_ecg_nd)
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image

        latest_ecg_nd = b64_to_ndarray(patient_info["ecg_images_b64"][-1])
        resized_ecg_nd = resize_image(latest_ecg_nd)
        tk_latest_ecg = display_ndarray(resized_ecg_nd)
        latest_ecg_image_label.configure(image=tk_latest_ecg)
        latest_ecg_image_label.image = tk_latest_ecg

    def update_medical_image(event):
        patient_info = update_patient_info()

        selected_image = variable2.get()
        index = get_index(patient_info["medical_images"], selected_image)
        new_medical_b64 = patient_info["medical_images_b64"][index]
        new_medical_nd = b64_to_ndarray(new_medical_b64)
        resized_medical_nd = resize_image(new_medical_nd)
        tk_medical_image = display_ndarray(resized_medical_nd)
        medical_image_label.configure(image=tk_medical_image)
        medical_image_label.image = tk_medical_image

    def update_ecg_image(event):
        patient_info = update_patient_info()

        selected_image = variable3.get()
        index = get_index(patient_info["datetimes"], selected_image)
        new_ecg_b64 = patient_info["ecg_images_b64"][index]
        new_ecg_nd = b64_to_ndarray(new_ecg_b64)
        resized_ecg_nd = resize_image(new_ecg_nd)
        tk_ecg_image = display_ndarray(resized_ecg_nd)
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image

    def save_latest_ecg():
        patient_info = update_patient_info()
        filename = filedialog.asksaveasfile(defaultextension=".jpg",
                                            initialfile="Latest_ECG.jpg",
                                            mode='wb')
        if not filename:
            return
        latest_ecg_b64 = patient_info["ecg_images_b64"][-1]
        b64_string_to_file(latest_ecg_b64, filename)

    def save_ecg():
        patient_info = update_patient_info()
        filename = filedialog.asksaveasfile(defaultextension=".jpg",
                                            initialfile="ECG.jpg",
                                            mode='wb')
        if not filename:
            return
        selected_image = variable3.get()
        index = get_index(patient_info["datetimes"], selected_image)
        ecg_b64 = patient_info["ecg_images_b64"][index]
        b64_string_to_file(ecg_b64, filename)

    def save_medical_image():
        patient_info = update_patient_info()
        filename = filedialog.asksaveasfile(defaultextension=".jpg",
                                            initialfile="Medical_Image.jpg",
                                            mode='wb')
        if not filename:
            return
        selected_image = variable2.get()
        index = get_index(patient_info["medical_images"], selected_image)
        medical_b64 = patient_info["medical_images_b64"][index]
        b64_string_to_file(medical_b64, filename)

    root = tk.Tk()
    root.configure(background="#ececec")
    root.title("Monitoring Station GUI")

    ttk.Label(root, text="Select Patient Medical Record Number")\
        .grid(column=0, row=0, sticky='w', padx=20, pady=20)

    r = requests.get(server + "/api/record_numbers")
    medical_record_options = json.loads(r.text)

    variable = tk.StringVar(root)
    variable.set(medical_record_options[0])
    record_selector = ttk.Combobox(root, textvariable=variable)
    record_selector['values'] = medical_record_options
    record_selector['state'] = 'readonly'
    record_selector.grid(column=1, row=0, sticky='w', padx=20, pady=20)

    record_selector.bind('<<ComboboxSelected>>', update_info)

    patient_info = update_patient_info()

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
    image_selector.bind('<<ComboboxSelected>>', update_medical_image)

    ttk.Label(root, text="Display Historical ECG") \
        .grid(column=3, row=6, sticky='w', padx=20, pady=20)
    ecg_image_options = patient_info["datetimes"]
    variable3 = tk.StringVar(root)
    variable3.set(ecg_image_options[0])
    ecg_selector = ttk.Combobox(root, textvariable=variable3)
    ecg_selector['values'] = ecg_image_options
    ecg_selector['state'] = 'readonly'
    ecg_selector.grid(column=4, row=6, sticky='w', padx=20, pady=20)
    ecg_selector.bind('<<ComboboxSelected>>', update_ecg_image)

    medical_nd = b64_to_ndarray(patient_info["medical_images_b64"][0])
    resized_medical_nd = resize_image(medical_nd)
    tk_medical_image = display_ndarray(resized_medical_nd)
    medical_image_label = ttk.Label(root, image=tk_medical_image)
    medical_image_label.configure(image=tk_medical_image)
    medical_image_label.grid(column=3, row=1, rowspan=4, columnspan=2)

    latest_ecg_nd = b64_to_ndarray(patient_info["ecg_images_b64"][-1])
    resized_ecg_nd = resize_image(latest_ecg_nd)
    tk_latest_ecg = display_ndarray(resized_ecg_nd)
    latest_ecg_image_label = ttk.Label(root, image=tk_latest_ecg)
    latest_ecg_image_label.configure(image=tk_latest_ecg)
    latest_ecg_image_label.grid(column=0, row=7, columnspan=2)

    ecg_nd = b64_to_ndarray(patient_info["ecg_images_b64"][0])
    resized_ecg_nd = resize_image(ecg_nd)
    tk_ecg_image = display_ndarray(resized_ecg_nd)
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.configure(image=tk_ecg_image)
    ecg_image_label.grid(column=3, row=7, columnspan=2)

    save_last_ecg_button = ttk.Button(root, text="Save",
                                      command=save_latest_ecg)
    save_last_ecg_button.grid(column=0, row=8, columnspan=2)

    save_selected_ecg_button = ttk.Button(root, text="Save",
                                          command=save_ecg)
    save_selected_ecg_button.grid(column=3, row=8, columnspan=2)

    save_medical_image_button = ttk.Button(root, text="Save",
                                           command=save_medical_image)
    save_medical_image_button.grid(column=3, row=5, columnspan=2)

    refresh()

    root.mainloop()


if __name__ == '__main__':
    design_window()
