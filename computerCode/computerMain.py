import AirtableLib
import paho.mqtt.client as mqtt
import time

def makeClient():
    # Adafruit IO MQTT broker information
    ADAFRUIT_IO_URL = "io.adafruit.com"
    ADAFRUIT_IO_PORT = 1883
    ADAFRUIT_IO_KEY = ""
    ADAFRUIT_IO_USERNAME = "tmartello"

    # Create an MQTT client instance
    client = mqtt.Client()

    # Set the username and password for Adafruit IO
    client.username_pw_set(username=ADAFRUIT_IO_USERNAME, password=ADAFRUIT_IO_KEY)

    # Connect to the Adafruit IO MQTT broker
    client.connect(ADAFRUIT_IO_URL, port=ADAFRUIT_IO_PORT)

    return client

def main():
    # initialize client and hex codes
    client = makeClient()
    codes = {"Red": "#E13C38", "Green": "#338237"}

    try:
        while True:
            # Retrieve color from airtable
            color = AirtableLib.getColor()
            print(color)

            # Find corresponding hex code
            hexCode = codes[color]

            # Publish the value to the feed
            topic1 = "tmartello/feeds/midtermdata.currcolor"
            client.publish(topic1, color)
            print("published color")

            topic2 = "tmartello/feeds/midtermdata.colorcode"
            client.publish(topic2, hexCode)
            print("published code")

            time.sleep(8)
    except KeyboardInterrupt:
        client.disconnect()


main()
