import math
import random
import sys
import paho.mqtt.client as mqtt
import time


class Publisher:

    mqttClient = None
    broker = None
    #  THESE ARE TAKEN FROM THE CONFIG FILES
    root_topic_ALL = None
    root_topic_HASH = None
    username = None
    password = None
    clientID = None
    #  THESE ARE GENERATED AND FORMATTED:
    #   - root_topic_ALL + clientID
    #   - root_topic_HASH + clientID
    topic_ALL = None
    topic_HASH = None

    def __init__(self):
        self.mqttClient = []

        self.topic_ALL = []
        self.topic_HASH = []

    def readConfigFile(self):
        f = open("config.txt", "r")
        for _singleLine in f:
            if _singleLine[0] == '#':  # Commented line
                continue

            _singleLine = _singleLine.replace(" ", "")  # Remove any blank spaces
            _field = _singleLine[:_singleLine.index('=')]
            _value = _singleLine[_singleLine.index('=')+1:].rstrip("\r\n")

            if _field == 'broker':
                self.broker = _value
            elif _field == 'root_topic_ALL':
                self.root_topic_ALL = _value
            elif _field == 'root_topic_HASH':
                self.root_topic_HASH = _value
            elif _field == 'username':
                self.username = _value
            elif _field == 'password':
                self.password = _value
            elif _field == 'clientID':
                self.clientID = _value.split(",")
            else:
                print("Error in the configuration file 'config.txt'")
                print("Check the fields names!!")
                exit(0)

        for _clientID in self.clientID:
            self.topic_ALL.append(self.root_topic_ALL + _clientID)
            # print(f"Topic ALL: {self.topic_ALL}")
            self.topic_HASH.append(self.root_topic_HASH + _clientID)
            # print(f"Topic HASH: {self.topic_ALL}")

        return None

    def connect_mqtt(self, cltID, usrName, psswrd, brk):
        def on_connect(client, userdata, flags, rc):
            print("on_connect")
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        _client = mqtt.Client(client_id=cltID)
        _client.username_pw_set(username=usrName, password=psswrd)
        _client.on_connect = on_connect
        _client.connect(host=brk)  # default port 1883
        return _client

    # msgAsString is string formatted as follows:
    # "x,y,z;x,y,z;x,y,z"
    def publish(self, client, topic, msgAsString):
        result = client.publish(topic, msgAsString)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Topic: {topic} - Msg: {msgAsString}")
        else:
            print(f"Failed to send message to topic {topic}")


    # Simply test, do not call it
    '''
    def publish(client):
        x = 1
        y = 2
        z = 3

        while True:
            time.sleep(1)
            msg = f"x={x}, y={y}, z={z}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send {msg} to topic {topic}")
            else:
                print(f"Failed to send message to topic {topic}")

            x += 1
            y += 2
            z += 5
    '''

    def connectToBroker(self):
        # global mqttClient
        for _singleClient in self.clientID:
            self.mqttClient.append(self.connect_mqtt(cltID=_singleClient, usrName=self.username, psswrd=self.password, brk=self.broker))
            self.mqttClient[-1].loop_start()

    def sendAll(self, msgAsString):
        # global mqttClient
        for _i in range(len(self.topic_ALL)):
            self.publish(self.mqttClient[_i], self.topic_ALL[_i], msgAsString)

    def sendHash(self, msgAsString):
        for _i in range(len(self.topic_HASH)):
            self.publish(self.mqttClient[_i], self.topic_HASH[_i], msgAsString)


if __name__ == '__main__':

    ######################
    # ## --- MAIN --- ## #  --> Check the PARAMETERS as input to the python ("Edit configuration")
    ######################
    #  Must call this as follows:
    #       - main.py PUBLISHER_TYPE DATA_AS_STR
    #
    #   PUBLISHER_TYPE can be 0 or 1.
    #       - 0 --> Publish ALL
    #       - 1 --> Publish HASH
    #
    #   DATA_AS_STR is a string formatted as follows:
    #   "x,y,z;x,y,z;x,y,z"

    publisher = Publisher()

    publisher.readConfigFile()
    publisher.connectToBroker()

    # Fixed data
    # sendAll("10,20,30;40,50,60;10,20,30;40,50,60;10,20,30;40,50,60")

    # Random data
    '''
    while True:
        time.sleep(1)
        rndData = ""
        for i in range(1, 301):
            rndData += str(random.randint(0, 99))
            if i % 3 != 0:
                rndData += ','
            else:
                rndData += ';'
        rndData = rndData[:-1]
        sendAll(rndData)
    '''

    # Sine waves
    while True:
        time.sleep(1)
        fs = 100  # Hz

        A_x = 1500
        f_x = 5  # Hz
        O_x = 0

        A_y = 2000
        f_y = 10  # Hz
        O_y = 0

        A_z = 1000
        f_z = 4  # Hz
        O_z = 0

        # Noise
        snr_db = 0

        # Transform linear
        snr_linear = pow(10, (snr_db/10))
        nsAmplitude_x = pow(10, -(snr_db / 20)) * A_x
        nsAmplitude_y = pow(10, -(snr_db / 20)) * A_y
        nsAmplitude_z = pow(10, -(snr_db / 20)) * A_z

        sineData = ""

        pwr_s_x = 0
        pwr_n_x = 0

        pwr_s_y = 0
        pwr_n_y = 0

        pwr_s_z = 0
        pwr_n_z = 0
        for i in range(1, 100):
            sineData += "1234,"  # Fake absolute time

            s_x = A_x * math.sin(2 * math.pi * f_x * (i / fs)) + O_x
            n_x = nsAmplitude_x * random.randint(0, 1)
            pwr_s_x += pow(s_x, 2)
            pwr_n_x += pow(n_x, 2)

            s_y = A_y * math.sin(2 * math.pi * f_y * (i / fs)) + O_y
            n_y = nsAmplitude_y * random.randint(0, 1)
            pwr_s_y += pow(s_y, 2)
            pwr_n_y += pow(n_y, 2)

            s_z = A_z * math.sin(2 * math.pi * f_z * (i / fs)) + O_z
            n_z = nsAmplitude_z * random.randint(0, 1)
            pwr_s_z += pow(s_z, 2)
            pwr_n_z += pow(n_z, 2)

            sineData += str(s_x + n_x) + ','
            sineData += str(s_y + n_y) + ','
            sineData += str(s_z + n_z) + ';'

        snr_db_x = 10 * math.log10(pwr_s_x / pwr_n_x)
        snr_db_y = 10 * math.log10(pwr_s_y / pwr_n_y)
        snr_db_z = 10 * math.log10(pwr_s_z / pwr_n_z)
        print(f"SNR X: {snr_db_x} [dB]")
        print(f"SNR Y: {snr_db_y} [dB]")
        print(f"SNR Z: {snr_db_z} [dB]")
        publisher.sendAll(sineData)

    # SINGLE SEND
    '''
    whichPublisher = int(sys.argv[1])
    inMsg = str(sys.argv[2])

    if whichPublisher == 0:  # Publish ALL
        publisher.sendAll(inMsg)
    elif whichPublisher == 1:  # Publish HASH
        publisher.sendHash(inMsg)
    else:
        print("Wrong parameter choice.")
    '''
