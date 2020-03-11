import numpy as np
import math
import argparse
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab


#Script to interact with the IDQ id800-tdc (time-to-digital converter)
#Move to directory
#cd “C:\Program Files\IDQuantique\userlib\src”

#To record time tags for 10 seconds as text to the file “textfile.txt” use:
#id800.exe –t 10 –f textfile.txt

#Figure out if the signal is in the coincidence window of channel 8 (trigger).

#If difference between the trigger and the detector is more than the coincidence window, populate new array with the polarisation that this is associated with ie. V,H,+,-.

#Populate another array saying which basis was used.

#Jitter time

#Need to check to see that the trigger is before instead of after. May take more time for trigger to get to detector?

#Compare code between Alice and Bob. Remove their incorrect basis choice. In another function. Takes the polarisation and basis for both Alice and Bob.
#Compare bases for both and edisregrd the measurements at the 
#Think about what if the arrays are not the same size because a darkcount has been detected or remove a correct count. 

'''
Does the laser send a photon when the trigger goes on? Will the voltage be applied to this photon in time for it to reach the EOM?
Maybe set a certain polarisation with a voltage first.
'''

def verification(data, co_window=10):
    '''
    Takes in a list of tuples (time, channel) and a coincidence window in
    number of bins. Outputs a list of polarisations and the basis of measurement
    as a list of strings
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


def jitter_time(data, detector):
    '''
    Takes in a list of tuples (time, channel) and the desired detector that you
    want the jitter time of. Plots and outputs the jitter time and optimal
    coincidence window.
    '''
    delay = []
    trigger = 2
    for i, (time, channel) in enumerate(data):
        if channel == trigger:
            j = 1
            # Removing dark counts from other detectors
            while data[i+j][1] != detector and data[i+j][1] != trigger:
                j += 1
            # Only appends signals in desired detector
            if data[i+j][1] != trigger:
                delay.append(data[i+j][0] - data[i][0])
    (mu, sigma) = norm.fit(delay)
    n, bins, patches = plt.hist(delay, bins=3, density=1, facecolor='green', alpha=0.75)
    # Adds a line of best fit
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--', linewidth=2)
    # Coincidence window
    window = mu + 3*sigma
    FWHM = 2.355 * sigma
    plt.show()
    return window, FWHM
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=argparse.FileType('r'),
                        help='Input file containing time stamp and channel')
    parser.add_argument('--co_window', default=10, type=int,
                        help='Input coincidence window')
    parser.add_argument('--detector', type=int,
                        help='Input detector for jitter measurement')
    args = parser.parse_args()
    lines = args.filename.readlines()
    times = []
    for line in lines:
        times.append(tuple(map(float, line.strip().split(','))))
    verification(times, args.co_window)
    jitter_time(times, args.detector)