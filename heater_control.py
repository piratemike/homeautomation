import paho.mqtt.client as mqtt

TEMPERATURE_QUEUE = "temperature"
DESIRED_TEMP_QUEUE = "desired_temp"
HEATER_CTRL_QUEUE = "heater_ctrl"
HEATER_STATE_QUEUE = "heater_state"

broker_address="localhost"
mqtt_client = mqtt.Client("heater_control")


DESIRED_TEMP = 21
HEATER_ON = False

def on_connect(client, userdata, flags, rc):
    print("Connected")


def on_message(client1, userdata, message):
    global HEATER_ON
    global DESIRED_TEMP
    payload = message.payload.decode("utf-8")
    print("message {} received from topic {}".format(payload, message.topic))
    if message.topic == TEMPERATURE_QUEUE:
        temperature = float(payload)
        if temperature < DESIRED_TEMP and not HEATER_ON:
            print("Turning heater on")
            mqtt_client.publish(HEATER_CTRL_QUEUE, "ON")
        elif temperature > DESIRED_TEMP and HEATER_ON:
            print("Turning heater off")
            mqtt_client.publish(HEATER_CTRL_QUEUE, "OFF")
    elif message.topic == HEATER_STATE_QUEUE:
        if payload == "ON":
            print("Setting heater state to ON")
            HEATER_ON = True
        elif payload == "OFF":
            print("Setting heater state to OFF")
            HEATER_ON = False
    elif message.topic == DESIRED_TEMP_QUEUE:
        print("Setting desired temperature to {}".format(payload))
        DESIRED_TEMP = int(payload)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(broker_address)
mqtt_client.subscribe([(TEMPERATURE_QUEUE, 0),
                       (HEATER_STATE_QUEUE, 0),
                       (DESIRED_TEMP_QUEUE, 0)])
mqtt_client.loop_forever()