from Constants import Const


class ConfigFile:
    mqttClient = None
    broker = None
    #  THESE ARE TAKEN FROM THE CONFIG FILES
    root_topic_ALL = None
    root_topic_HASH = None
    username = None
    password = None
    clientIDs = None
    #  THESE ARE GENERATED AND FORMATTED:
    #   - root_topic_ALL + clientID
    #   - root_topic_HASH + clientID
    topic_ALL = None
    topic_HASH = None

    def __init__(self):
        return None

    def readConfigFile(self):
        f = open("clients.txt", "r")
        for _singleLine in f:
            if _singleLine[0] == '#':  # Commented line
                continue

            _singleLine = _singleLine.replace(" ", "")  # Remove any blank spaces
            _field = _singleLine[:_singleLine.index('=')]
            _value = _singleLine[_singleLine.index('=') + 1:].rstrip("\r\n")

            if _field == 'broker':
                self.broker = _value
                Const.broker = self.broker
            elif _field == 'root_topic_ALL':
                self.root_topic_ALL = _value
                Const.root_topic_ALL = self.root_topic_ALL
            elif _field == 'root_topic_HASH':
                self.root_topic_HASH = _value
                Const.root_topic_HASH = self.root_topic_HASH
            elif _field == 'username':
                self.username = _value
                Const.username = self.username
            elif _field == 'password':
                self.password = _value
                Const.password = self.password
            elif _field == 'clientIDs':
                self.clientIDs = _value.split(",")
                Const.clientIDs = self.clientIDs
            else:
                print("Error in the configuration file 'clients.txt'")
                print("Check the fields names!!")
                exit(0)
