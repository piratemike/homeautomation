from functools import partial
import traceback

import serial
from serial.threaded import LineReader, ReaderThread
import paho.mqtt.client as mqtt

INCOMMING = 'arduino/incoming'
OUTGOING = 'arduino/outgoing'

client = mqtt.Client()


class SerialDataReader(LineReader):
    def connection_made(self, transport):
        super(SerialDataReader, self).connection_made(transport)
        print("port opened")

    def handle_line(self, data):
        client.publish(INCOMMING, data)
        print('line received: {}\n'.format(data))

    def connection_lost(self, exc):
        raise exc
        print("port opened")


def connected(mosq, obj, rc):
    print("Connected to MQTT!  Listening for {0} changes...".format(OUTGOING))
    client.subscribe(OUTGOING)


def message(serial_protocol, mosq, obj, msg):
    payload = str(msg.payload.decode("utf-8"))
    print('Feed {0} received new value: {1}'.format(msg.topic, payload))
    if payload == 'HTRON':
        print("Writing ON to serial")
        serial_protocol.write_line("HTRON")
    else:
        print("Writing OFF to serial")
        serial_protocol.write_line("HTROFF")

if __name__ == '__main__':
    try:
        # try and connect to ttyACM0
        ser = serial.serial_for_url('/dev/ttyACM0', baudrate=9600, timeout=1)
    except serial.SerialException:
        # that failed, try ttyACM1 instead
        ser = serial.serial_for_url('/dev/ttyACM1', baudrate=9600, timeout=1)

    client.on_connect = connected

    # Connect to the MQTT server.
    client.connect('localhost')

    with ReaderThread(ser, SerialDataReader) as protocol:
        client.on_message = partial(message, protocol)
        client.loop_forever()

