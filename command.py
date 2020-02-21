'''
Waveform Generator


Todo:
Perpare Device to send message at trigger point from laser
'''

import pyvisa
import time

"""
EXPERIMENTAL PARAMETERS
"""
# voltages in V 
VOL_1 = 0
VOL_2 = 0.25
VOL_3 = 0.5
VOL_4 = 1

BLOCK_SIZE = 4 # number of pulses in block
PULSE_LENGTH = 1 # pulse lenght in secounds


"""
CONNECT TO DEVICE
"""
rm = pyvisa.ResourceManager()
print(rm.list_resources())
awg = rm.open_resource('USB0::0x0957::0x0407::MY44057486::INSTR')
awg.write('OUTPut ON')


"""
Prepare Block
"""

# dictionary of volatage values
volages_def = {
    "H": VOL_1,
    "s_plus": VOL_2,
    "V": VOL_3,
    "s_minus": VOL_4
}

# message to send to device
VOL_1 = VOL_1/5
VOL_2 = VOL_2/5
VOL_3 = VOL_3/5
VOL_4 = VOL_4/5

message = 'DATA VOLATILE, ' + str(VOL_1)  + ', '  + str(VOL_2) + ', ' + str(VOL_3) + ', ' + str(VOL_4)

# read message into device
awg.write(message)
awg.write('DATA:COPY STEPFUNC')
awg.write('FUNC:USER STEPFUNC')

# execute message
awg.write('APPL:USER 10, 5 Vpp, 0') #frequency, amplitude, offset


# For pulse sweep 
'''
lower = 0
upper = 5
length = 1000
volts = [lower + x*(upper-lower)/(length-1) for x in range(length)]

for i in range(len(volts)):
    message = 'APPLy:DC DEF, DEF, '
    message += str(volts[i])
    awg.write(message)
    time.sleep(0.1)
    print(volts[i])
'''