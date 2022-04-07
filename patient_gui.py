import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk


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

    # Create root/base window
    root = tk.Tk()
    root.title("Patient-side Client")
    root.geometry("800x500")

    # Patient MRN Entry
    ttk.Label(root, text="MRN:").grid(column=0, row=1, padx=20, pady=20)
    name_entry = tk.StringVar()
    ttk.Entry(root, width=20, textvariable=name_entry).grid(column=1, row=1)

    # Patient Name Entry
    ttk.Label(root, text="Name:").grid(column=0, row=2, padx=20, pady=0)
    id_entry = tk.StringVar()
    ttk.Entry(root, width=20, textvariable=id_entry).grid(column=1, row=2)

    # Start GUI
    root.mainloop()


if __name__ == '__main__':
    main_window()
