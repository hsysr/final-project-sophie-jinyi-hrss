from pymodm import MongoModel, fields


class Patient(MongoModel):
    """ Description of data to be stored for each patient
    This class derives from the pymodm.MongoModel class and is used to define
    the structure of a document in the database for this server.  Each
    document will have four fields:
    name (CharField) will be a string containing the name of the patient
    MRN (IntegerField) will contain an integer that is the unique
        patient identifier.  This is the primary key of the database.
    name (Charfield) will contain a string that indicates the name
        of the patient
    heart_rate (ListField) will contain a list of integers of heart rate
    medical_image (ListField) will contain a list of base64 medical images
    medical_timestamp (ListField) will contain a list of datetime strings
        of the medical images
    ECG_image (ListField) will contain a list of base64 ECG images
    ECG_timestamp (ListField) will contain a list of datetime strings
        of the ECG images
    """

    MRN = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    medical_image = fields.ListField()
    medical_timestamp = fields.ListField()
    heart_rate = fields.ListField()
    ECG_image = fields.ListField()
    ECG_timestamp = fields.ListField()
