import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog


def main_window():
    """Creates and runs a GUI for the health database
    This function creates a window that allows a user to enter patient
    information for eventual upload to a health database server.  Entires
    on the GUI include MRN, name, medical_image, medical_timestamp
    heart_rate, ECG_image, ECG_timestamp
    """
    # Create root/base window
    root = tk.Tk()
    root.title("Monitoring Station")
    root.geometry("600x800")

    ttk.Label(root, text="Blood Donor Database").grid(column=0, row=0,
                                                      columnspan=4,
                                                      sticky=tk.W)

    # Patient MRN selection
    ttk.Label(root, text="Patient MRN:").grid(column=0, row=1,
                                              padx=5, pady=5,
                                              sticky=tk.W)
    MRN_entry = tk.StringVar()
    MRN_entry.set("Select patient MRN")
    MRN_dropdown = ttk.Combobox(root, textvariable=MRN_entry)
    MRN_dropdown.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)
    MRN_dropdown["values"] = ("MRN1", "MRN2", "MRN3")  # would be replace
    MRN_dropdown.state(['readonly'])

    # Patient name
    ttk.Label(root, text="Patient name:").grid(column=0, row=2,
                                               padx=5, pady=5,
                                               sticky=tk.W)
    name_entry = tk.StringVar()
    name_entry.set("None")
    # Will be replaced by the name of the selected patient
    ttk.Label(root, textvariable=name_entry).grid(column=1, row=2,
                                                  padx=5, pady=5,
                                                  sticky=tk.W)

    # Heart rate
    ttk.Label(root, text="Latest heart rate:").grid(column=0, row=3,
                                                    padx=5, pady=5,
                                                    sticky=tk.W)
    heart_rate_entry = tk.StringVar()
    heart_rate_entry.set("None")
    ttk.Label(root, textvariable=heart_rate_entry).grid(column=1, row=3,
                                                        padx=5, pady=5,
                                                        sticky=tk.W)

    root.mainloop()


if __name__ == '__main__':
    main_window()
