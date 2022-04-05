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
    def cancel_cmd():
        """ Closes GUI window upon click of "Cancel" button
        When the user clicks on the "Cancel" button, this function is run
        which closes the main root GUI window.
        """
        root.destroy()

    def download_cmd():
        """ Download images upon click of "Download" button
        When the user clicks on the "Download" button, this function is run
        which download the corresponding image.
        """
        pass

    def retrieve_ECG_list():
        """ Retrieve list of ECG upon click of "Select ECG image" dropdown
        When the user clicks on the "Select ECG image" dropdown box, this function
        is run which retrieves up-to-date ECG image list of the selected patient.
        """
        pass

    # Create root/base window
    root = tk.Tk()
    root.title("Monitoring Station")
    root.geometry("800x600")

    # Patient MRN selection
    ttk.Label(root, text="Patient MRN:").grid(
        column=0, row=0, padx=5, pady=20, sticky=tk.W)
    MRN_entry = tk.StringVar()
    MRN_entry.set("Select patient MRN")
    MRN_dropdown = ttk.Combobox(root, textvariable=MRN_entry)
    MRN_dropdown.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
    MRN_dropdown["values"] = ("MRN1", "MRN2", "MRN3")  # would be replace
    MRN_dropdown.state(['readonly'])

    # Area1
    # Patient name
    ttk.Label(root, text="Patient name:").grid(column=0, row=1,
                                               padx=5, pady=5,
                                               sticky=tk.W)
    name_label = tk.StringVar()
    name_label.set("None")
    # Will be replaced by the name of the selected patient
    ttk.Label(root, textvariable=name_label).grid(
        column=1, row=1, padx=5, pady=5, sticky=tk.W)

    # Latest heart rate
    ttk.Label(root, text="Latest heart rate:").grid(
        column=0, row=2, padx=5, pady=5, sticky=tk.W)
    latest_heart_rate_label = tk.StringVar()
    latest_heart_rate_label.set("None")
    ttk.Label(root, textvariable=latest_heart_rate_label).grid(
        column=1, row=2, padx=5, pady=5, sticky=tk.W)

    # Latest ECG image
    ttk.Label(root, text="Latest ECG image:").grid(
        column=0, row=3, padx=5, pady=5, sticky=tk.W)
    blank_image_latest_ECG = Image.open("images/acl1.jpg").resize((200, 100))
    tk_blank_image_latest_ECG = ImageTk.PhotoImage(blank_image_latest_ECG)
    latest_ECG_label = ttk.Label(root, image=tk_blank_image_latest_ECG)
    latest_ECG_label.grid(
        column=0, row=4, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Latest ECG image datatime
    ttk.Label(root, text="Date of latest ECG image:").grid(
        column=0, row=6, padx=5, pady=5, sticky=tk.W)
    date_latest_ECG_label = tk.StringVar()
    date_latest_ECG_label.set("None")
    ttk.Label(root, textvariable=date_latest_ECG_label).grid(
        column=1, row=6, padx=5, pady=5, sticky=tk.W)

    # download ECG image
    ttk.Button(root, text="Download", command=download_cmd).grid(
        column=0, row=7, padx=5, pady=5, sticky=tk.W)

    # Area2
    # Select historical ECG
    ttk.Label(root, text="Select historical ECG image:").grid(
        column=2, row=1, padx=5, pady=5, sticky=tk.W)
    ECG_entry = tk.StringVar()
    ECG_entry.set("Select ECG image")
    ECG_dropdown = ttk.Combobox(
        root, textvariable=ECG_entry, postcommand = retrieve_ECG_list)
    ECG_dropdown.grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
    ECG_dropdown["values"] = ("Image1", "Image2", "Image3")  # would be replace
    ECG_dropdown.state(['readonly'])

    # Selected heart rate
    ttk.Label(root, text="Selected heart rate:").grid(
        column=2, row=2, padx=5, pady=5, sticky=tk.W)
    latest_heart_rate_label = tk.StringVar()
    latest_heart_rate_label.set("None")

    # Will be replaced by Latest heart rate of the selected patient
    ttk.Label(root, textvariable=latest_heart_rate_label).grid(
        column=3, row=2, padx=5, pady=5, sticky=tk.W)

    # Selected ECG image
    ttk.Label(root, text="Selected ECG image:").grid(
        column=2, row=3, padx=5, pady=5, sticky=tk.W)
    blank_image_selected_ECG = Image.open("images/acl1.jpg").resize((200, 100))
    tk_blank_image_selected_ECG = ImageTk.PhotoImage(blank_image_selected_ECG)
    selected_ECG_label = ttk.Label(root, image=tk_blank_image_selected_ECG)
    selected_ECG_label.grid(
        column=2, row=4, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Selected ECG image datatime
    ttk.Label(root, text="Date of selected ECG image:").grid(
        column=2, row=6, padx=5, pady=5, sticky=tk.W)
    date_selected_ECG_label = tk.StringVar()
    date_selected_ECG_label.set("None")
    ttk.Label(root, textvariable=date_selected_ECG_label).grid(
        column=3, row=6, padx=5, pady=5, sticky=tk.W)

    # download ECG emage
    ttk.Button(root, text="Download", command=download_cmd).grid(
        column=2, row=7, padx=5, pady=5, sticky=tk.W)

    root.mainloop()


if __name__ == '__main__':
    main_window()
