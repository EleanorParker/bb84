'''
Script to voltage sweep the AOM, so to identify the associated phases.
Data is read using a data Acquisition board.

Output:
    - Graph of voltage sweep and 
    - Data of voltage sweep
    - The data is saved to sweep_data/todays-date/

Parameters:
    SWEEP_NAME: Name for filename
    FOLDER_NAME: Target directory for saved files
    Voltage_MIN: Start voltage of sweep
    VOLTAGE_MAX: End voltage of sweep
    SWEEP_LENGTH: Number of data points
    AMPLIFICATION: Included in filenames, should be set manually not
                   used as input in script 
'''

import pyvisa
import time
import nidaqmx
import matplotlib.pyplot as plt
import csv
from datetime import date
import os

"""
PARAMETERS
"""
# Parameters for book keeping
SWEEP_NAME = 'detector_4'
FOLDER_NAME = 'sweep_data/' +  str(date.today()) + "/"
AMPLIFICATION = 7

# Parameters used in script
VOLTAGE_MAX = 0.75
VOLTAGE_MIN = -0.75
SWEEP_LENGTH = 1000

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
daq = nidaqmx.Task()
daq.ai_channels.add_ai_voltage_chan("Dev1/ai1", min_val=0, max_val=10)
print("Connected to DAQ device ID: " + str(daq.devices))


"""
PREPARE SWEEP

Makes array of voltages, lower is the starting voltage, upper is the
ending voltage, length is the number of steps.
"""
lower = VOLTAGE_MIN
upper = VOLTAGE_MAX
length = SWEEP_LENGTH
volts = [lower + x*(upper-lower)/(length-1) for x in range(length)]


"""
EXECUTE SWEEP
"""
power = []
for i in range(len(volts)):
    message = 'APPLy:DC DEF, DEF, '
    message += str(volts[i])
    awg.write(message)
    time.sleep(0.18)
    power.append(daq.read())
    print("vol: " + str(volts[i]) + " pow: " + str(power[i]))

"""
MAKE PLOTS AND SAVE DATA
"""
# Make directory
if not os.path.exists(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)
    print("Directory " , FOLDER_NAME ,  " Created ")
else:    
    print("Directory " , FOLDER_NAME ,  " already exists")

#power = [pow(AMPLIFICATION, -1)*x for x in power]
plt.figure()
plt.plot(volts, power)
plt.xlabel("Voltage")
plt.ylabel("Power")
plt.savefig(FOLDER_NAME + 'sweep_' + SWEEP_NAME + '_' + str(AMPLIFICATION) + '.pdf')
plt.savefig(FOLDER_NAME + 'sweep_' + SWEEP_NAME + '_' + str(AMPLIFICATION) + '.png', dpi=1200)

with open(FOLDER_NAME + 'sweep_data_' + SWEEP_NAME + '_' + str(AMPLIFICATION) + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(volts, power))


"""
DISCONNECT DEVICES

The DAQ throws an error if not disconnected.
"""
daq.close()
plt.show()