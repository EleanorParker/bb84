import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
from pathlib import Path

def voltage_of_max_power(voltage, power):
    max_idx = np.argmax(power)
    return voltage[max_idx]

def normalise(power):
    max_idx = np.argmax(power)
    N = power[max_idx]
    return power/N

def get_index(value, df):
    index = abs(df - value).idxmin()
    return index

if __name__ == "__main__":
    
    detector_1 = "sweep_data_detector_1_7.csv"
    detector_2 = 'sweep_data_detector_2_7.csv'
    detector_3 = 'sweep_data_detector_3_7.csv'
    detector_4 = 'sweep_data_detector_4_7.csv'
    path = Path("sweep_data/2020-03-12/")

    detector_1 = path / detector_1
    detector_2 =  path / detector_2
    detector_3 =  path / detector_3
    detector_4 =  path / detector_4

    # Detector 1
    df = pd.read_csv(detector_1, sep=',', header=None ,
                     names = ['voltage', 'power'])
    voltage_1 = df['voltage']
    power_1 = df['power']
    
    # Detector 2
    df = pd.read_csv(detector_2, sep=',', header=None ,
                     names = ['voltage', 'power'])
    voltage_2 = df['voltage']
    power_2 = df['power']
    
    # Detector 3
    df = pd.read_csv(detector_3, sep=',', header=None ,
                     names = ['voltage', 'power'])
    voltage_3 = df['voltage']
    power_3 = df['power']
    
    # Detector 4
    df = pd.read_csv(detector_4, sep=',', header=None ,
                     names = ['voltage', 'power'])
    voltage_4 = df['voltage']
    power_4 = df['power']
    
    # Plot all Detector Powers as a fucntion of EOM Voltage Sweeps
    plt.figure()
    plt.plot(voltage_1, power_1, 'tab:blue', label='Detector 1')
    plt.plot(voltage_2, power_2, 'tab:red', label='Detector 2')
    plt.plot(voltage_3, power_3, 'tab:green', label='Detector 3')
    plt.plot(voltage_4, power_4, 'tab:purple', label='Detector 4')
    plt.legend()
    
    power_1_norm = normalise(power_1)
    power_2_norm = normalise(power_2)
    power_3_norm = normalise(power_3)
    power_4_norm = normalise(power_4)
    
    # Plot all Detector Powers as a function of EOM Voltage Sweeps
    plt.figure()
    plt.plot(voltage_1, power_1_norm, 'tab:blue', label='Detector 1')
    plt.plot(voltage_2, power_2_norm, 'tab:red', label='Detector 2')
    plt.plot(voltage_3, power_3_norm, 'tab:green', label='Detector 3')
    plt.plot(voltage_4, power_4_norm, 'tab:purple', label='Detector 4')
    plt.legend()
    
    print('Detector 1 : Voltage at Max Power = %.3f V' % voltage_of_max_power(voltage_1, power_1))
    print('Detector 2 : Voltage at Max Power = %.3f V' % voltage_of_max_power(voltage_2, power_2))
    print('Detector 3 : Voltage at Max Power = %.3f V' % voltage_of_max_power(voltage_3, power_3))
    print('Detector 4 : Voltage at Max Power = %.3f V' % voltage_of_max_power(voltage_4, power_4))

    
    # Plot Estimated historgrams
    
    max_voltage = [voltage_of_max_power(voltage_1, power_1),
                voltage_of_max_power(voltage_2, power_2),
                voltage_of_max_power(voltage_3, power_3),
                voltage_of_max_power(voltage_4, power_4)]
    
    for voltage in max_voltage:
        v1_index = get_index(voltage, voltage_1)
        v2_index = get_index(voltage, voltage_2)
        v3_index = get_index(voltage, voltage_3)
        v4_index = get_index(voltage, voltage_4)
        
        probability = np.array([power_1[v1_index],
                       power_2[v2_index],
                       power_3[v3_index],
                       power_4[v4_index]])
        plt.figure()
        plt.title("Voltage: " + str(voltage) + "$\mu$ V")    
        plt.bar(range(1,5), probability, color=('tab:blue', 'tab:red', 'tab:green', 'tab:purple'))
        plt.xlabel("Detector")
        plt.ylabel("Voltage")
        plt.xticks(range(1,5))

        # make normalised version
        probability = pow(np.amax(probability), - 1) * probability
        plt.figure()
        plt.title("Voltage: " + str(voltage) + "$\mu$ V")    
        plt.bar(range(1,5), probability, color=('tab:blue', 'tab:red', 'tab:green', 'tab:purple'))
        plt.xlabel("Detector")
        plt.ylabel("Probability")
        plt.xticks(range(1,5))
        print("%.3f" % voltage   + " Disturbance : %.3f" % np.amin(probability))
        
plt.show()
               

    