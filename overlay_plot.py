import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Detector 1
df = pd.read_csv('sweep_data_laser_1_10^-6.csv', sep=',', header=None ,
                 names = ['voltage', 'power'])
voltage_1 = df['voltage']
power_1 = df['power']

# Detector 2
df = pd.read_csv('sweep_data_laser_2 4.csv', sep=',', header=None ,
                 names = ['voltage', 'power'])
voltage_2 = df['voltage']
power_2 = df['power']

# Detector 3
df = pd.read_csv('sweep_data_laser_3_1.csv', sep=',', header=None ,
                 names = ['voltage', 'power'])
voltage_3 = df['voltage']
power_3 = df['power']

# Detector 4
df = pd.read_csv('sweep_data_laser_4_1.csv', sep=',', header=None ,
                 names = ['voltage', 'power'])
voltage_4 = df['voltage']
power_4 = df['power']

# Plot all Detector Powers as a fucntion of EOM Voltage Sweeps
plt.figure()
plt.plot(voltage_1, power_1, 'b-', label='Detector 1')
plt.plot(voltage_2, power_2, 'r-', label='Detector 2')
plt.plot(voltage_3, power_3, 'g-', label='Detector 3')
plt.plot(voltage_4, power_4, 'y-', label='Detector 4')
plt.legend()

def voltage_of_max_power(voltage, power):
    max_idx = np.argmax(power)
    return voltage[max_idx]
