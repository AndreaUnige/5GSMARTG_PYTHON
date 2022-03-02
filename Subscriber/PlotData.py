import time
import matplotlib.pyplot as plt
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from datetime import datetime
from Constants import Const
from SpectrumAnalysis import SpectrumAnalysis
import numpy as np
from tkinter import *


class PlotData:
    singleNode_figureAxis = None

    whichNodesToPlot = None

    def __init__(self):
        self.whichNodesToPlot = []
        return None

    # This must open a different figure, one for each node selected
    # Every figure will have different plots, depending on which axis have been selected
    # figure_axis contains which axis do I have to plot for each node
    # For example
    #   - figure_axis = [['X_AXIS','Y_AXIS'],['X_AXIS', 'Y_AXIS','Z_AXIS'],['Y_AXIS']]
    #   - whichNodes = [1, 2, 4]
    # three plots must be opened. In the first x,y axis of node1 must be plotted,
    # in the second x,y,z of node2 and the third only y axis for the node4
    def preparePlot(self, title, whichNodes, figure_axis):
        print("Preparing plot")

        # nFigures = len(figure_axis)
        self.singleNode_figureAxis = []
        for i in range(0, len(figure_axis)):
            _singleFigure = figure_axis[i]
            nAxis = len(_singleFigure)
            _figure, _ax = plt.subplots(2, nAxis, sharex=False, facecolor='#DEDEDE', figsize=(20, 15))
            _figure.suptitle(f"Node: {Const.clientIDs[whichNodes[i]]}", fontsize=18, fontweight="bold")
            # _figure.suptitle(f"Node: {Const.clientIDs[whichNodes[i]]} - {title[-50:]}", fontsize=18, fontweight="bold")
            self.whichNodesToPlot.append(Const.clientIDs[whichNodes[i]])

            self.singleNode_figureAxis.append([_figure, _ax, _singleFigure])
            plt.pause(Const.PLOT_PAUSE_SEC)


        '''
        if fullScreen:
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
            plt.pause(Const.PLOT_PAUSE_SEC)
        '''

    def doPlot(self, idx, accelerometricData):
        if len(accelerometricData.xDataAsVector) > 0 and len(accelerometricData.yDataAsVector) > 0 and len(accelerometricData.zDataAsVector) > 0:
            considerDataFromThisNode = True
            idxNode = -1
            try:
                idxNode = self.whichNodesToPlot.index(idx)
            except ValueError:
                considerDataFromThisNode = False
                print(f"Received data from Node {idx} but data from such a node should not be plotted nor saved!\n"
                      f"(The checkbox for node {idx} has not been checked\n"
                      "Ignore data!")

            if considerDataFromThisNode:
                # Clear all the old plots
                self.__clearPlots(idx)

                '''
                # Get the last Const.MAX_SAMPLES_TO_VISUALIZE elements
                accX = accelerometricData.xDataAsVector[-Const.MAX_SAMPLES_TO_VISUALIZE:]
                accY = accelerometricData.yDataAsVector[-Const.MAX_SAMPLES_TO_VISUALIZE:]
                accZ = accelerometricData.zDataAsVector[-Const.MAX_SAMPLES_TO_VISUALIZE:]
                '''
                accX = accelerometricData.xDataAsVector
                accY = accelerometricData.yDataAsVector
                accZ = accelerometricData.zDataAsVector

                # Do single time plots
                _ax = self.singleNode_figureAxis[idxNode][1]
                whichAx = self.singleNode_figureAxis[idxNode][2]
                nAxis = len(whichAx)

                # This are the index of the axis.
                # If there is only one axis, then they must be 1D (just a number) otherwise 2D (vector)
                timeIdxAxis = 0
                freqIdxAxis = 1

                for i in range(0, nAxis):
                    if nAxis > 1:
                        # If more than two axis must be plot, this should be bi-dimentional
                        timeIdxAxis = (0, i)
                        freqIdxAxis = (1, i)

                    if whichAx[i] == Const.X_AXIS:
                        self.__singleTimePlot(axis=_ax[timeIdxAxis], accData=accX, xLabel='Samples', yLabel='AccData',
                                              title='X', markers=True)
                        self.__singleSpectrumPlot(axis=_ax[freqIdxAxis], accData=accX, xLabel='Hz',
                                                  yLabel='PSD [DB/Hz]', title='', markers=True)

                    elif whichAx[i] == Const.Y_AXIS:
                        self.__singleTimePlot(axis=_ax[timeIdxAxis], accData=accY, xLabel='Samples', yLabel='',
                                              title='Y', markers=True)
                        self.__singleSpectrumPlot(axis=_ax[freqIdxAxis], accData=accY, xLabel='Hz',
                                                  yLabel='', title='', markers=True)

                    elif whichAx[i] == Const.Z_AXIS:
                        self.__singleTimePlot(axis=_ax[timeIdxAxis], accData=accZ, xLabel='Samples', yLabel='',
                                              title='Z', markers=True)
                        self.__singleSpectrumPlot(axis=_ax[freqIdxAxis], accData=accZ, xLabel='Hz',
                                                  yLabel='', title='', markers=True)

                self.__updatePlot(idxNode)

        else:
            print("No data available for plotting!")

    def __singleTimePlot(self, axis, accData, xLabel, yLabel, title, markers):
        if markers:
            axis.plot(np.arange(len(accData)), accData, '-p', markersize=2, linewidth=2, markerfacecolor='white',
                      markeredgecolor='gray', markeredgewidth=2)
        else:
            axis.plot(np.arange(len(accData)), accData, '-p')

        axis.grid(True)

        # Controllare !
        # axis.set_xlim(0, len(accData))
        axis.set_ylim(bottom=0, top=5000)  # Fixed limits

        axis.set_title(title, fontsize=18, fontweight="bold")
        axis.set_xlabel(xLabel, fontsize=16, fontweight="bold")
        axis.set_ylabel(yLabel, fontsize=16, fontweight="bold")
        axis.tick_params(labelsize=14)

    def __singleSpectrumPlot(self, axis, accData, xLabel, yLabel, title, markers):

        # Estimate the PSD
        spectrumAnalyzer = SpectrumAnalysis()
        win = np.hamming(Const.SAMPLING_RATE * Const.WINDOW_LENGTH_IN_SEC)

        if len(accData) > len(win):
            # Compute the power spectral density (V ** 2 / Hz)
            f, psd = spectrumAnalyzer.welchPowerSpectrum(accData=accData, win=win, logarithmic=True,
                                                                           smoothing=False)

            if markers:
                axis.plot(f, psd, '-p', markersize=2, linewidth=2, markerfacecolor='white',
                          markeredgecolor='gray', markeredgewidth=2)
            else:
                axis.plot(f, psd, '-p')

            axis.grid(True)
            axis.set_xlim(0, 50)
            # axis.set_title(f"{title} - Pwr: {round(pwrFreq * 100) / 100} [W]", fontsize=18, fontweight="bold")
            axis.set_xlabel(xLabel, fontsize=16, fontweight="bold")
            axis.set_ylabel(yLabel, fontsize=16, fontweight="bold")
            axis.tick_params(labelsize=14)
            # axis.set_title("ArgMax: " + str('%.2f' % f[xPSD.argmax()]) + " [Hz]", fontdict={'fontsize': 26, 'fontweight': 'bold'})
        else:
            # Not enough samples
            # Write this only in the middle plot.
            axis.text(0.1, 0.7, 'Not enough samples to fill the windows to estimate PSD', fontsize=8,
                      bbox=dict(facecolor='red', alpha=0.5))
            axis.text(0.25, 0.5, f'AccSamples: {len(accData)} out of {len(win)}', fontsize=8,
                      bbox=dict(facecolor='red', alpha=0.5))

    def __clearPlots(self, idx):

        idxNode = self.whichNodesToPlot.index(idx)

        _ax = self.singleNode_figureAxis[idxNode][1]
        nAxis = len(self.singleNode_figureAxis[idxNode][2])
        for i in range(0, nAxis):
            if nAxis > 1:
                _ax[0, i].cla()  # Clear time plots
                _ax[1, i].cla()  # Clear freq plots
            else:
                _ax[0].cla()  # Clear time plots
                _ax[1].cla()  # Clear freq plots

    def __updatePlot(self, idxNode):
        self.singleNode_figureAxis[idxNode][0].tight_layout()  # set the spacing between subplots
        self.singleNode_figureAxis[idxNode][0].canvas.draw()
        self.singleNode_figureAxis[idxNode][0].canvas.flush_events()
