from PlotData import PlotData
from AccelerationFolder.AccelerometricData import AccelerometricData
from Constants import Const
from MQTT import MQTT
from GUI.MainGUI import MainGUI
from ConfigFile import ConfigFile


class Engine:

    myGUI = None

    mqtt = None
    accelerometricData = None
    plotData = None

    mqttClient = None

    def __init__(self):

        configFile = ConfigFile()
        configFile.readConfigFile()

        self.mqtt = MQTT()
        self.accelerometricData = AccelerometricData()
        self.plotData = PlotData()

        self.mqttClient = self.mqtt.connect_mqtt(cltID=Const.subscriberID, usrName=Const.username,
                                                 psswrd=Const.password, brk=Const.broker)

    def runGUI(self):
        self.myGUI = MainGUI()
        self.myGUI.setCallback(callback=self.onGUIdone)
        self.myGUI.run()

    # Example: figure_axis = [['X_AXIS', 'Y_AXIS'], ['X_AXIS', 'Y_AXIS', 'Z_AXIS'], ['Y_AXIS']]
    def onGUIdone(self, subscribeTo, doThePlots, whichNodes, figure_axis):
        # self.myGUI.root.destroy()

        if doThePlots:
            self.plotData.preparePlot(title="", whichNodes=whichNodes, figure_axis=figure_axis)

        # Specify here the callback
        self.mqtt.subscribe(self.mqttClient, toWhichTopicSubscribe=subscribeTo, callback=self.onDataReceived)
        self.mqttClient.loop_forever()

    def onDataReceived(self, topic, data):
        self.myGUI.setDataLedStatus(status=True)

        print(f"Topic: {topic} - Data: {data}")
        # data = "12345;" + data

        # Extract the clientID
        _id = topic[topic.rindex("/")+1:]

        idxNode = Const.clientIDs.index(_id)
        dataSplitted = data.split(Const.SampleSeparator)
        if len(dataSplitted) >= 2:  # At least TS and 1 acc samples
            if len(dataSplitted[0]) > 0 and len(dataSplitted[1]) > 0:
                # nodeTS, receivedSamples = self.accelerometricData.doParse(msgAsString=data)
                receivedSamples = self.accelerometricData.doParse(msgAsString=data, idxNode=idxNode)

                # Handle the plotting
                if self.myGUI.doThePlots:

                    # Get the last Const.MAX_SAMPLES_TO_VISUALIZE elements
                    lastAccData = AccelerometricData()
                    lastAccData.xDataAsVector = self.accelerometricData.nodesAccelerations[idxNode].xDataAsVector[-Const.MAX_SAMPLES_TO_VISUALIZE:]
                    lastAccData.yDataAsVector = self.accelerometricData.nodesAccelerations[idxNode].yDataAsVector[-Const.MAX_SAMPLES_TO_VISUALIZE:]
                    lastAccData.zDataAsVector = self.accelerometricData.nodesAccelerations[idxNode].zDataAsVector[-Const.MAX_SAMPLES_TO_VISUALIZE:]
                    self.plotData.doPlot(idx=_id, accelerometricData=lastAccData)

                # Handle the file saving
                if self.myGUI.saveOnDataFile:
                    for _sample in receivedSamples:
                        self.accelerometricData.writeOnFile(path=self.myGUI.chosenDir, fileName=self.myGUI.fileName,
                                                            clientID=_id, topic=topic, samples=_sample)
            else:
                print("Discard packet!! - Not enough data")
        else:
            print("Discard packet!! - Packet void!")


if __name__ == '__main__':
    # ## --- MAIN --- ## #
    engine = Engine()
    engine.runGUI()




