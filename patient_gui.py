import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from helper import file_to_b64_string

from PIL import Image, ImageTk


medical_image_base64 = ""


def verify_GUI_inputs(input_id):
    try:
        id_integer = int(input_id)
    except ValueError:
        return False
    return id_integer


def main_window():
    """Creates and runs a GUI for the patient-side client

    This function creates a window that allows a user to enter patient
    information for eventual upload to a heart rate database server.
    Entires on the GUI include patient MRN, patient name, medical
    image and ECG data.
    """
    def cancel_cmd():
        """ Closes GUI window upon click of "Cancel" button
        When the user clicks on the "Cancel" button, this function is run
        which closes the main root GUI window.
        """
        root.destroy()

    def clear_cmd():
        """ Clear all entry upon click of "Clear" button
        When the user clicks on the "Clear" button, this function is run
        which clear all entry in the GUI window and change back to inital.
        """
        pass

    def ok_cmd():
        """ This function runs when the user clicks on the "Ok" button. It gets
        the entered data from the interface and call other functions that
        upload the data to a server.
        """
        pass

    def medical_image_cmd():
        global medical_image_base64
        filename = filedialog.askopenfilename()
        if filename == "":
            return
        new_medical_image = Image.open(filename).resize((350, 175))
        new_tk_image = ImageTk.PhotoImage(new_medical_image)
        medical_image_label.configure(image=new_tk_image)
        medical_image_label.image = new_tk_image
        medical_image_base64 = file_to_b64_string(filename)

    def ECG_data_cmd():
        pass

    # Create root/base window
    root = tk.Tk()
    root.title("Patient-side Client")
    root.geometry("750x600")

    # Patient MRN Entry
    ttk.Label(root, text="MRN:").grid(column=0, row=1, padx=20, pady=20)
    name_entry = tk.StringVar()
    ttk.Entry(root, width=20, textvariable=name_entry).grid(column=1, row=1)

    # Patient Name Entry
    ttk.Label(root, text="Name:")\
       .grid(column=0, row=2, padx=20, pady=0, sticky='n')
    id_entry = tk.StringVar()
    ttk.Entry(root, width=20, textvariable=id_entry)\
       .grid(column=1, row=2, sticky='n')

    # Select Medical Image
    ttk.Button(root, text="Select Medical Image", command=medical_image_cmd)\
       .grid(column=2, row=1, padx=140, pady=5, sticky='w')
    blank_image = Image.open("images/blank-avatar.jpg").resize((350, 175))
    medical_image = ImageTk.PhotoImage(blank_image)
    medical_image_label = ttk.Label(root, image=medical_image)
    medical_image_label\
        .grid(column=2, row=2, padx=140, pady=5,
              rowspan=2, columnspan=2, sticky='w')

    # Select ECG Data File
    ttk.Button(root, text="Select ECG Data File ", command=ECG_data_cmd)\
       .grid(column=2, row=4, padx=140, pady=20, sticky='w')
    ECG_image = ImageTk.PhotoImage(blank_image)
    ECG_image_label = ttk.Label(root, image=ECG_image)
    ECG_image_label\
        .grid(column=2, row=5, padx=140, pady=5,
              rowspan=2, columnspan=2, sticky='w')
    hr_label = ttk.Label(root, text="Heart Rate:")
    hr_label.grid(column=2, row=7, padx=140, pady=20, sticky='w')

    # Buttons
    ttk.Button(root, text="Clear", command=clear_cmd)\
       .grid(column=2, row=8, padx=195, sticky='w')
    ttk.Button(root, text="Ok", command=ok_cmd)\
       .grid(column=2, row=8, padx=300, sticky='w')
    ttk.Button(root, text="Cancel", command=cancel_cmd)\
       .grid(column=2, row=8, padx=405, sticky='w')

    # Status Label
    status_label = ttk.Label(root, text="Please Enter Patient information")
    status_label.grid(column=0, row=7, padx=20, columnspan=3, sticky='w')

    # Start GUI
    root.mainloop()


if __name__ == '__main__':
    main_window()
