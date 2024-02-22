import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

data = np.loadtxt('./data/2023-12-03_12.csv', delimiter =',', dtype = str)
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

accel_mag = np.sqrt((np.power(xdata, 2) + np.power(ydata, 2) + np.power(zdata, 2)))
accel_mag = accel_mag - np.mean(accel_mag)

fig, ax = plt.subplots(1,1)
fig.set_figheight(7.5)
fig.set_figwidth(15)

fig.suptitle("Accelerometer Data", fontsize = 30)
fig.tight_layout()

ax.plot(accel_mag, 'b')
ax.set_ylabel('Acceleration (m/s^2)', fontdict = {'size':20})
ax.set_ylim(-2,2)

plt.show()

# TODO: change height
# accel_mag = accel_mag - np.mean(accel_mag)
# min_peak_height = np.std(accel_mag) + np.mean(accel_mag)

# peaks, _ = find_peaks(accel_mag, height=min_peak_height)

std_dev_height = np.std(accel_mag)
height = 0.3
min_peak_height = std_dev_height if std_dev_height > height else height
peaks, _ = find_peaks(accel_mag, height=min_peak_height)

fig, ax = plt.subplots(1,1)
fig.set_figheight(7.5)
fig.set_figwidth(15)

fig.suptitle("Accelerometer Data with Peaks", fontsize = 30)
fig.tight_layout()

ax.plot(accel_mag, 'b')
ax.plot(peaks,accel_mag[peaks], "rx")
ax.set_ylabel('Acceleration (m/s^2)', fontdict = {'size':20})
ax.set_ylim(-2,2)

plt.tight_layout()
plt.show()

neg_accel_mag = -accel_mag

neg_std_dev_height = np.std(neg_accel_mag)
neg_height = 0.18
neg_min_peak_height = neg_std_dev_height if neg_std_dev_height > neg_height else height
neg_peaks, _ = find_peaks(neg_accel_mag, height=neg_min_peak_height)

fig, ax = plt.subplots(1,1)
fig.set_figheight(7.5)
fig.set_figwidth(15)

fig.suptitle("Neg Accelerometer Data with Peaks", fontsize = 30)
fig.tight_layout()

ax.plot(neg_accel_mag, 'b')
ax.plot(neg_peaks,neg_accel_mag[neg_peaks], "rx")
ax.set_ylabel('Neg Acceleration (m/s^2)', fontdict = {'size':20})
ax.set_ylim(-2,2)

plt.tight_layout()
plt.show()

total_peaks = len(peaks) if len(peaks) < len(neg_peaks) else len(neg_peaks)

print("The number of steps taken is", total_peaks)