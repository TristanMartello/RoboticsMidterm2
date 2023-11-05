
# This code has a few different simultaneous tasks:
#   - Create + update screen display
#   - Read thermistor value
#      - Push thermistor val to Adafruit dashboard via MQTT
#      - Display val on the screen
#   - Read airtable cell for current color
#      - Display on screen
#      - Change units of temperature accordingly
#   - Take input from i2c Device
#      - Display on screen

import wifiLib
import secrets
import AirtableLib
import AccelLib as AL
from AdaMqttLib import AdaMQTT
from i2cScreen import i2cScreen
from machine import Pin, ADC
from math import log
import uasyncio as asyncio

r25 = 10000
beta = 3977

unit = "C"
temp = 25
gyros = [0, 0, 0]

async def readTemp(therm):
    global temp
    while True:
        r = 10000.0 / (65535 / float(therm.read_u16()) - 1)
        lnr = log(r / r25)
        degC = -273.15 + 1/(1/298.15 + lnr/beta)
        degF = degC*(9/5) + 32
        if unit == "C":
            temp = degC
        else:
            temp = degF
        print(temp)
        await asyncio.sleep_ms(500)

async def readAPI():
    global unit
    while True:
        color = AirtableLib.getColor()
        if color == "Red":
            unit = "F"
        else:
            unit = "C"
        await asyncio.sleep_ms(5000)

async def postTemp(ada):
    while True:
        ada.publishMessage(temp, "currTemp")
        print("Adafruit Message sent:", temp)
        await asyncio.sleep(300)

async def drawDisplay(screen):
    while True:
        sendTemp = float(f'{temp:.1f}')
        screen.mainDisplay(sendTemp, unit, gyros)
        await asyncio.sleep_ms(100)

async def readAccel(accel):
    global gyros
    while True:
        gyros = accel.allGyro()
        await asyncio.sleep_ms(300)

async def controlLoop(therm, ada, screen, accel):
    timeLimit = 60
    asyncio.create_task(drawDisplay(screen))
    asyncio.create_task(readTemp(therm))
    asyncio.create_task(readAccel(accel))
    asyncio.create_task(readAPI())
    asyncio.create_task(postTemp(ada))
    await asyncio.sleep(timeLimit)

    print('done')

def main():
    wifiLib.connect_wifi("home")
    ada = AdaMQTT()
    therm = ADC(26)
    screen = i2cScreen()
    accel = AL.accelerometer(1, 3, 2)
    
    try:
        asyncio.run(controlLoop(therm, ada, screen, accel))
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        screen.clear()
        ada.destroy()
        asyncio.new_event_loop()
        print('Loop finished, clear state')
    
main()
    
