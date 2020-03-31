import numpy as np
import math
import argparse
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit


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

def lorentzian(x,x0,y0,h,b):
    ''' 
    Returns a 1D array of function values for:
    - x : Input array of x-values
    - x0 : Peak position
    - y0 : Background level
    - h : Peak height
    - b : Half-Width at Half-Maximum
    '''
    return y0 + h/(1+((x-x0)/b)**2)

def jitter_and_delay(data, detector):
    '''
    Takes in a list of tuples (time, channel) and the desired detector that you
    want the jitter time of. Plots and outputs the optimal coincidence window,
    the jitter time and the delay time.
    '''
    delay = []
    bin_width = 125
    clock_period = (81 / 10**6) * bin_width
    trigger = 8
    for i, (time, channel) in enumerate(data):
        if channel == trigger and i < len(data):
            j = 1
            # Removing dark counts from other detectors
            while i + j < len(data) and data[i+j][1] != detector and data[i+j][1] != trigger:  # and :
                j += 1
            # Only appends signals in desired detector
            if i + j < len(data) and data[i+j][1] == detector:
                delay.append((data[i+j][0] - data[i][0]) * clock_period)
    '''
    # For 1st histogram
    (delay_time, sigma) = norm.fit(delay)
    n, bins, patches = plt.hist(delay, bins=50, facecolor='green')
    '''
    
    # After 1st histogram
    low = 2.25
    high = 2.6
    delay_filt = []
    for x in delay:
        if x > low and x < high:
            delay_filt.append(x)
    n, bins, patches = plt.hist(delay_filt, bins=30, facecolor='green')
    i = 0
    midpoint = []
    while i < len(bins)-1:
        midpoint.append((bins[i+1]+bins[i])/2)
        i += 1
    '''
    #Plotting Gaussian fit
    (delay_time, sigma) = norm.fit(delay_filt)
    lnspc = np.linspace(low, high, 100)
    y = norm.pdf(lnspc, delay_time, sigma)
    plt.plot(lnspc, y, 'r--', linewidth=2)
    '''
#    window = delay_time + 3*sigma      # Coincidence window
#    FWHM = 2.355 * sigma               # Jitter time
    
    #Plot Lorentzian fit
    initialPeak = 2.38
    initialBackground = 0
    initialHeight = 17500
    initialHWHM = 0.01
    initialGuess = [initialPeak, initialBackground, initialHeight, initialHWHM]
    lopt, lcov = curve_fit(lorentzian, midpoint, n, p0=initialGuess)
    xLorentz = np.linspace(low, high, len(midpoint)*10)
    plt.plot(xLorentz, lorentzian(xLorentz, *lopt), 'r-', label="Lorentzian Fit")
    plt.title('Detector 4')
    plt.xlabel('Time (ns)')
    plt.ylabel('Counts')
    plt.show()
    jitter = 2*lopt[3]
    delay_time = lopt[0]
    return lopt, jitter, delay_time






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

