import paho.mqtt.client as mqtt

SCENE_SELECT_QUEUE = "scene_select"
DESIRED_TEMP_QUEUE = "desired_temp"

broker_address="localhost"
mqtt_client = mqtt.Client("scene_controller")

SCENE_COMMAND_MAP = {
    'night': [(DESIRED_TEMP_QUEUE, "18")],
    'daytime': [(DESIRED_TEMP_QUEUE, "20")]
}


def on_connect(client, userdata, flags, rc):
    print("Connected")


def on_message(client1, userdata, message):
    payload = message.payload.decode("utf-8")
    print("message {} received from topic {}".format(payload, message.topic))
    if message.topic == SCENE_SELECT_QUEUE:
        scene_commands = SCENE_COMMAND_MAP[payload]
        for command in scene_commands:
            queue = command[0]
            value = command[1]
            mqtt_client.publish(queue, value)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(broker_address)
mqtt_client.subscribe([(SCENE_SELECT_QUEUE, 0)])
mqtt_client.loop_forever()