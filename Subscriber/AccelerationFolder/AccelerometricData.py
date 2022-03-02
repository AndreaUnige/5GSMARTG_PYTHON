from Constants import Const
from AccelerationFolder.Accelerations import Accelerations
from datetime import datetime
import time


class AccelerometricData:

    nodesAccelerations = None

    # At the moment this is not used
    samplingTimesAsVector = None

    # At the moment this is not used
    absoluteSampleTimeAsVector = None

    # At the moment this is not used
    accDataAsMatrix = None

    writeHeader = True

    def __init__(self):
        self.nodesAccelerations = []
        for _nodeId in Const.clientIDs:
            self.nodesAccelerations.append(Accelerations(nodeId=_nodeId))

        self.samplingTimesAsVector = []
        self.absoluteSampleTimeAsVector = []

        self.accDataAsMatrix = []

        self.writeHeader = True

    def doParse(self, msgAsString, idxNode):
        # msgAsString = "1234,1,2,3;1234,1,2,3;1234,1,2,3;"

        # Remove the final ';'
        if msgAsString[-1] == Const.SampleSeparator:
            msgAsString = msgAsString[:-1]

        samples = msgAsString.split(Const.SampleSeparator)

        '''
        # First sample should be the node absolute time
        nodeTS_nano = samples[0]
        samples.pop(0)  # Remove it
        '''
        for _singleSample in samples:
            # [_samplingTime, _x, _y, _z] = _singleSample.split(Const.SingleValuesSeparator)
            [_absoluteSampleTime, _x, _y, _z] = _singleSample.split(Const.SingleValuesSeparator)

            self.nodesAccelerations[idxNode].addDataAsVector(float(_x), Const.X_AXIS)
            self.nodesAccelerations[idxNode].addDataAsVector(float(_y), Const.Y_AXIS)
            self.nodesAccelerations[idxNode].addDataAsVector(float(_z), Const.Z_AXIS)

            # self.samplingTimesAsVector.append(float(_samplingTime))
            # self.absoluteSampleTimeAsVector.append(float(_absoluteSampleTime))

            # return nodeTS_nano, samples
        return samples

    def writeOnFile(self, path, fileName, clientID, topic, samples):
        f = open(f"{path}/{fileName}", "a")
        # ts_ns,topic,x,y,z

        # NOTA: Dentro 'samples' c'è anche il sampling time.
        # In pratica 'samples' è una quaterna di dati: samplingTime,x,y,z
        # 14 Feb 2022:
        # 'samples' è di nuovo una terna di dati: x,y,z
        # 17 Feb 2022:
        # 'samples' una terna quanterna di dati: absSampleTime,x,y,z

        [_absoluteSampleTime, _, _, _] = samples.split(Const.SingleValuesSeparator)
        if self.writeHeader:
            # f.write("Node_Time[ns],Subscriber_AbsTime,Subscriber_Time[ns],ClientID,Topic,SamplingTime[us],X,Y,Z\n")
            f.write("Node_AbsTime[us],Subscriber_AbsTime,Subscriber_Time[ns],ClientID,Topic,X,Y,Z\n")
            self.writeHeader = False
        f.write(f"{_absoluteSampleTime},{datetime.now()},{time.time_ns()},{clientID},{topic},{samples}\n")
