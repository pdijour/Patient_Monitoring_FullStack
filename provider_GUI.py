import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from PIL import Image, ImageTk
import requests
import json
from cloud_client import b64_to_ndarray, get_index, \
    resize_image, b64_string_to_file, process_b64

server = "http://127.0.0.1:5000"


def design_window():
    """Creates the provider-side GUI window

        A GUI window is created that is the providers' way of accessing
        the database storing all the information uploaded through the
        patient-side GUI. It allows providrs to see all patient medical
        record numbers corresponding to entries in the database through
        a drop down menu. Upon selection of one, the relevant information
        for that patient will be displayed in the GUI, including the
        patient's name, medical record number, latest heart rate, the
        date and time of the last ecg uploaded, and the trace of the most
        recent ECG. Also, the drop down menus for medical image and
        historical ECG selection all update as well to reflect those of
        the current selected patient. Whenever a selection is made on
        one of those drop down menus, the corresponding image is displayed.
        Each image has a save button underneath to allow users to save the
        image locally to their device with a desired file name. The
        GUI refreshes the information available every 10 seconds by
        making requests to the server to access the database, in case
        any information changes or new information is uploaded. When this
        occurs, all the relevant information is updated in the GUI.
    """
    def cancel_cmd():
        """
        Closes the GUI
        """
        root.destroy()

    def refresh():
        """
        Function called every 10 seconds to refresh
        the GUI with updated information from the Mongo
        database. Refreshes all comboboxes, info,
        and latest ECG datetime, trace, and heart rate as well.
        """
        r = requests.get(server + "/api/record_numbers")
        medical_record_options = json.loads(r.text)
        record_selector['values'] = medical_record_options
        patient_info = update_patient_info()

        namelabel.set(patient_info["name"])
        idlabel.set(patient_info["medical_record_number"])
        hrlabel.set(patient_info["heart_rates"][-1])
        dtlabel.set(patient_info["datetimes"][-1])

        image_selector['values'] = patient_info["medical_images"]
        ecg_selector['values'] = patient_info["datetimes"]

        resized_ecg_nd = process_b64(patient_info["ecg_images_b64"][-1])
        tk_latest_ecg = ImageTk. \
            PhotoImage(image=Image.fromarray(resized_ecg_nd))
        latest_ecg_image_label.configure(image=tk_latest_ecg)
        latest_ecg_image_label.image = tk_latest_ecg
        root.after(10000, refresh)

    def update_patient_info():
        """
        This function is called specifically to perform a post request
        the server to retrieve all the relevant information about a patient,
        specified by selection in the first combobox,from the database.

        Returns
        -------
        Dict
            Containing all relevant updated information about selected patient
        """
        patient_id = int(variable.get())
        r = requests.post(server + "/api/get_info", json=patient_id)
        patient_info = json.loads(r.text)
        return patient_info

    def update_info(event):
        """
        This function does essentially the same thing as the update
        function but has the event parameter because it is bound to
        the combobox for the medical record number selection.
        Additionally, it changes the displayed medical image, and
        ecg image to match the selected patient. This way, whenever
        a different selection is made, the relevant information about
        that patient is updated on the GUI.

        Parameters
        ----------
        event
            Needed to trigger when bound combobox selection changes
        """
        patient_info = update_patient_info()

        namelabel.set(patient_info["name"])
        idlabel.set(patient_info["medical_record_number"])
        hrlabel.set(patient_info["heart_rates"][-1])
        dtlabel.set(patient_info["datetimes"][-1])

        variable2.set(patient_info["medical_images"][0])
        variable3.set(patient_info["datetimes"][0])
        image_selector['values'] = patient_info["medical_images"]
        ecg_selector['values'] = patient_info["datetimes"]

        resized_medical_nd = process_b64(patient_info["medical_images_b64"][0])
        tk_medical_image = ImageTk. \
            PhotoImage(image=Image.fromarray(resized_medical_nd))
        medical_image_label.configure(image=tk_medical_image)
        medical_image_label.image = tk_medical_image

        resized_ecg_nd = process_b64(patient_info["ecg_images_b64"][0])
        tk_ecg_image = ImageTk. \
            PhotoImage(image=Image.fromarray(resized_ecg_nd))
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image

        resized_ecg_nd = process_b64(patient_info["ecg_images_b64"][-1])
        tk_latest_ecg = ImageTk. \
            PhotoImage(image=Image.fromarray(resized_ecg_nd))
        latest_ecg_image_label.configure(image=tk_latest_ecg)
        latest_ecg_image_label.image = tk_latest_ecg

    def update_medical_image(event):
        """
        This function updates the medical image displayed whenever
        a different selection is made in the medical image combobox.
        It reads the selected file, gets the index of that file
        in the medical image list for that patient, then uses that
        index to retrieve the corresponding b64 string representing
        that image selected from the parallel b64 list. Then, this
        b64 string is converted to an ndarray, resized, and then
        displayed.

        Parameters
        ----------
        event
            Needed to trigger when bound combobox selection changes
        """
        patient_info = update_patient_info()

        selected_image = variable2.get()
        index = get_index(patient_info["medical_images"], selected_image)
        resized_medical_nd = process_b64(patient_info["medical_images_b64"]
                                         [index])
        tk_medical_image = ImageTk.\
            PhotoImage(image=Image.fromarray(resized_medical_nd))
        medical_image_label.configure(image=tk_medical_image)
        medical_image_label.image = tk_medical_image

    def update_ecg_image(event):
        """
        This function updates the ecg image displayed whenever
        a different selection is made in the ecg image combobox.
        It reads the selected file, gets the index of that file
        in the ecg image list for that patient, then uses that
        index to retrieve the corresponding b64 string representing
        that image selected from the parallel b64 list. Then, this
        b64 string is converted to an ndarray, resized, and then
        displayed.

        Parameters
        ----------
        event
            Needed to trigger when bound combobox selection changes
        """
        patient_info = update_patient_info()

        selected_image = variable3.get()
        index = get_index(patient_info["datetimes"], selected_image)
        resized_ecg_nd = process_b64(patient_info["ecg_images_b64"][index])
        tk_ecg_image = ImageTk.\
            PhotoImage(image=Image.fromarray(resized_ecg_nd))
        ecg_image_label.configure(image=tk_ecg_image)
        ecg_image_label.image = tk_ecg_image

    def save_latest_ecg():
        """
        This function allows users to save the latest_ecg image
        displayed in the GUI locally to their computer with a
        location and name of their choice. First, the filedialogue
        module asksaveasfile is used to allow users to specify a
        name and location for the image. Then, if they provide
        these, the b64 string is retrieved and written into a file.
        """
        patient_info = update_patient_info()
        filename = filedialog.asksaveasfile(defaultextension=".jpg",
                                            initialfile="Latest_ECG.jpg",
                                            mode='wb')
        if not filename:
            return
        latest_ecg_b64 = patient_info["ecg_images_b64"][-1]
        b64_string_to_file(latest_ecg_b64, filename)

    def save_ecg():
        """
        This function allows users to save the selected ecg image
        displayed in the GUI locally to their computer with a
        location and name of their choice. First, the filedialogue
        module asksaveasfile is used to allow users to specify a
        name and location for the image. Then, if they provide
        these, the b64 string is retrieved and written into a file.
        """
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
        """
        This function allows users to save the selected medcial image
        displayed in the GUI locally to their computer with a
        location and name of their choice. First, the filedialogue
        module asksaveasfile is used to allow users to specify a
        name and location for the image. Then, if they provide
        these, the b64 string is retrieved and written into a file.
        """
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

    # Select from available medical record numbers in database
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

    # Update displayed information if selection changes
    record_selector.bind('<<ComboboxSelected>>', update_info)

    # Updates patient_info dictionary to contain all relevant info
    patient_info = update_patient_info()

    # Display the name of the patient selected
    ttk.Label(root, text="Patient Name") \
        .grid(column=0, row=2, sticky='w', padx=20, pady=20)
    namelabel = tk.StringVar()
    namelabel.set(patient_info["name"])
    ttk.Label(textvariable=namelabel)\
        .grid(column=1, row=2, sticky='w', padx=20, pady=20)

    # Display the medical record number of the patient
    ttk.Label(root, text="Medical Record Number")\
        .grid(column=0, row=3, sticky='w', padx=20, pady=20)
    idlabel = tk.StringVar()
    idlabel.set(patient_info["medical_record_number"])
    ttk.Label(textvariable=idlabel)\
        .grid(column=1, row=3, sticky='w', padx=20, pady=20)

    # Display the latest heart rate for the patient
    ttk.Label(root, text="Latest Heart Rate")\
        .grid(column=0, row=4, sticky='w', padx=20, pady=20)
    hrlabel = tk.StringVar()
    hrlabel.set(patient_info["heart_rates"][-1])
    ttk.Label(textvariable=hrlabel)\
        .grid(column=1, row=4, sticky='w', padx=20, pady=20)

    # Display the datetime for the latest ECG trace for the patient
    ttk.Label(root, text="Latest ECG Trace")\
        .grid(column=0, row=6, sticky='w', padx=20, pady=20)
    dtlabel = tk.StringVar()
    dtlabel.set(patient_info["datetimes"][-1])
    ttk.Label(textvariable=dtlabel)\
        .grid(column=1, row=6, sticky='w', padx=20, pady=20)

    # Button to close the GUI
    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=6, row=12)

    # Combobox for medical image selection
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

    # Combobox for ecg selection
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

    # Display the selected medical image
    resized_medical_nd = process_b64(patient_info["medical_images_b64"][0])
    tk_medical_image = ImageTk.\
        PhotoImage(image=Image.fromarray(resized_medical_nd))
    medical_image_label = ttk.Label(root, image=tk_medical_image)
    medical_image_label.configure(image=tk_medical_image)
    medical_image_label.grid(column=3, row=1, rowspan=4, columnspan=2)

    # Display the latest ECG trace for the patient
    resized_ecg_nd = process_b64(patient_info["ecg_images_b64"][-1])
    tk_latest_ecg = ImageTk.\
        PhotoImage(image=Image.fromarray(resized_ecg_nd))
    latest_ecg_image_label = ttk.Label(root, image=tk_latest_ecg)
    latest_ecg_image_label.configure(image=tk_latest_ecg)
    latest_ecg_image_label.grid(column=0, row=7, columnspan=2)

    # Display the selected ECG trace from the combobox
    resized_ecg_nd = process_b64(patient_info["ecg_images_b64"][0])
    tk_ecg_image = ImageTk.\
        PhotoImage(image=Image.fromarray(resized_ecg_nd))
    ecg_image_label = ttk.Label(root, image=tk_ecg_image)
    ecg_image_label.configure(image=tk_ecg_image)
    ecg_image_label.grid(column=3, row=7, columnspan=2)

    # Save buttons to allow users to save any image they like locally
    save_last_ecg_button = ttk.Button(root, text="Save",
                                      command=save_latest_ecg)
    save_last_ecg_button.grid(column=0, row=8, columnspan=2)
    save_selected_ecg_button = ttk.Button(root, text="Save",
                                          command=save_ecg)
    save_selected_ecg_button.grid(column=3, row=8, columnspan=2)
    save_medical_image_button = ttk.Button(root, text="Save",
                                           command=save_medical_image)
    save_medical_image_button.grid(column=3, row=5, columnspan=2)

    # Function to retrieve latest information from the database every
    # 10 seconds and display it in the GUI
    refresh()

    root.mainloop()


if __name__ == '__main__':
    design_window()
