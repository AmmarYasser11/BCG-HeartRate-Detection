import numpy as np

from detect_peaks import detect_peaks


def compute_rate(beats, mpd):

    peaks = detect_peaks(beats, mpd=mpd)

    if len(peaks) > 1:
        fs = 50
        diff_sample = peaks[-1] - peaks[0] + 1
        t_N = diff_sample / fs
        heartRate = (len(peaks) - 1) / t_N * 60
        return heartRate
    else:
        return 0.0, 0.0
