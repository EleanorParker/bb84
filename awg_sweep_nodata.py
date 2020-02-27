'''

'''

import pyvisa
import time
import nidaqmx
import matplotlib.pyplot as plt
import csv

SWEEP_NAME = 'laser_2 3'

"""
CONNECT TO AWG

Connects to the AWG device using pyvisa.
"""
rm = pyvisa.ResourceManager()
print(rm.list_resources())
awg = rm.open_resource('USB0::0x0957::0x0407::MY44057486::INSTR')
awg.write('OUTPut ON')

"""
CONNECT TO DAQ

Connects to the DAQ device using nidaqmx
"""

"""
PREPARE SWEEP

Makes array of voltages, lower is the starting voltage, upper is the
ending voltage, length is the number of steps.
"""
lower = -0.8
upper = 0.8
length = 1000
volts = [lower + x*(upper-lower)/(length-1) for x in range(length)]


"""
EXECUTE SWEEP
"""
power = []
for i in range(len(volts)):
    message = 'APPLy:DC DEF, DEF, '
    message += str(volts[i])
    awg.write(message)
    time.sleep(0.03)
    print(volts[i])

"""
MAKE PLOTS AND SAVE DATA
"""

"""
DISCONNECT DEVICES

The DAQ throws an error if not disconnected.
"""


plt.show()