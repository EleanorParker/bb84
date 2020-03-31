
import pyvisa
import time

"""
EXPERIMENTAL PARAMETERS
"""
# voltages in V (MAX 5V)
VOL_1 = 0.4
VOL_2 = -0.005
VOL_3 = -0.333
VOL_4 = -0.748

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
# dictionary of volatage values useful in the future?
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

# write message into device

awg.write('DATA VOLATILE, ' + str(VOL_1))
awg.write('DATA:COPY VOL1')
awg.write('DATA VOLATILE, ' + str(VOL_2))
awg.write('DATA:COPY VOL2')
awg.write('DATA VOLATILE, ' + str(VOL_3))
awg.write('DATA:COPY VOL3')
awg.write('DATA VOLATILE, ' + str(VOL_4))
awg.write('DATA:COPY VOL4')


# Tell device to make triggers
awg.write('OUTPut:TRIG ON')


awg.write('BURS:MODE TRIG')
awg.write('BURS:NCYC 1')
awg.write('TRIG:SOUR BUS')
awg.write('BURS:STAT ON')


command = ['FUNC:USER VOL1', 'FUNC:USER VOL2', 'FUNC:USER VOL3', 'FUNC:USER VOL4']
x = 0
while x < 100:
    for i in command:
        awg.write(i)
        awg.write('APPL:USER 10, 5 Vpp, 0')
        time.sleep(1)
        awg.write('TRIG')
    x = x+1
'''

awg.write('FUNC:USER STEPFUNC') # Selects the user function

# execute message
awg.write('APPL:USER 1000000, 5 Vpp, 0') #frequency, amplitude, offset


# set device to trigger

# For pulse sweep 

'''
