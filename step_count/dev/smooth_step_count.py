import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter

def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

data = np.loadtxt('./data/2024-01-10_18.csv', delimiter =',', dtype = str)
xdata = convert_strings_to_floats(data[:,2])
ydata = convert_strings_to_floats(data[:,3])
zdata = convert_strings_to_floats(data[:,4])

accel_mag = np.sqrt((np.power(xdata, 2) + np.power(ydata, 2) + np.power(zdata, 2)))
accel_mag = accel_mag - np.mean(accel_mag)

y_smooth = savgol_filter(accel_mag, window_length=40, polyorder=3, mode="nearest")
smooth_peaks, _ = find_peaks(y_smooth, height=0.2)

# neg_y_smooth = -y_smooth
# neg_smooth_peaks, _ = find_peaks(neg_y_smooth, height=0.2)

print("number of steps:", len(smooth_peaks))

plt.plot(y_smooth)
plt.plot(accel_mag, alpha = 0.5)
plt.plot(smooth_peaks,y_smooth[smooth_peaks], "rx")
# plt.plot(neg_smooth_peaks,-neg_y_smooth[neg_smooth_peaks], "rx")
plt.show()