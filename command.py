"""
Program 4 voltage waveform
"""

import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())

my_instrument = rm.open_resource('USB0::0x0957::0x0407::MY44057486::INSTR')
"""
print(my_instrument.query('*IDN?'))
"""
my_instrument.write('*IDN?')
print(my_instrument.read())

"""
my_instrument.write('OUTPut ON')
"""
my_instrument.write('FREQ 100')
my_instrument.write('APPLy:DC DEF, DEF, 0.5')