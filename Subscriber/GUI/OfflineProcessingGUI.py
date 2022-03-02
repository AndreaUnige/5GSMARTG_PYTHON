import math

from Constants import Const

from tkinter import *
from tkinter import font as tkFont
from tkinter import filedialog
from tkinter import messagebox
from PlotData import PlotData
from AccelerationFolder.AccelerometricData import AccelerometricData


class OfflineProcessingGUI:

    root = None
    plotData = None

    nodeId = None
    fromTime = None
    toTime = None

    fs = None
    win = None
    ovrlPerc = None
    choosenFile_label = None

    bttChooseFile = None
    fileChoosen = None

    whichDevice = None

    def __init__(self, whichDevice):
        self.whichDevice = whichDevice
        self.plotData = PlotData()

    def onFileChosen(self):
        self.fileChoosen = filedialog.askopenfilename(title="Select file")
        # Show the last 40 chars only
        self.choosenFile_label['text'] = f'File: ...{self.fileChoosen[-40:]}'

    def readLJfile(self):
        f = open(self.fileChoosen, "r")

        node_time_s = []

        xData = []
        yData = []
        zData = []

        for i in range(0, 9):
            f.readline()  # This to discard the first 9 lines. It is the header

        for _singleLine in f:
            _singleLine = _singleLine.replace("", "")  # Remove any blank spaces
            _time, _x, _y, _z, _, _, _ = _singleLine.split("\t")

            node_time_s.append(float(_time))
            xData.append(float(_x))
            yData.append(float(_y))
            zData.append(float(_z))

        return node_time_s, xData, yData, zData

    def readDSPfile(self, fromTime_ns, toTime_ns, nodeID):
        f = open(self.fileChoosen, "r")

        node_time_ns = []
        subscriber_abs_time = []
        subscriber_time_ns = []
        clientID = []
        topic = []

        xData = []
        yData = []
        zData = []

        f.readline()  # This to discard the first line. It is the header
        for _singleLine in f:
            _singleLine = _singleLine.replace(" ", "")  # Remove any blank spaces
            _node_time_ns, _abs_time, _time_ns, _nodeID, _topic, _x, _y, _z = _singleLine.split(",")

            # Skip it if the nodeID is not the same
            if _nodeID != nodeID:
                continue

            # Skip it if the is not in the specified period of time
            if not (fromTime_ns == -1 or _time_ns > fromTime_ns) and (toTime_ns == -1 or _time_ns < toTime_ns):
                continue

            node_time_ns.append(str(_node_time_ns))
            subscriber_abs_time.append(str(_abs_time))
            subscriber_time_ns.append(int(_time_ns))
            clientID.append(_nodeID)
            topic.append(_topic)

            xData.append(float(_x))
            yData.append(float(_y))
            zData.append(float(_z))

        return node_time_ns, subscriber_abs_time, subscriber_time_ns, clientID, topic, xData, yData, zData

    def onDoPlot(self):
        if self.fileChoosen is None or self.fileChoosen == '':
            messagebox.showerror('No file choosen!',
                                 'Error: No file has been selected!')
            return

        if self.nodeId is None or str(self.nodeId.get()) == '':
            messagebox.showerror('Empty NodeID',
                                 'Error: No nodeID has been chosen!')
            return

        Const.SAMPLING_RATE = int(self.fs.get())
        Const.WINDOW_LENGTH_IN_SEC = int(self.win.get())
        Const.OVERLAP_PERCENTAGE = int(self.ovrlPerc.get())

        # Extract the clientID
        nodeId = str(self.nodeId.get())

        # Compute times
        fromTime_ns = -1
        if str(self.fromTime.get()) != '-1':
            hh_from, mm_from, ss_from, mm_from = str(self.fromTime.get()).split(":")
            fromTime_ns = int(hh_from) * 3600 * math.pow(10, 9) +\
                          int(mm_from) * 60 * math.pow(10, 9) +\
                          int(ss_from) * math.pow(10, 9) + \
                          int(mm_from) * math.pow(10, 6)

        toTime_ns = -1
        if str(self.toTime.get()) != '-1':
            hh_to, mm_to, ss_to, mm_to = str(self.toTime.get()).split(":")
            toTime_ns = int(hh_to) * 3600 * math.pow(10, 9) + \
                          int(mm_to) * 60 * math.pow(10, 9) + \
                          int(ss_to) * math.pow(10, 9) + \
                          int(mm_to) * math.pow(10, 6)

        # Read data from the selected file
        if self.whichDevice == Const.NODE_DSP:
            node_time_ns, abs_time, time_ns, clientID, topic, xData, yData, zData = \
                self.readDSPfile(fromTime_ns=fromTime_ns, toTime_ns=toTime_ns, nodeID=nodeId)

        if self.whichDevice == Const.NODE_LABJACK:
            node_time_s, xData, yData, zData = self.readLJfile()

        figure_axis = [[Const.X_AXIS, Const.Y_AXIS, Const.Z_AXIS]]
        self.plotData.preparePlot(title=self.fileChoosen, figure_axis=figure_axis)

        accelerometricDataFromFile = AccelerometricData()
        accelerometricDataFromFile.addDataAsVector(data=xData, whichAxis=Const.X_AXIS)
        accelerometricDataFromFile.addDataAsVector(data=yData, whichAxis=Const.Y_AXIS)
        accelerometricDataFromFile.addDataAsVector(data=zData, whichAxis=Const.Z_AXIS)

        self.plotData.doPlot(idx=Const.clientIDs.index(nodeId), accelerometricData=accelerometricDataFromFile)

        return None

    def run(self, master):

        self.root = Toplevel(master)
        self.root.title(f"Offline processing - {self.whichDevice}")
        self.root.geometry('600x450')

        # LABEL
        lbl = Frame(self.root, padx=5, pady=5, bg="#2a2a2a")
        lbl.grid(row=0, column=1)
        Label(lbl, text=f"{self.whichDevice}", width=15, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)).pack()

        # BUTTON choose file
        self.bttChooseFile = Button(self.root, text='Choose file', command=self.onFileChosen)
        self.bttChooseFile.grid(row=1, column=0, padx=10, pady=20)
        self.choosenFile_label = Label(self.root, text="", width=60, borderwidth=5)
        self.choosenFile_label.grid(row=1, column=1)

        # Node ID
        nodeIdFrame = Frame(self.root, bd=3, padx=2, pady=2, bg="#454545")
        nodeIdFrame.grid(row=2, column=0, rowspan=1, columnspan=2, pady=10)
        Label(nodeIdFrame, text="Node ID", width=35, borderwidth=5).grid(row=2, column=0)
        self.nodeId = Entry(nodeIdFrame, width=10, borderwidth=5)
        self.nodeId.grid(row=2, column=1)

        timeFrame = Frame(self.root, bd=3, padx=2, pady=2, bg="#454545")
        timeFrame.grid(row=3, column=0, rowspan=2, columnspan=2, pady=10)

        # FROM
        Label(timeFrame, text="From (hh:mm:ss:mmmm)", width=35, borderwidth=5).grid(row=3, column=0)
        self.fromTime = Entry(timeFrame, width=10, borderwidth=5)
        self.fromTime.insert(END, -1)
        self.fromTime.grid(row=3, column=1)

        # TO
        Label(timeFrame, text="To (hh:mm:ss:mmmm)", width=35, borderwidth=5).grid(row=4, column=0)
        self.toTime = Entry(timeFrame, width=10, borderwidth=5)
        self.toTime.insert(END, -1)
        self.toTime.grid(row=4, column=1)

        plotFrame = Frame(self.root, bd=3, padx=2, pady=2, bg="#454545")
        plotFrame.grid(row=5, column=0, rowspan=3, columnspan=2, pady=10)

        # SAMPLING FREQUENCY
        fs_label = Label(plotFrame, text="Sampling frequency [Hz]", width=35, borderwidth=5)
        fs_label.grid(row=5, column=0)
        self.fs = Entry(plotFrame, width=10, borderwidth=5)
        self.fs.insert(END, str(Const.SAMPLING_RATE))
        self.fs.grid(row=5, column=1)

        # WIN size
        win_label = Label(plotFrame, text="Window size [s]", width=35, borderwidth=5)
        win_label.grid(row=6, column=0)
        self.win = Entry(plotFrame, width=10, borderwidth=5)
        self.win.insert(END, str(Const.WINDOW_LENGTH_IN_SEC))
        self.win.grid(row=6, column=1)

        # Set overlap % (spectrum analysis)
        ovrlPerc_label = Label(plotFrame, text="Overlap %", width=35, borderwidth=5)
        ovrlPerc_label.grid(row=7, column=0)
        self.ovrlPerc = Entry(plotFrame, width=10, borderwidth=5)
        self.ovrlPerc.insert(END, str(Const.OVERLAP_PERCENTAGE))
        self.ovrlPerc.grid(row=7, column=1)

        # DO-PLOT button
        Button(self.root, text='Plot', command=self.onDoPlot, fg="white", bg='#336600',
               font=tkFont.Font(family='Helvetica', size=14, weight=tkFont.BOLD)).grid(row=8, column=0, columnspan=2)

        self.root.mainloop()


