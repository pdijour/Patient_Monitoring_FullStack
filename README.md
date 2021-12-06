Patient Monitoring Client/Server Project
BME 547 Final Project - Michael Tian and Phoebe Dijour

A detailed README describing the final performance and state of your project. This should include a basic instruction manual for your GUI clients, an API reference guide for your server, and a description of your database structure.

Basic instruction manual
1. The cloud server script will be running on a virtual machine which can be accessed using the following url: 
2. Patients will upload their information using the  patient_GUI, and providers on the other hand will need to have both the cloud client script as well as the  provider_GUI script. 



Database Structure
MongoDB - For this class, we will be using a non-relational database called MongoDB. It is easy to set-up and use. A database is just like any other program that runs on a computer. This program could be running on your own computer, on a virtual machine, or a cloud service. Our Python code accesses the database by making requests to the database API.

We will be accessing the MongoDB database from our Python code using a package called PyMODM which gives us access to the MongoDB API, but also enforces type-checking which is very helpful from a programming perspective.

Database definitions
    name = fields.CharField()
    medical_record_number = fields.IntegerField(primary_key=True)
    medical_images = fields.ListField()
    medical_images_b64 = fields.ListField()
    ecg_images = fields.ListField()
    ecg_images_b64 = fields.ListField()
    heart_rates = fields.ListField()
    datetimes = fields.ListField()
