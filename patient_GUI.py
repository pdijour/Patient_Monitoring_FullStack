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
    """Creates a tkinter image variable than can be displayed on GUI

       This function receives the name of a file containing a digital image. It
       opens and stores the file as a Pillow image file and uses the
       Image.resize method to make the image 250x250 pixels. It then converts
       the Pillow image to a tk image.

       Parameters
        ----------
        filename : Str
            containing the name of the image file

       Returns
       -------
        Pillow.ImageTk.PhotoImage
            Containing a tk-compatible image variable
        filename
            Containing the name of the image file
       """
    pil_image = Image.open(filename)
    resized_image = pil_image.resize((250, 250))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image, filename


def change_file(starting, type):
    """Opens a file dialog box for the user to select an image

       This function uses the filedialog command .askopenfilename to open a file
       dialog box and allow the user to select an image. It opens in a specific
       directory and only allows users to select certain types of files.

       Parameters
        ----------
        starting: Str
            Contains the name of the default starting file directory
        type: Str
            Contains the type of file that the user can select

       Returns
       -------
        filename
            Containing the name that the user selected
       """
    filename = filedialog.askopenfilename(initialdir="{}".format(starting),
                                          filetypes=type)
    return filename


def add_files_to_server(patient_name, id_no, medical_files,
                        medical_files_b64, ecg_files, ecg_files_b64,
                        bpms, timestamps):
    """Makes post request to server to add patient information

       This function takes patient information as parameter inputs and makes
       a post request to the database server to store the information. It prints
       the server response to the console as well as returns it to the caller.

       Parameters
        ----------
        patient_name: Str
            Contains the patient's name
        id_no: int
            Contains the patient's medical record / ID number
        medical_files: Str
            Contains the file name of the medical image
        medical_files_b64: Str
            Contains the b64 string of the medical image
        ecg_files: Str
            Contains the file name of the ecg image
        ecg_files_b64: Str
            Contains the b64 string of the ecg image
        bpms: int
            Contains the heart rate for the chosen ecg file
        timestamps: Str
            Contains the date and time that the heart rate was determined

       Returns
       -------
        r.text
            Containing the server response to the post request
       """
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


def convert_file_to_b64_string(filename):
    """Converts image to b64 string

       This function opens the chosen filename and uses the base64.b64encode
       method to convert the file to a b64 string. If a filename that does not
       exist is entered, the function implement an exception within a try except
       block to return "no file." Otherwise, it returns the b64 string.

       Parameters
        ----------
        filename: Str
            Contains the name of the image file

       Returns
       -------
        b_64 string
            Containing the b64 string for the specified image file
       """
    try:
        with open(filename, "rb") as image_file:
            b64_bytes = base64.b64encode(image_file.read())
        b64_string = str(b64_bytes, encoding='utf-8')
    except FileNotFoundError:
        return "no file"
    return b64_string


