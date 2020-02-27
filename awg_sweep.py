'''

'''

import pyvisa
import time
import nidaqmx
import matplotlib.pyplot as plt
import csv

SWEEP_NAME = 'laser_1 1'

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
daq.ai_channels.add_ai_voltage_chan("Dev1/ai1")
print("Connected to DAQ device ID: " + str(daq.devices))


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
    power.append(daq.read())

"""
MAKE PLOTS AND SAVE DATA
"""

plt.figure()
plt.plot(volts, power)
plt.xlabel("Voltage")
plt.ylabel("Power")
plt.savefig('sweep_' + SWEEP_NAME + '.png')
plt.show()

with open('sweep_data_' + SWEEP_NAME + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(volts, power))


"""
DISCONNECT DEVICES

The DAQ throws an error if not disconnected.
"""
daq.close()