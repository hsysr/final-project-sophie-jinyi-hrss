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

    # Start GUI
    root.mainloop()


if __name__ == '__main__':
    main_window()
