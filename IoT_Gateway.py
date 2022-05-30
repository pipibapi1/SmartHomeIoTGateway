import sys
from Adafruit_IO import MQTTClient
import serial.tools.list_ports
import time

AIO_USERNAME = "duy1711ak"
AIO_KEY = "aio_AiBw06MvLAKuH7qkApWKad6lFAFH"
AIO_FEED = ["iot-alarm", "iot-door", "iot-gas", "iot-secu", "iot-humi",
            "iot-temp", "iot-light", "iot-lightsys", "iot-switchlight", "alarmcontroller"]


def connected(client):
    print("Ket noi thanh cong ...")
    for feed in AIO_FEED:
        client.subscribe(feed)


def subscribe(client, userdata, mid, granted_qos):
    print(" Subcribe thanh cong ...")


def disconnected(client):
    print(" Ngat ket noi ...")
    sys.exit(1)

# chieu tu ada -> microbit


def message(client, feed_id, payload):
    print(" Nhan du lieu : " + feed_id + ': '+payload)
    if isMicrobitConnected:
        if (feed_id == "iot-secu"):
            ser.write(('door' + str(payload) + "#").encode())
        elif (feed_id == "iot-alarm"):
            ser.write(('gas' + str(payload) + "#").encode())
        elif (feed_id == "iot-switchlight"):
            client.publish('iot-light', payload)
            ser.write(('light' + str(payload) + "#").encode())
        elif (feed_id == "iot-lightsys"):
            ser.write(('lsys' + str(payload) + "#").encode())
        elif (feed_id == 'alarmcontroller'):
            if (payload == '1'):
                ser.write(('a0' + '#').encode())

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


def processData(data):
    data = data . replace("!", "")
    data = data . replace("#", "")
    splitData = data . split(":")
    print(splitData)
    topic = splitData[1]
    value = splitData[2]
    try:
        if (topic == 'TEMP'):
            client.publish("iot-temp", value)
        elif (topic == 'HUMID'):
            client.publish("iot-humi", value)
        elif (topic == 'LIGHT'):
            client.publish("iot-light", value)
        elif (topic == 'GAS'):
            client.publish("iot-gas", value)
        elif (topic == 'MAGNETIC'):
            client.publish("iot-door", value)
    except:
        pass


mess = ""


def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF -8")
        while ("#" in mess) and ("!" in mess):
            start = mess . find("!")
            end = mess . find("#")
            processData(mess[start: end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


isMicrobitConnected = False
if (getPort() != None):
    ser = serial.Serial(port= "COM3", baudrate=115200)
    isMicrobitConnected = True
time.sleep(2)
ser.write(('s#').encode())
while True:
    if isMicrobitConnected:
        readSerial()
    time.sleep(1)
