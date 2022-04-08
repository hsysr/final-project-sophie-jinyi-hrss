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

    def clear_cmd():
        """ Clear all entry upon click of "Clear" button
        When the user clicks on the "Clear" button, this function is run
        which clear all entry in the GUI window and change back to inital.
        """
        MRN_entry.set("Select patient MRN")
        name_label.set("None")
        latest_heart_rate_label.set("None")
        latest_ECG_label.image = tk_blank_image_latest_ECG
        date_latest_ECG_label.set("None")
        ECG_entry.set("Select ECG image")
        selected_heart_rate_label.set("None")
        selected_ECG_label.image = tk_blank_image_selected_ECG
        date_selected_ECG_label.set("None")
        med_entry.set("Select medical image")
        selected_medical_label.image = tk_blank_image_selected_med
        date_selected_med_label.set("None")
        status_label.configure(text="Status")

    def download_cmd():
        """ Download images upon click of "Download" button
        When the user clicks on the "Download" button, this function is run
        which download the corresponding image.
        """
        pass

    def retrieve_ECG_list():
        """ Retrieve list of ECG upon click of "Select ECG image" dropdown
        When the user clicks on the "Select ECG image" dropdown box, this
        function is run which retrieves up-to-date ECG image list of the
        selected patient.
        """
        pass

    def retrieve_med_list():
        """ Retrieve list of medical image upon click of "Select medical
        image" dropdown When the user clicks on the "Select ECG image"
        dropdown box, this function is run which retrieves up-to-date
        medical image list of the selected patient.
        """
        pass

    # Create root/base window
    root = tk.Tk()
    root.title("Monitoring Station")
    root.geometry("800x780")

    # Patient MRN selection
    ttk.Label(root, text="Patient MRN:").grid(
        column=0, row=0, padx=5, pady=20, sticky=tk.W)
    MRN_entry = tk.StringVar()
    MRN_entry.set("Select patient MRN")
    MRN_dropdown = ttk.Combobox(root, textvariable=MRN_entry)
    MRN_dropdown.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
    MRN_dropdown["values"] = ("MRN1", "MRN2", "MRN3")  # would be replace
    MRN_dropdown.state(['readonly'])

    # Area1 latest ECG
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
    blank_image_latest_ECG = Image.open("images/acl1.jpg").resize((150, 150))
    tk_blank_image_latest_ECG = ImageTk.PhotoImage(blank_image_latest_ECG)
    latest_ECG_label = ttk.Label(root, image=tk_blank_image_latest_ECG)
    latest_ECG_label.grid(
        column=0, row=4, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Latest ECG image datatime
    ttk.Label(root, text="Date of latest ECG image:").grid(
        column=0, row=6, padx=5, pady=5, sticky=tk.W)
    date_latest_ECG_label = tk.StringVar()
    # Display Latest heart rate
    date_latest_ECG_label.set("None")
    ttk.Label(root, textvariable=date_latest_ECG_label).grid(
        column=1, row=6, padx=5, pady=5, sticky=tk.W)

    # download ECG image
    ttk.Button(root, text="Download", command=download_cmd).grid(
        column=0, row=7, padx=5, pady=5, sticky=tk.W)

    # Area2 historical ECG
    # Select historical ECG
    ttk.Label(root, text="Historical ECG image:").grid(
        column=2, row=1, padx=5, pady=5, sticky=tk.W)
    ECG_entry = tk.StringVar()
    ECG_entry.set("Select ECG image")
    ECG_dropdown = ttk.Combobox(
        root, textvariable=ECG_entry, postcommand=retrieve_ECG_list)
    ECG_dropdown.grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
    ECG_dropdown["values"] = ("Image1", "Image2", "Image3")  # would be replace
    ECG_dropdown.state(['readonly'])

    # Selected heart rate
    ttk.Label(root, text="Selected heart rate:").grid(
        column=2, row=2, padx=5, pady=5, sticky=tk.W)
    # Display Selected heart rate
    selected_heart_rate_label = tk.StringVar()
    selected_heart_rate_label.set("None")
    # Will be replaced by Latest heart rate of the selected patient
    ttk.Label(root, textvariable=selected_heart_rate_label).grid(
        column=3, row=2, padx=5, pady=5, sticky=tk.W)

    # Display selected ECG image
    ttk.Label(root, text="Selected ECG image:").grid(
        column=2, row=3, padx=5, pady=5, sticky=tk.W)
    blank_image_selected_ECG = Image.open("images/acl1.jpg").resize((150, 150))
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

    # blank line
    ttk.Label(root, text='------------------------------').grid(
        column=0, row=8, padx=5, pady=5, columnspan=4, sticky=tk.W)

    # Area3 historical medical image
    # Select historical medical image name
    ttk.Label(root, text="Medical image:").grid(
        column=0, row=9, padx=5, pady=5, sticky=tk.W)
    med_entry = tk.StringVar()
    med_entry.set("Select medical image")
    med_dropdown = ttk.Combobox(
        root, textvariable=med_entry, postcommand=retrieve_med_list)
    med_dropdown.grid(column=1, row=9, padx=5, pady=5, sticky=tk.W)
    med_dropdown["values"] = ("Image1", "Image2", "Image3")
    med_dropdown.state(['readonly'])

    # Display medical image
    ttk.Label(root, text="Selected medical image:").grid(
        column=0, row=10, padx=5, pady=5, sticky=tk.W)
    blank_image_selected_med = Image.open("images/acl1.jpg").resize((150, 150))
    tk_blank_image_selected_med = ImageTk.PhotoImage(blank_image_selected_med)
    selected_medical_label = ttk.Label(root, image=tk_blank_image_selected_med)
    selected_medical_label.grid(
        column=0, row=11, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Selected medical image datatime
    ttk.Label(root, text="Date of selected medical image:").grid(
        column=0, row=13, padx=5, pady=5, sticky=tk.W)
    date_selected_med_label = tk.StringVar()
    date_selected_med_label.set("None")
    ttk.Label(root, textvariable=date_selected_med_label).grid(
        column=1, row=13, padx=5, pady=5, sticky=tk.W)

    # download ECG emage
    ttk.Button(root, text="Download", command=download_cmd).grid(
        column=0, row=14, padx=5, pady=5, sticky=tk.W)

    # Status indicator
    status_label = ttk.Label(root, text="Status")
    status_label.grid(column=2, row=13, sticky=tk.W)

    # main buttons
    ttk.Button(root, text="Clear", command=clear_cmd).grid(
        column=2, row=15, sticky=tk.W)
    ttk.Button(root, text="Cancel", command=cancel_cmd).grid(
        column=3, row=15, sticky=tk.W)

    root.mainloop()


if __name__ == '__main__':
    main_window()
