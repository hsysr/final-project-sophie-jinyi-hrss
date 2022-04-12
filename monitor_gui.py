import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
import monitor_api as api
import helper
import io
import base64


global record
record = None


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
        global record
        MRN_entry.set("Select patient MRN")
        MRN_dropdown["values"] = ()
        reset_record()

    def reset_record():
        """ Clear all entry except for MRN_dropdown
        Clear all entry except for MRN_dropdown when select a new MRN
        """
        global record
        name_string.set("None")
        latest_heart_rate_string.set("None")
        latest_ECG_label.configure(image=tk_blank_image_latest_ECG)
        latest_ECG_label.image = tk_blank_image_latest_ECG
        date_latest_ECG_string.set("None")
        ECG_entry.set("Select ECG image")
        ECG_dropdown["values"] = ()
        selected_heart_rate_string.set("None")
        selected_ECG_label.configure(image=tk_blank_image_selected_ECG)
        selected_ECG_label.image = tk_blank_image_selected_ECG
        date_selected_ECG_string.set("None")
        medical_entry.set("Select medical image")
        medical_dropdown["values"] = ()
        selected_medical_label.configure(image=tk_blank_image_selected_med)
        selected_medical_label.image = tk_blank_image_selected_med
        date_selected_medical_string.set("None")
        status_label.configure(text="Status")
        MRN_dropdown.now = None
        ECG_dropdown.idx = None
        medical_dropdown.idx = None
        record = None

    def display_mrnlist_handler():
        """ Handles Retrieving list of MRN upon click of "Select MRN image"
        When the user clicks on the "Select MRN image" dropdown box, this
        function is run which calls theretrieve_mrnlist_driver() to
        retrieves up-to-date MRN list in thr database.
        """
        mrnlist = api.display_mrnlist_driver()
        MRN_dropdown["values"] = mrnlist

    def display_record_cmd(event):
        """ Get record of the selected MRN and display latest ECG
        When the user select a value under the dropdown box, this function
        would run store the MRN value under MRN_dropdown.now, and
        will call update_record_handler to update the display of the latest
        ECG image.

        :param event: event user select a value under the combobox
        """
        reset_record()
        MRN_dropdown.now = MRN_dropdown["values"][MRN_dropdown.current()]
        status_label.configure(
            text="Patient {} selected".format(MRN_dropdown.now))
        update_record_handler()

    def update_record_handler():
        """ Handles update_record driver, store record and display the
        latest ECG When the user select a value under the dropdown box,
        this function would run and call te driver to update the record.
        THis function would also run every 2000msec, to automatically
        update the record.
        """
        global record
        record = api.update_record_driver(MRN_dropdown.now)
        name_string.set(record["name"])
        latest_heart_rate_string.set(record["heart_rate"][-1])
        tk_latest_ECG_image = format_image(record["ECG_image"][-1])
        latest_ECG_label.image = tk_latest_ECG_image
        latest_ECG_label.configure(image=tk_latest_ECG_image)
        date_latest_ECG_string.set(record["ECG_timestamp"][-1])
        root.after(2000, update_record_handler)

    def format_image(base64_string):
        """ format the base64 image to ImageTk of size 150x150
        call functions in base64 and PIL to convert the base64 string
        to ImageTk of size 150x150

        :param base64_string: base64 string of the input image
        :returns: ImageTk object
        """
        imgdata = base64.b64decode(str(base64_string))
        image = Image.open(io.BytesIO(imgdata)).resize((150, 150))
        tk_image = ImageTk.PhotoImage(image)
        return tk_image

    def download_cmd(base64_string, filename):
        """ Download images upon click of "Download" button
        When the user clicks on the "Download" button, this function would
        download the image represented by base64_string.

        :param base64_string: base64 string of the input image
        :param filename: filename of the downloaded image
        :returns: None
        """
        # base64_string = record["ECG_timestamp"][-1]
        # filename = record["ECG_timestamp"][-1][:10] + "ECG.jpg"
        # f = asksaveasfile(
        #     initialfile=filename,
        #     defaultextension=".jpg",
        #     filetypes=[("All Files","*.*"),("Image Documents","*.jpg")])
        helper.b64_string_to_file(base64_string, filename)
        status_label.configure(
            text="{} downloaded successfully".format(filename))

    def display_ECG_list_cmd():
        """ Retrieve list of ECG upon click of "Select ECG image" dropdown
        When the user clicks on the "Select ECG image" dropdown box, this
        function is run which retrieves up-to-date ECG image list of the
        selected patient.
        """
        global record
        if record is None:
            status_label.configure(text="Please select a patient MRN first")
            return
        ECG_dropdown["values"] = record["ECG_timestamp"]

    def display_selected_ECG_cmd(event):
        """ Retrieve corresponding ECG_image upon selection of ECG_dropdown
        When the user clicks on the value under ECG_dropdown box, this
        function is run which displays the selected ECG image of the
        selected patient.
        :param event: automatically generated by event, not used
        """
        ECG_timestamp = ECG_dropdown["values"][ECG_dropdown.current()]
        status_label.configure(
            text="ECG image at {} selected".format(ECG_timestamp))
        ECG_idx = record["ECG_timestamp"].index(ECG_timestamp)
        selected_heart_rate_string.set(record["heart_rate"][ECG_idx])
        tk_selected_ECG_image = format_image(record["ECG_image"][ECG_idx])
        selected_ECG_label.image = tk_selected_ECG_image
        selected_ECG_label.configure(image=tk_selected_ECG_image)
        date_selected_ECG_string.set(ECG_timestamp)
        ECG_dropdown.idx = ECG_idx

    def display_medical_list_cmd():
        """ Retrieve list of medical image upon click of "Select medical
        image" dropdown When the user clicks on the "Select ECG image"
        dropdown box, this function is run which retrieves up-to-date
        medical image list of the selected patient.
        """
        global record
        if record is None:
            status_label.configure(text="Please select a patient MRN first")
            return
        medical_dropdown["values"] = record["medical_timestamp"]

    def display_selected_medical_cmd(event):
        """ Retrieve corresponding medical_image upon selection of ECG_dropdown
        When the user clicks on the value under ECG_dropdown box, this
        function is run which displays the selected ECG image of the
        selected patient.
        """
        medical_timestamp = \
            medical_dropdown["values"][medical_dropdown.current()]
        status_label.configure(
            text="Medical image at {} selected".format(medical_timestamp))
        medical_idx = record["medical_timestamp"].index(medical_timestamp)
        tk_selected_medical_image = format_image(
            record["medical_image"][medical_idx])
        selected_medical_label.image = tk_selected_medical_image
        selected_medical_label.configure(image=tk_selected_medical_image)
        date_selected_medical_string.set(medical_timestamp)
        medical_dropdown.idx = medical_idx

    # Create root/base window
    root = tk.Tk()
    root.title("Monitoring Station")
    root.geometry("800x780")

    # Patient MRN selection
    ttk.Label(root, text="Patient MRN:").grid(
        column=0, row=0, padx=5, pady=20, sticky=tk.W)
    MRN_entry = tk.StringVar()
    MRN_entry.set("Select patient MRN")
    MRN_dropdown = ttk.Combobox(root, textvariable=MRN_entry,
                                postcommand=display_mrnlist_handler)
    MRN_dropdown.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
    MRN_dropdown.now = None
    MRN_dropdown["values"] = ()
    MRN_dropdown.state(['readonly'])
    MRN_dropdown.bind('<<ComboboxSelected>>', display_record_cmd)

    # Area1 latest ECG
    # Patient name
    ttk.Label(root, text="Patient name:").grid(column=0, row=1,
                                               padx=5, pady=5,
                                               sticky=tk.W)
    name_string = tk.StringVar()
    name_string.set("None")
    # Will be replaced by the name of the selected patient
    ttk.Label(root, textvariable=name_string).grid(
        column=1, row=1, padx=5, pady=5, sticky=tk.W)

    # Latest heart rate
    ttk.Label(root, text="Latest heart rate:").grid(
        column=0, row=2, padx=5, pady=5, sticky=tk.W)
    latest_heart_rate_string = tk.StringVar()
    latest_heart_rate_string.set("None")
    ttk.Label(root, textvariable=latest_heart_rate_string).grid(
        column=1, row=2, padx=5, pady=5, sticky=tk.W)

    # Latest ECG image
    ttk.Label(root, text="Latest ECG image:").grid(
        column=0, row=3, padx=5, pady=5, sticky=tk.W)
    blank_image_latest_ECG = Image.open(
        "images/blank-avatar.jpg").resize((150, 150))
    tk_blank_image_latest_ECG = ImageTk.PhotoImage(blank_image_latest_ECG)
    latest_ECG_label = ttk.Label(root, image=tk_blank_image_latest_ECG)
    latest_ECG_label.grid(
        column=0, row=4, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Latest ECG image datatime
    ttk.Label(root, text="Date of latest ECG image:").grid(
        column=0, row=6, padx=5, pady=5, sticky=tk.W)
    date_latest_ECG_string = tk.StringVar()
    # Display Latest heart rate
    date_latest_ECG_string.set("None")
    ttk.Label(root, textvariable=date_latest_ECG_string).grid(
        column=1, row=6, padx=5, pady=5, sticky=tk.W)

    # download ECG image
    ttk.Button(
        root, text="Download",
        command=lambda: download_cmd(
            record["ECG_image"][-1], record["ECG_timestamp"][-1][:10] +
            "ECG.jpg")).grid(column=0, row=7, padx=5, pady=5, sticky=tk.W)

    # Area2 historical ECG
    # Select historical ECG
    ttk.Label(root, text="Historical ECG image:").grid(
        column=2, row=1, padx=5, pady=5, sticky=tk.W)
    ECG_entry = tk.StringVar()
    ECG_entry.set("Select ECG image")
    ECG_dropdown = ttk.Combobox(
        root, textvariable=ECG_entry, postcommand=display_ECG_list_cmd)
    ECG_dropdown.grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
    ECG_dropdown["values"] = ()
    ECG_dropdown.state(['readonly'])
    ECG_dropdown.bind('<<ComboboxSelected>>', display_selected_ECG_cmd)

    # Selected heart rate
    ttk.Label(root, text="Selected heart rate:").grid(
        column=2, row=2, padx=5, pady=5, sticky=tk.W)
    # Display Selected heart rate
    selected_heart_rate_string = tk.StringVar()
    selected_heart_rate_string.set("None")
    ttk.Label(root, textvariable=selected_heart_rate_string).grid(
        column=3, row=2, padx=5, pady=5, sticky=tk.W)

    # Display selected ECG image
    ttk.Label(root, text="Selected ECG image:").grid(
        column=2, row=3, padx=5, pady=5, sticky=tk.W)
    blank_image_selected_ECG = Image.open(
        "images/blank-avatar.jpg").resize((150, 150))
    tk_blank_image_selected_ECG = ImageTk.PhotoImage(blank_image_selected_ECG)
    selected_ECG_label = ttk.Label(root, image=tk_blank_image_selected_ECG)
    selected_ECG_label.grid(
        column=2, row=4, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Selected ECG image datatime
    ttk.Label(root, text="Date of selected ECG image:").grid(
        column=2, row=6, padx=5, pady=5, sticky=tk.W)
    date_selected_ECG_string = tk.StringVar()
    date_selected_ECG_string.set("None")
    ttk.Label(root, textvariable=date_selected_ECG_string).grid(
        column=3, row=6, padx=5, pady=5, sticky=tk.W)

    # download ECG image
    ttk.Button(root, text="Download", command=lambda: download_cmd(
            record["ECG_image"][ECG_dropdown.idx],
            record["ECG_timestamp"][ECG_dropdown.idx][:10] +
            "ECG.jpg")).grid(
        column=2, row=7, padx=5, pady=5, sticky=tk.W)

    # blank line
    ttk.Label(root, text='------------------------------').grid(
        column=0, row=8, padx=5, pady=5, columnspan=4, sticky=tk.W)

    # Area3 historical medical image
    # Select historical medical image name
    ttk.Label(root, text="Medical image:").grid(
        column=0, row=9, padx=5, pady=5, sticky=tk.W)
    medical_entry = tk.StringVar()
    medical_entry.set("Select medical image")
    medical_dropdown = ttk.Combobox(
        root, textvariable=medical_entry, postcommand=display_medical_list_cmd)
    medical_dropdown.grid(column=1, row=9, padx=5, pady=5, sticky=tk.W)
    medical_dropdown["values"] = ()
    medical_dropdown.state(['readonly'])
    medical_dropdown.bind('<<ComboboxSelected>>', display_selected_medical_cmd)

    # Display medical image
    ttk.Label(root, text="Selected medical image:").grid(
        column=0, row=10, padx=5, pady=5, sticky=tk.W)
    blank_image_selected_med = Image.open(
        "images/blank-avatar.jpg").resize((150, 150))
    tk_blank_image_selected_med = ImageTk.PhotoImage(blank_image_selected_med)
    selected_medical_label = ttk.Label(root, image=tk_blank_image_selected_med)
    selected_medical_label.grid(
        column=0, row=11, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.W)

    # Selected medical image datatime
    ttk.Label(root, text="Date of selected medical image:").grid(
        column=0, row=13, padx=5, pady=5, sticky=tk.W)
    date_selected_medical_string = tk.StringVar()
    date_selected_medical_string.set("None")
    ttk.Label(root, textvariable=date_selected_medical_string).grid(
        column=1, row=13, padx=5, pady=5, sticky=tk.W)

    # download medical emage
    ttk.Button(
        root, text="Download", command=lambda: download_cmd(
            record["medical_image"][medical_dropdown.idx],
            record["medical_timestamp"][medical_dropdown.idx][:10] +
            "medical.jpg")).grid(column=0, row=14, padx=5, pady=5, sticky=tk.W)

    # Status indicator
    status_label = ttk.Label(root, text="Status")
    status_label.grid(column=2, row=13, columnspan=2, sticky=tk.W)

    # main buttons
    ttk.Button(root, text="Clear", command=clear_cmd).grid(
        column=2, row=15, sticky=tk.W)
    ttk.Button(root, text="Cancel", command=cancel_cmd).grid(
        column=3, row=15, sticky=tk.W)

    root.after(2000, update_record_handler)
    root.mainloop()


if __name__ == '__main__':
    main_window()
