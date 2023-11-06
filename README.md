# RoboticsMidterm2
The individual, second part of the ME35 midterm involving a temperature sensor, communication with two databases (Adafruit and Airtable), and three communicating programs.

This project involves python code simultaneously running on three different machines- the Raspberry Pi Pico, my computer, and OpenCV. The code files are grouped accordingly. 

The Pico code does the brunt of the work for this project. I wanted the main loop to be as streamlined and easy to read as possible, so I made several libraries to outsource the complicated processes. The file picoMain.py houses an asynchronous loop that trades off between the various simultaneous functions, each of which has a library specifically designed to make that task easier. The tasks and associated libraries are listed here:
- Reading thermistor (no library)
- Reading i2c Gyroscope values (AccelLib.py)
- Requesting color data from the Airtable API (AirtableLib.py)
- Sending color data through MQTT to the Adafruit Dashboard (AdaMqttLib.py)
- Creating and updating the i2c OLED display screen (i2cScreen.py)

This is a bunch of different tasks for the Pico to do, but the control flow is simple: the program starts an asynchronous loop that cycles through all of the tasks at their respective rates. The main current problem with this code is that the Airtable requests take significantly longer than any other subtask, so whenever that communication is happening all other functions slow down.


The openCV code is more straightforward, the only helper function is to run a color isolation algorithm on a grayscale image to differentiate bright values of a single color, and bright values of all colors. The program runs this isolation function for each of the main rgb colors, determines the most prominent one, and updates the Airtable cell with that value.

Similarly, the computer main function is much more streamlined. The computer in this project is essentially just a middleman between the two dashboards; the code reads color data from the Airtable cell, determines the associated unit system and hex code for the Adafruit dashboard, and uses MQTT messages to send that information into the correct feeds. 
