import json
import random
import datetime
import time
from paho.mqtt import client as mqtt
from MongoDB_Main import Document as Doc

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    subscribe = str(msg.payload.decode("utf-8"))
    subscribedData = json.loads(subscribe)
    print(subscribedData)
    eventData(subscribedData)

def eventData(data):
    col = "DeviceStatus"
    DeviceID= "Arima_01"
    ID = {"DeviceID": DeviceID }
    timestamp = str(datetime.datetime.now())
    data.update(ID)
    json.dumps(data, indent=4)
    deviceData = data["data"]["modbus"][0]
    windSpeed = int(deviceData["WIND_SPD"])
    if windSpeed > 10:
        windAlert: str = "High"
    elif windSpeed < 1:
        windAlert: str = "Low"
    else:
        windAlert: str = "Normal"
    data_to_DB = {
      "DeviceID": DeviceID,
      "temperature": int(deviceData["IN_TEMP"])/100,
      "uvindex": deviceData["SOLR_RADI"],
      "rainfall": deviceData["DAY_RAIN"],
      "humidity": deviceData["IN_HUMI"],
      "wind_speed": deviceData["WIND_SPD"],
      "wind_direction": deviceData["WIND_DIRT"],
      "soil_moisture": random.randint(32, 35),
      "soil_temperature": random.randint(32, 35),
      "dew_point": random.randint(32, 35),
      "wind_alert": windAlert,
      "timestamp": timestamp,
    }
    update = Doc().Write_Document(data=data_to_DB, col=col, DeviceID=DeviceID)
    if update == 0:
        Doc().DB_Write(data=data_to_DB, col=col)
    return data


# MQTT Main Function

subscriptiontopic = "IOTC3WSX0001/Event"
serveripaddress = "167.233.7.5"
serverport = 1883
client = mqtt.Client()
# connection must be dynamic
client.connect(serveripaddress, serverport,)
# connect to client
client.on_connect = on_connect
client.on_message = on_message

client.subscribe(subscriptiontopic)
print("Subscribed to the topic")
time.sleep(3)
client.loop_forever()





