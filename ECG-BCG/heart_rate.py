import numpy as np
from compute_rate import compute_rate
import heartpy

def heart_rate(t1, t2, win_size, window_limit, sig, mpd, sig_type="bcg", plot=0):

    all_rate = []
    for j in range(0, window_limit):
        sub_signal = sig[t1:t2]
        if sig_type == "ecg":
            w, results = heartpy.process(sub_signal, 50)
            rate = results['bpm']
        else:
            rate = compute_rate(sub_signal, mpd)
        all_rate.append(rate)

        t1 = t2
        t2 += win_size

    all_rate = np.vstack(all_rate).flatten()
    return all_rate