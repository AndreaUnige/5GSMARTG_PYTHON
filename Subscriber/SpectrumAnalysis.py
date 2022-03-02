from Constants import Const
import scipy.signal
import numpy as np
import math
import sys


class SpectrumAnalysis:

    def __init__(self):
        return None

    def welchPowerSpectrum(self, accData, win, logarithmic, smoothing):
        # window può essere anche un array. In quel caso nperseg == len(array)
        # se window è string -> nperseg = 256
        # nOverlap di default è uguale a noverlap = nperseg // 2 (NOTA: // significa divisione intera)
        nOverlap = round(len(win) * Const.OVERLAP_PERCENTAGE / 100)
        f, psd = scipy.signal.welch(x=accData, fs=Const.SAMPLING_RATE, window=win, noverlap=nOverlap)

        '''
        # Compute overall power
        pwrFreq = 0
        for _psd in psd: pwrFreq += _psd
        # print(f"Overall power (freq): {pwrFreq} - Length: {len(psd)}")

        pwrTime = 0
        for _accData in accData: pwrTime += math.pow(_accData, 2)
        pwrTime /= (len(accData) / 2)  # because this is only half spectrum
        # print(f"Overall power (time): {} - Length: {len(accData)}")
        '''

        # Do a spectrum smoothing through a moving average
        if smoothing:
            psd = np.convolve(psd, np.ones(Const.RUNNING_AVERAGE_IN_SAMPLES) / Const.RUNNING_AVERAGE_IN_SAMPLES, mode='same')

        if logarithmic:
            for i in range(0, len(psd)):
                if psd[i] == 0:
                    psd[i] += np.finfo(np.float32).eps  # It should be 1.19209e-07
                psd[i] = 10 * math.log10(psd[i])

        return f, psd
        # return f, psd, pwrTime, pwrFreq



