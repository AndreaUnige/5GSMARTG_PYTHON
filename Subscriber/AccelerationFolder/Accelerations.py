from Constants import Const


# This class should handle the acceleration data related to a single Node
# See the variable 'nodeID'
class Accelerations:

    xDataAsVector = None
    yDataAsVector = None
    zDataAsVector = None

    # At the moment this is not used
    accDataAsMatrix = None

    nodeID = None

    def __init__(self, nodeId):
        self.xDataAsVector = []
        self.yDataAsVector = []
        self.zDataAsVector = []

        self.nodeID = nodeId

    def addDataAsVector(self, data, whichAxis):

        if not isinstance(data, list):
            if whichAxis == Const.X_AXIS:
                self.xDataAsVector.append(data)
            elif whichAxis == Const.Y_AXIS:
                self.yDataAsVector.append(data)
            elif whichAxis == Const.Z_AXIS:
                self.zDataAsVector.append(data)
            else:
                print("ERROR! Cannot add data as vector!")

        else:
            if whichAxis == Const.X_AXIS:
                self.xDataAsVector += data
            elif whichAxis == Const.Y_AXIS:
                self.yDataAsVector += data
            elif whichAxis == Const.Z_AXIS:
                self.zDataAsVector += data
            else:
                print("ERROR! Cannot add data as vector!")

    # Not used at the moment
    def addDataAsMatrix(self):
        return None

    def clearData(self):
        self.xDataAsVector = []
        self.yDataAsVector = []
        self.zDataAsVector = []