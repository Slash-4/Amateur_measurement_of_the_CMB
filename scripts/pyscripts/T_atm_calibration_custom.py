import numpy as np
import pandas as pd
import datetime as dt

import scipy.optimize as sp


from lmfit.models import LinearModel
import matplotlib.pyplot as plt

#angles from the zenith in rads

G = 4.9609445291343685e-06
angles = [
    0.9,
    10.0,
    20.0,
    29.5,
    39.9 
    
]

# angles = [
#     0.5, 
#     0.8
# ]

P_ANGLE_PATHS = [
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_1",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_2",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_3",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_1",
    "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/sky_measurement_5"
    
]

# csv_path = "../../../data/Sys_constants/T_atm.csv"

#loop over paths to average the power
power = np.empty_like(P_ANGLE_PATHS)
power_raw = []

for i, P_PATH in enumerate(P_ANGLE_PATHS):
    power_file = G*np.fromfile(open(P_PATH), dtype=np.float32)
    power[i] = power_file.mean()

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




def linear(x, m, c):
    return x*m+c

popt, pcov = sp.curve_fit(linear, angles, power)
plt.plot(angles, linear(angles, *popt), 'g--',
         label='fit: m=%1.8f, c=%1.8f' % tuple(popt))
print(popt)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()



# df = pd.DataFrame({
#     'time_of_measurement': [dt.datetime.now().isoformat(timespec='minutes')],
#     'value': [T_atm],
# })


# df.to_csv(csv_path, mode='a', header=False, index=False)