def design_window():
    """Creates the patient-side GUI window for the database

        A GUI window is created that is the main interface for the database. It
        accepts information from the user (patient name, medical record number,
        and medical and ecg image filenames (from dialog boxes). The GUI
        includes "Select Image" buttons for the medical and ECG images. Upon
        clicking one of these, the GUI opens a file dialog box that allows the
        user to select an image. It displays the chosen images along with their
        filenames and calculates the heart rate for the chosen ECG .csv file.
        The GUI includes "Clear Image" buttons to clear both images. When it is
        pressed, the image and filename disappears and is removed from memory.
        The GUI also includes an "Upload" button. Upon hitting this button, the
        information is sent to the server and a return message is displayed
        below the button. Finally, the GUI includes a "Cancel" button that
        closes the GUI window.
      """
    def upload_button_cmd():
        """Event to run when Upload button is pressed

           This function works when the Upload button is pressed. It first gets
           data from the name and ID entry boxes. It implements two try except
           blocks to bet the ECG and Medical image filenames and b64 strings,
           which it acquires through an external function that converts image
           file to b64 strings. If the filename does not exist, it assigns empty
           lists to the variable. It uses the datetime function to get the
           date and time at which the button is pressed and then uses an
           external function in the server to add the files to the server. It
           then prints the response from the post request to the server in the
           GUI.
       """
        name = name_data.get()
        record_number = record_data.get()
        try:
            medical_filename = os.path.basename(medical_file_label.name)
            medical_b64 = convert_file_to_b64_string(medical_file_label.name)
        except AttributeError:
            medical_filename = ""
            medical_b64 = ""
        try:
            ecg_filename = os.path.basename(ecg_file_label.name)
            ecg_b64 = convert_file_to_b64_string(ecg_file_label.name)
            heart_rate = bpm_label.hr
        except AttributeError:
            ecg_filename = ""
            ecg_b64 = ""
            heart_rate = ""
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

    def clear_ecg_cmd():
        """Clears ECG filename and image from GUI

           This function is connected to the "Clear ECG Image" button of the
           GUI. It sets the labels fo the ECG filename and image to empty
           empty strings, effectively erasing the filename and image from the
           GUI.
          """        
        ecg_file_label.name = ''
        ecg_file_label.config(text='')
        ecg_image_label.config(image='')
        bpm_label.config(text='')

    def clear_medical_cmd():
        """Clears medical filename and image from GUI

           This function is connected to the "Clear Medical Image" button of the
           GUI. It sets the labels fo the ECG filename and image to empty
           empty strings, effectively erasing the filename and image from the
           GUI.
          """   
        medical_file_label.name = ''
        medical_file_label.config(text='')
        medical_image_label.config(image='')

    def cancel_cmd():
        """Closes window upon click of Cancel button

           This function is connected to the "Cancel" button of the GUI.  It
           destroys the root window causing the GUI interface to close.
          """
        root.destroy()

    def change_ecg_picture_cmd():
        """Allows user to select a new ECG file to display as an image

           This function opens a dialog box to allow the user to choose a .csv
           file. If the user does not cancel the dialog box, the chosen file is
           plotted and saved as a .png file. The file is then set sent to an
           external function for opening and resizing. The returned image is
           then added to the ecg_image_label widget for display on the GUI. The
           filename is added to the ecg_file_label widget for display. The heart
           rate is also calculated and added to the bpm_label widget for
           display.
          """
        filename = change_file("test_data", [("CSV Files", ".csv")])
        filename_png = "{}.png".format(filename.strip(".csv"))
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the file selection")
            return
        elif filename == "no file":
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
        """Allows user to select a new medical image to display

           This function opens a dialog box to allow the user to choose an image
           file. If the user does not cancel the dialog box, the chosen filename
           is sent to an external function for opening and resizing. The
           returned image is then added to the medical_image_label widget for
           display on the GUI. The filename is added to the medical_file_label
           for display.
          """
        filename = change_file("images",
                               [("Picture files", ".png .jpg .jpeg")])
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the image load")
            return
        elif filename == "no file":
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
    medical_file_label.grid(column=0, row=3, columnspan=2, padx=20)

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
    ecg_file_label.grid(column=3, row=3, columnspan=2, padx=20)

    change_picture_btn = ttk.Button(root, text="Choose ECG Data to Display",
                                    command=change_ecg_picture_cmd)
    change_picture_btn.grid(column=4, row=2, sticky='w', padx=20, pady=20)

    ttk.Label(root, text="Heart Rate:")\
        .grid(column=3, row=5, sticky='w', padx=20, pady=20)

    hr = ""

    bpm_label = ttk.Label(root, text=hr)
    bpm_label.grid(column=4, row=5, sticky='w', padx=20, pady=20)

    clear_medical_button = ttk.Button(root, text="Clear Medical Image",
                                      command=clear_medical_cmd)
    clear_medical_button.grid(column=0, row=6, columnspan=2)

    clear_ecg_button = ttk.Button(root, text="Clear ECG Image",
                                  command=clear_ecg_cmd)
    clear_ecg_button.grid(column=3, row=6, columnspan=2)

    upload_button = ttk.Button(root, text="Upload",
                               command=upload_button_cmd)
    upload_button.grid(column=0, row=7, columnspan=5, pady=[40, 0])

    output_string = ttk.Label(root, wraplength=500)
    output_string.grid(column=0, row=8, columnspan=5)

    cancel_button = ttk.Button(root, text="Cancel",
                               command=cancel_cmd)
    cancel_button.grid(column=5, row=7, pady=[40, 0])

    root.mainloop()


if __name__ == '__main__':
    design_window()
