from Constants import Const

from tkinter import *
from tkinter import font as tkFont
from tkinter import filedialog
from tkinter import messagebox

from GUI.OfflineProcessingGUI import OfflineProcessingGUI
from GUI.DSPvsLJ import DSPvsLJ


class MainGUI:

    callback = None

    root = None

    chosenDir = None
    fileName = None

    saveOnDataFile = False
    doThePlots = False

    cb_x_axis_4_nodes = None
    x_axis = None

    cb_y_axis_4_nodes = None
    y_axis = None

    cb_z_axis_4_nodes = None
    z_axis = None

    cb_allTopic = None
    cb_hashTopic = None
    cb_saveOnFile = None
    cb_doPlot = None

    bttSaveOnFile = None
    fileInput = None
    dirLabel = None

    led = None
    #############
    # Plot data #
    #############
    maxSamples2Plot = None
    maxSamples2Plot_label = None
    # Time

    # Spectrum
    fs = None
    fs_label = None

    win = None
    win_label = None

    ovrlPerc = None
    ovrlPerc_label = None

    def __init__(self):
        self.cb_x_axis_4_nodes = []
        self.x_axis = []

        self.cb_y_axis_4_nodes = []
        self.y_axis = []

        self.cb_z_axis_4_nodes = []
        self.z_axis = []
        return None

    def setCallback(self, callback):
        self.callback = callback

    def onTopicSelection(self):
        print(f"allTopic: {self.cb_allTopic}")
        print(f"HashTopic: {self.cb_hashTopic}")

    def onSaveOnFile(self):
        print("onSaveOnFile():")
        if self.cb_saveOnFile.get() == 0:
            self.bttSaveOnFile['state'] = DISABLED
            self.dirLabel['state'] = DISABLED
            self.fileInput.grid_remove()
        if self.cb_saveOnFile.get() == 1:
            self.bttSaveOnFile['state'] = NORMAL
            self.dirLabel['state'] = NORMAL
            self.fileInput.grid()

    def onDoPlot(self):
        print("onDoPlot():")
        if self.cb_doPlot.get() == 0:
            self.maxSamples2Plot['state'] = DISABLED
            self.maxSamples2Plot_label['state'] = DISABLED

            self.fs['state'] = DISABLED
            self.fs_label['state'] = DISABLED

            self.win['state'] = DISABLED
            self.win_label['state'] = DISABLED

            self.ovrlPerc['state'] = DISABLED
            self.ovrlPerc_label['state'] = DISABLED

            for _i in range(0, len(self.cb_x_axis_4_nodes)):
                self.x_axis[_i]['state'] = DISABLED
                self.y_axis[_i]['state'] = DISABLED
                self.z_axis[_i]['state'] = DISABLED

        if self.cb_doPlot.get() == 1:
            self.maxSamples2Plot['state'] = NORMAL
            self.maxSamples2Plot_label['state'] = NORMAL

            self.fs['state'] = NORMAL
            self.fs_label['state'] = NORMAL

            self.win['state'] = NORMAL
            self.win_label['state'] = NORMAL

            self.ovrlPerc['state'] = NORMAL
            self.ovrlPerc_label['state'] = NORMAL

            for _i in range(0, len(self.cb_x_axis_4_nodes)):
                self.x_axis[_i]['state'] = NORMAL
                self.y_axis[_i]['state'] = NORMAL
                self.z_axis[_i]['state'] = NORMAL

    def onOfflineProcessing(self, whichDevice):
        offlineProcessing = OfflineProcessingGUI(whichDevice=whichDevice)
        offlineProcessing.run(master=self.root)

    # def onDSPvsLJ(self):
    #    dsp_vs_lj = DSPvsLJ()
    #    dsp_vs_lj.run(master=self.root)

    def onStart(self):
        print("onStart():")

        # Check if at least on topic has been selected
        if self.cb_allTopic.get() == 0 and self.cb_hashTopic.get() == 0:
            messagebox.showerror('Subscribing error', 'Error: at least on topics must be subscribed!')
            return
        else:
            if self.cb_allTopic.get() == 1 and self.cb_hashTopic.get() == 0:
                subscribeTo = Const.SUBSCRIBE_TO_TOPIC_ALL
            elif self.cb_allTopic.get() == 0 and self.cb_hashTopic.get() == 1:
                subscribeTo = Const.SUBSCRIBE_TO_TOPIC_HASH
            elif self.cb_allTopic.get() == 1 and self.cb_hashTopic.get() == 1:
                subscribeTo = Const.SUBSCRIBE_TO_BOTH_TOPICS

        # If 'saveOnFile' is selected, check that path and fileName have been set
        if self.cb_saveOnFile.get() == 1:
            self.saveOnDataFile = True
            self.fileName = str(self.fileInput.get())

            if self.chosenDir is None or self.fileName == '':
                messagebox.showerror('Directory and/or File name error',
                                     'Error: No directory and/or file name have been set!')
                return

        if self.cb_doPlot.get() == 1:
            self.doThePlots = True

            if int(self.maxSamples2Plot.get()) <= int(self.win.get()) * int(self.fs.get()):
                messagebox.showerror('Wrong parameters choice!',
                                     f'You have set:'
                                     f'\n - max #samples to plot = {int(self.maxSamples2Plot.get())}'
                                     f'\n - Sampling frequency = {int(self.fs.get())}'
                                     f'\n - Window size [s] = {int(self.win.get())}\n\n'
                                     f'However, in order to have enough samples to fill a window the condition:\n\n'
                                     f'max #samples to plot > Sampling frequency * Window size\n\n'
                                     f'MUST BE satisfied!'
                                     )
                return

            # Set plot data
            Const.MAX_SAMPLES_TO_VISUALIZE = int(self.maxSamples2Plot.get())

            Const.SAMPLING_RATE = int(self.fs.get())
            Const.WINDOW_LENGTH_IN_SEC = int(self.win.get())
            Const.OVERLAP_PERCENTAGE = int(self.ovrlPerc.get())

        # cb_x_axis_4_nodes = None
        # cb_y_axis_4_nodes = None
        # cb_z_axis_4_nodes = None

        # For example, if x,y,z checkboxes have been checked both for nodes 1 and 6 then:
        #   - figure_axis = [['X_AXIS', 'Y_AXIS'], ['X_AXIS', 'Y_AXIS', 'Z_AXIS'], ['Y_AXIS']]
        #   - which_Nodes = [0, 5]
        figure_axis = []
        which_Nodes = []
        for i in range(0, len(self.cb_x_axis_4_nodes)):
            _singleNode = []
            if self.cb_x_axis_4_nodes[i].get() == 1:
                _singleNode.append(Const.X_AXIS)
            if self.cb_y_axis_4_nodes[i].get() == 1:
                _singleNode.append(Const.Y_AXIS)
            if self.cb_z_axis_4_nodes[i].get() == 1:
                _singleNode.append(Const.Z_AXIS)

            if len(_singleNode) > 0:
                figure_axis.append(_singleNode)
                which_Nodes.append(i)

        self.callback(subscribeTo, self.doThePlots, which_Nodes, figure_axis)
        return

    def onChoosePath(self):
        print("onChoosePath():")
        self.chosenDir = filedialog.askdirectory(title="Select directory")
        print(f"Chosen dir: {self.chosenDir}")
        # Show the last 40 chars only
        self.dirLabel['text'] = f'Dir: ...{self.chosenDir[-40:]}'

    def setDataLedStatus(self, status):

        if not status:
            self.led['font'] = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
            self.led['text'] = "Data N/A"
            self.led['bg'] = "red"
            # print("label red")
        else:
            self.led['font'] = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
            self.led['text'] = "Data OK"
            self.led['bg'] = "green"
            # print("label green")

    # defaultTrue is use to set which node and which axis should be checked as default
    # defaultTrue = [[0, 1], [['X_AXIS', 'Y_AXIS', 'Z_AXIS'], ['Y_AXIS', 'Z_AXIS']]]
    #    - The nodes 0 and 1 should have the x,y and z axis ticks as default, respectively
    def createNodesFrames(self, startRow, startCol, defaultTrue):

        nNodes = len(Const.clientIDs)

        # Create 4 frames per each row
        # How many rows ?
        _nNodesPerRow = 4
        nRows = (nNodes // _nNodesPerRow) + 1

        _idx = 0
        for _row in range(0, nRows):
            _nNodesThisRow = _nNodesPerRow
            if (_row+1) * 4 > nNodes:
                _nNodesThisRow = nNodes - (_row * _nNodesPerRow)
            for _cols in range(0, _nNodesThisRow):
                # Choose what to plot for each node
                nodesFrame = Frame(self.root, padx=2, pady=2)
                nodesFrame.grid(row=startRow + _row, column=startCol + _cols, sticky="ew")
                checkGroup = LabelFrame(nodesFrame, text=f"Node {Const.clientIDs[_idx]}", padx=10, pady=10)

                self.cb_x_axis_4_nodes.append(IntVar())
                self.x_axis.append(Checkbutton(checkGroup, variable=self.cb_x_axis_4_nodes[-1], text="X"))
                self.x_axis[-1].pack()
                # Check if this must be ticked as default
                if (_idx in defaultTrue[0]) and (Const.X_AXIS in defaultTrue[1][_idx]):
                    self.cb_x_axis_4_nodes[-1].set(1)

                self.cb_y_axis_4_nodes.append(IntVar())
                self.y_axis.append(Checkbutton(checkGroup, variable=self.cb_y_axis_4_nodes[-1], text="Y"))
                self.y_axis[-1].pack()
                # Check if this must be ticked as default
                if (_idx in defaultTrue[0]) and (Const.Y_AXIS in defaultTrue[1][_idx]):
                    self.cb_y_axis_4_nodes[-1].set(1)

                self.cb_z_axis_4_nodes.append(IntVar())
                self.z_axis.append(Checkbutton(checkGroup, variable=self.cb_z_axis_4_nodes[-1], text="Z"))
                self.z_axis[-1].pack()
                # Check if this must be ticked as default
                if (_idx in defaultTrue[0]) and (Const.Z_AXIS in defaultTrue[1][_idx]):
                    self.cb_z_axis_4_nodes[-1].set(1)

                checkGroup.pack()
                _idx += 1

    def run(self):
        self.root = Tk()
        self.root.title('5GSMARTG - Subscriber')
        self.root.geometry('1500x650')

        self.cb_allTopic = IntVar()
        self.cb_hashTopic = IntVar()
        self.cb_saveOnFile = IntVar()
        self.cb_doPlot = IntVar()

        frame1 = Frame(self.root, padx=5, pady=5, bg="#006699")
        frame1.grid(row=0, column=1, columnspan=4)

        Label(frame1, text="5GSMARTG Subscriber", width=35, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)).pack()

        # Topics to subscribe
        Label(self.root, text="Topics to subscribe", width=35, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)).grid(row=1, column=0)
        Checkbutton(self.root, text='ALL', variable=self.cb_allTopic, onvalue=1, offvalue=0, command=self.onTopicSelection).grid(row=1, column=1)
        self.cb_allTopic.set(1)  # Set it as DEFAULT choice
        Checkbutton(self.root, text='HASH', variable=self.cb_hashTopic, onvalue=1, offvalue=0, command=self.onTopicSelection).grid(row=1, column=2)

        # Available clients (nodes)
        nodeIDs = ""
        for _id in Const.clientIDs:
            nodeIDs += _id + ", "
        nodeIDs = nodeIDs[:-2]
        _maxLength = 20
        if len(nodeIDs) > _maxLength:
            nodeIDs = nodeIDs[0:_maxLength-3] + "..."

        lbl = Label(self.root, text=f"Available Node IDs: {nodeIDs}", width=35, borderwidth=5,
                  font=tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD))
        lbl.grid(row=1, column=3)

        self.led = Label()
        self.led.grid(row=1, column=4)

        # Save on file
        Label(self.root, text="Save data", width=35, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)).grid(row=2, column=0)
        Checkbutton(self.root, text='Save on file', variable=self.cb_saveOnFile, onvalue=1, offvalue=0, command=self.onSaveOnFile).grid(row=2, column=1)
        self.dirLabel = Label(self.root, text="Dir: None", width=50, borderwidth=5)
        self.dirLabel.grid(row=2, column=2)
        self.dirLabel['state'] = DISABLED

        self.bttSaveOnFile = Button(self.root, text='Choose path', command=self.onChoosePath)
        self.bttSaveOnFile.grid(row=3, column=2)
        self.bttSaveOnFile['state'] = DISABLED

        self.fileInput = Entry(self.root, textvariable="asd", width=15, borderwidth=5)
        self.fileInput.grid(row=4, column=2)
        self.fileInput.grid_remove()

        # Do plot
        Label(self.root, text="Plotting", width=35, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)).grid(row=6, column=0)
        Checkbutton(self.root, text='Do plot', variable=self.cb_doPlot, onvalue=1, offvalue=0, command=self.onDoPlot)\
            .grid(row=6, column=1, columnspan=2)
        self.cb_doPlot.set(1)  # Set it as DEFAULT choice

        timeFrame = Frame(self.root, padx=2, pady=2, bg="#006699")
        timeFrame.grid(row=8, column=1, rowspan=4, columnspan=2, sticky=W)

        Label(timeFrame, text="Time", width=35, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)).grid(row=7, column=1, columnspan=2)
        # Set sampling frequency
        self.maxSamples2Plot_label = Label(timeFrame, text="Max #samples to plot", width=35, borderwidth=5)
        self.maxSamples2Plot_label.grid(row=8, column=1)
        self.maxSamples2Plot = Entry(timeFrame, width=10, borderwidth=5)
        self.maxSamples2Plot.insert(END, str(Const.MAX_SAMPLES_TO_VISUALIZE))
        self.maxSamples2Plot.grid(row=8, column=2)

        spectrumFrame = Frame(self.root, padx=2, pady=2, bg="#006699")
        spectrumFrame.grid(row=8, column=3, rowspan=4, columnspan=2, sticky=W)

        Label(spectrumFrame, text="Spectrum", width=35, borderwidth=5,
              font=tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)).grid(row=7, column=3, columnspan=2)
        # Set sampling frequency
        self.fs_label = Label(spectrumFrame, text="Sampling frequency [Hz]", width=35, borderwidth=5)
        self.fs_label.grid(row=8, column=3)
        self.fs = Entry(spectrumFrame, width=10, borderwidth=5)
        self.fs.insert(END, str(Const.SAMPLING_RATE))
        self.fs.grid(row=8, column=4)

        # Set win size (spectrum analysis)
        self.win_label = Label(spectrumFrame, text="Window size [s]", width=35, borderwidth=5)
        self.win_label.grid(row=9, column=3)
        self.win = Entry(spectrumFrame, width=10, borderwidth=5)
        self.win.insert(END, str(Const.WINDOW_LENGTH_IN_SEC))
        self.win.grid(row=9, column=4)

        # Set overlap % (spectrum analysis)
        self.ovrlPerc_label = Label(spectrumFrame, text="Overlap %", width=35, borderwidth=5)
        self.ovrlPerc_label.grid(row=10, column=3)
        self.ovrlPerc = Entry(spectrumFrame, width=10, borderwidth=5)
        self.ovrlPerc.insert(END, str(Const.OVERLAP_PERCENTAGE))
        self.ovrlPerc.grid(row=10, column=4)

        # This allows to choose which node visualize and, for each fo them, which axis.
        # [[0], [['X_AXIS', 'Y_AXIS', 'Z_AXIS']]]
        # [[0, 1], [['X_AXIS', 'Y_AXIS', 'Z_AXIS'], ['Y_AXIS', 'Z_AXIS']]]
        self.createNodesFrames(startRow=12, startCol=1, defaultTrue=[[0], [['X_AXIS', 'Y_AXIS', 'Z_AXIS']]])

        # RUN button
        Button(self.root, text='Start', command=self.onStart, fg="white", bg='#336600',
               font=tkFont.Font(family='Helvetica', size=18, weight=tkFont.BOLD)).grid(row=20, column=2, columnspan=2)

        # OFFLINE PROCESSING buttons
        Button(self.root, text='Offline DSP processing', command=lambda: self.onOfflineProcessing(whichDevice=Const.NODE_DSP),
               fg="white", bg='#000080', font=tkFont.Font(family='Helvetica', size=14, weight=tkFont.BOLD)).grid(row=21, column=2, columnspan=2)
        Button(self.root, text='Offline LJ processing', command=lambda: self.onOfflineProcessing(whichDevice=Const.NODE_LABJACK),
               fg="white", bg='#ff5c33', font=tkFont.Font(family='Helvetica', size=14, weight=tkFont.BOLD)).grid(row=22, column=2, columnspan=2)
        # DSP vs LJ
        # Button(self.root, text='DSP vs LJ', command=self.onDSPvsLJ(),
        #       fg="white", bg='#008080', font=tkFont.Font(family='Helvetica', size=14, weight=tkFont.BOLD)).grid(row=23, column=2, columnspan=2)

        self.root.mainloop()



