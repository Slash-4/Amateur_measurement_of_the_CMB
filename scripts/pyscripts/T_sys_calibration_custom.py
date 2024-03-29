import numpy as np
import pandas as pd
import datetime as dt



#temperature in Kelvin (k)
# T_hot = 276.45
# T_cold = 77


# P_COLD_PATH = "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/cold_load_foam1"
# P_HOT_PATH = "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/hot_load_foam1"


# csv_path = "../../../data/Sys_constants/T_sys.csv"

# p_cold = np.fromfile(open(P_COLD_PATH), dtype=np.float32, count=800)
# p_hot = np.fromfile(open(P_HOT_PATH), dtype=np.float32, count=800)

#graph histogram

def Temp_system(T_hot, T_cold, p_hot, p_cold):
    p_cold_avg = p_cold.mean()
    p_hot_avg = p_hot.mean()

    T_system = (T_hot - T_cold*(p_hot_avg/p_cold_avg))/((p_hot_avg/p_cold_avg)-1) 
    T_system = p_hot_avg*(T_hot-T_cold)/(p_hot_avg-p_cold_avg)-T_hot

    df = pd.DataFrame({
        'time_of_measurement': [dt.datetime.now().isoformat(timespec='minutes')],
        'value': [T_system],
        'T_hot': [T_hot],
        'T_cold': [T_cold]
    })
    print(df)
    return T_system


# csv_path = "/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/Sys_constants/T_sys.csv"
# df.to_csv(csv_path, mode='a', header=False, index=False)
