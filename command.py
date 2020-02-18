"""
Program 4 voltage waveform
"""

import pyvisa
import time

rm = pyvisa.ResourceManager()
#print(rm.list_resources())
my_instrument = rm.open_resource('USB0::0x0957::0x0407::MY44057486::INSTR')
#my_instrument.write('OUTPut ON')

# dictionary of volatage values
volages_def = {
    "H": 0.1,
    "s_plus": 0.2,
    "V": 0.3,
    "s_minus":0.4
}


my_instrument.write('FREQ 100')
my_instrument.write('APPLy:DC DEF, DEF, 0.5')

lower = 0
upper = 5
length = 1000
volts = [lower + x*(upper-lower)/(length-1) for x in range(length)]

for i in range(len(volts)):
    message = 'APPLy:DC DEF, DEF, '
    message += str(volts[i])
    my_instrument.write(message)
    time.sleep(0.5)
