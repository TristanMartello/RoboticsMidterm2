from mqtt import MQTTClient
import secrets

class AdaMQTT:
    def __init__(self):
        # Initialize necessary variables to access the Adafruit dashboard
        self.url = "io.adafruit.com"
        self.port = 1883
        self.username = secrets.AdafruitUsername
        self.key = secrets.AdafruitApiKey
        # Initialize the MQTT client, and connect
        self.client = MQTTClient("umqtt_client", self.url, port=self.port, user=self.username, password=self.key)
        self.client.connect()
    
    def publishMessage(self, value, feedName):
        # Send the given message to the specified channel
        topic = f"{self.username}/feeds/{feedName}"
        self.client.publish(topic, str(value))
    
    def destroy(self):
        # Deinitialize the client when done
        self.client.disconnect()