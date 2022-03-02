from Constants import Const
import paho.mqtt.client as mqtt


class MQTT:

    def __init__(self):
        return None

    def connect_mqtt(self, cltID, usrName, psswrd, brk):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker! ")
            else:
                print("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        _client = mqtt.Client(client_id=cltID)
        _client.username_pw_set(username=usrName, password=psswrd)
        _client.on_connect = on_connect
        _client.connect(host=brk)  # default port 1883
        return _client

    def subscribe(self, clt, toWhichTopicSubscribe, callback):
        def on_message(client, userdata, msg):
            # print(f"Received {msg.payload.decode()} from {msg.topic} topic")
            callback(msg.topic, msg.payload.decode())

        # Subscribe to the topic ALL only
        if toWhichTopicSubscribe == Const.SUBSCRIBE_TO_TOPIC_ALL:
            for _clientID in Const.clientIDs:
                _topic = Const.root_topic_ALL + _clientID
                clt.subscribe(_topic)
                print(f"Subscribed to topic: {_topic}")
                Const.listOfTopicToSubscribeTo.append(_topic)

        # Subscribe to the topic HASH only
        elif toWhichTopicSubscribe == Const.SUBSCRIBE_TO_TOPIC_HASH:
            for _clientID in Const.clientIDs:
                _topic = Const.root_topic_HASH + _clientID
                clt.subscribe(_topic)
                print(f"Subscribed to topic: {_topic}")
                Const.listOfTopicToSubscribeTo.append(_topic)

        # Subscribe to the topic ALL and HASH
        elif toWhichTopicSubscribe == Const.SUBSCRIBE_TO_BOTH_TOPICS:
            for _clientID in Const.clientIDs:
                _topic_ALL = Const.root_topic_HASH + _clientID
                _topic_HASH = Const.root_topic_HASH + _clientID
                clt.subscribe(_topic_ALL)
                clt.subscribe(_topic_HASH)
                print(f"Subscribed to topic: {_topic_ALL}")
                print(f"Subscribed to topic: {_topic_HASH}")
                Const.listOfTopicToSubscribeTo.append(_topic_ALL)
                Const.listOfTopicToSubscribeTo.append(_topic_HASH)
        else:
            print("Error! Check the subscribe codes!")
            exit(0)
        clt.on_message = on_message

    def unsubscribe(self, clt):
        clt.unsubscribe(Const.topic_ALL)
        clt.unsubscribe(Const.topic_HASH)
