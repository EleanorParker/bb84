import numpy as np
import math
import argparse
import matplotlib.pyplot as plt
from scipy.stats import norm


'''
def dark_counts(data, bin_width):
    # Number of counts in each detector
    counts1 = 0
    counts2 = 0
    counts3 = 0
    counts4 = 0
    # Amount of time for 1 bin in nanoseconds
    clock_period = (81 / 10**6) * bin_width
    N = len(data)
    # Converting from bins to time (in seconds)
    tot_time = (data[N-1][0] - data[0][0]) * clock_period * 10**-9
    for (time, channel) in data:
        if channel == 1.0:
            counts1 += 1
        if channel == 2.0:
            counts2 += 1
        if channel == 3.0:
            counts3 += 1
        if channel == 4.0:
            counts4 += 1
    rate1 = counts1 / tot_time
    rate2 = counts2 / tot_time
    rate3 = counts3 / tot_time
    rate4 = counts4 / tot_time
    return rate1, rate2, rate3, rate4
'''

def jitter_and_delay(data, detector):
    '''
    Takes in a list of tuples (time, channel) and the desired detector that you
    want the jitter time of. Plots and outputs the optimal coincidence window,
    the jitter time and the delay time.
    '''
    delay = []
    trigger = 8
    for i, (time, channel) in enumerate(data):
        if channel == trigger and i<len(data):
            j = 1
            # Removing dark counts from other detectors
            while i+j<len(data) and data[i+j][1] != detector and data[i+j][1] != trigger:  # and :
                j += 1
            # Only appends signals in desired detector
            if i+j<len(data) and data[i+j][1] == detector:
                delay.append(data[i+j][0] - data[i][0])

    delay = [(x * 81 *10**-12)*10**8 for x in delay]
    '''
    # For 1st histogram
    (delay_time, sigma) = norm.fit(delay)
    n, bins, patches = plt.hist(delay, bins=50, facecolor='green')
    '''
    # After 1st histogram            
    delay_filt = []
    for x in delay:
        if x > 1 and x <6:
            delay_filt.append(x)     
    (delay_time, sigma) = norm.fit(delay_filt)
    n, bins, patches = plt.hist(delay_filt, bins=50, facecolor='green')
    
    print(delay_filt)
    
    # Adds a line of best fit
    lnspc = np.linspace(1, 6, bins)
    y = norm.pdf(lnspc, delay_time, sigma)
    plt.plot(lnspc, y, 'r--', linewidth=2)
    # Coincidence window
    window = delay_time + 3*sigma
    # Jitter time
    FWHM = 2.355 * sigma
    plt.show()
    return window, FWHM, delay_time


def verification(data, co_window=10):
    '''
    Takes in a list of tuples (time, channel) and a coincidence window in
    number of bins. Outputs a list of polarisations and the basis of
    measurement as a list of strings
    '''
    polar = {1: 'V',
             2: 'H',
             3: '+',
             4: '-'}
    bases = {1: 'VH',
             2: 'VH',
             3: '+-',
             4: '+-'}
    trigger = 2
    polarisation = []
    basis = []
    for i, (time, channel) in enumerate(data):
        # Recording valid pulses
        if channel == trigger and abs(time - data[i+1][0]) <= co_window:
            polarisation.append(polar[data[i+1][1]])
            basis.append(bases[data[i+1][1]])
        # Adding placeholders to keep list the same length as Alice's
        elif channel == trigger:
            polarisation.append('X')
            basis.append('X')
    return polarisation, basis


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=argparse.FileType('r'),
                        help='Input file containing time stamp and channel')
    parser.add_argument('--co_window', default=10, type=int,
                        help='Input coincidence window in bins')
    parser.add_argument('--detector', type=int,
                        help='Input detector for jitter measurement')
    parser.add_argument('--bin_width', type=int,
                        help='Input bin width')
    args = parser.parse_args()
    lines = args.filename.readlines()
    times = []
    for line in lines:
        times.append(tuple(map(float, line.strip().split(','))))
    #print(verification(times, args.co_window))
    print(jitter_and_delay(times, args.detector))

