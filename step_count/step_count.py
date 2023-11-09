import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

data = np.loadtxt('acc.csv', delimiter =',', dtype = str)
xdata = convert_strings_to_floats(data[:,2])
ydata = convert_strings_to_floats(data[:,3])
zdata = convert_strings_to_floats(data[:,4])

fig, ax = plt.subplots(3,1)
fig.set_figheight(7.5)
fig.set_figwidth(15)

fig.suptitle("Accelerometer Data", fontsize = 30)
fig.tight_layout()

ax[0].plot(xdata, 'b')
ax[0].set_ylabel('x-axis', fontdict = {'size':20})
ax[0].set_ylim(-5,5)
                
ax[1].plot(ydata, 'r')
ax[1].set_ylabel('y-axis', fontdict = {'size':20})
ax[1].set_ylim(-5,5)

ax[2].plot(zdata, 'g')
ax[2].set_ylabel('z-axis', fontdict = {'size':20})
ax[2].set_ylim(-5,5)

plt.show()

accel_mag = np.sqrt((np.power(xdata, 2) + np.power(ydata, 2) + np.power(ydata, 2)))

fig, ax = plt.subplots(1,1)
fig.set_figheight(7.5)
fig.set_figwidth(15)

fig.suptitle("Accelerometer Data", fontsize = 30)
fig.tight_layout()

ax.plot(accel_mag, 'b')
ax.set_ylabel('Acceleration (m/s^2)', fontdict = {'size':20})
ax.set_ylim(0,7)

plt.show()

# TODO: change height
peaks, _ = find_peaks(accel_mag, height=1.5)

fig, ax = plt.subplots(1,1)
fig.set_figheight(7.5)
fig.set_figwidth(15)

fig.suptitle("Accelerometer Data with Peaks", fontsize = 30)
fig.tight_layout()

ax.plot(accel_mag, 'b')
ax.plot(peaks,accel_mag[peaks], "rx")
ax.set_ylabel('Acceleration (m/s^2)', fontdict = {'size':20})
ax.set_ylim(0,7)

plt.tight_layout()
plt.show()

print("The number of steps taken is", len(peaks))