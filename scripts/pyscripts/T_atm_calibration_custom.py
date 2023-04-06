import numpy as np
import pandas as pd
import datetime as dt

import scipy.optimize as sp


from lmfit.models import LinearModel
import matplotlib.pyplot as plt

#angles from the zenith in rads

G = 96510.127
angles = [
    0.9,
    10.0,
    20.0,
    29.5,
    39.9 
    
]


P_ANGLE_PATHS = [
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_1",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_2",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_3",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_4",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_5"
    
]

# csv_path = "../../../data/Sys_constants/T_atm.csv"

#loop over paths to average the power
power = []
power_std = []
power_a = []

power_raw = []

for i, P_PATH in enumerate(P_ANGLE_PATHS):
    power_file = G*np.fromfile(open(P_PATH), dtype=np.float32)

    power.append(power_file.mean())
    power_std.append(power_file.std())
    power_a.append(power_file.std()/np.sqrt(len(power_file)))

    power_raw.append(power_file)




angles = np.array(angles)
angles = np.pi/180*angles
print(angles)
angles = np.arccos(angles)

print(power)
# graph relation

# for xe, ye in zip(angles, power_raw):
#     plt.scatter([xe] * len(ye), ye, color='b', marker='.')

# plt.scatter(angles, power, color='orange')
plt.errorbar(angles, power, power_a, color='orange', linestyle='')

print(angles, power)


def linear(x, m, c):
    return x*m+c

popt, pcov = sp.curve_fit(linear, angles, power)
plt.plot(angles, linear(angles, *popt), 'g--',
         label='fit: m=%1.8f, c=%1.8f' % tuple(popt))



# print(popt)
plt.xlabel('x')
plt.ylabel('y')
plt.ylim(0)
plt.legend()
plt.show()

