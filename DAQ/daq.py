import nidaqmx
daq = nidaqmx.Task()
daq.ai_channels.add_ai_voltage_chan("Dev1/ai1")
print("Connected to DAQ device ID: " + str(daq.devices))
print(daq.read())
daq.close()