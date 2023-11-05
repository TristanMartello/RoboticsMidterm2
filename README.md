# RoboticsMidterm2
The individual, second part of the ME35 midterm involving a temperature sensor, communication with two databases (Adafruit and Airtable), and three communicating programs.

This project involves python code simultaneously running on three different machines- the Raspberry Pi Pico, my computer, and OpenCV. The code files are grouped accordingly. 

The Pico code does the most work, and therefore has the most libraries. The file picoMain.py houses an asynchronous loop that trades off between the various simultaneous functions: reading thermistor and i2c gyroscope values, requesting color data from the Airtable API, posting temperature data to the Adafruit dashboard, and updating the OLED display screen. Most of these sub-tasks have an associated helper library; AccelLib.py reads and returns gyroscope data, AdaMqttLib.py handles sending messages to the Adafruit dashboard, AirtableLib.py sends and processes the get requests to the airtable database, and i2cScreen manages the changing graphics of the OLED display. 
