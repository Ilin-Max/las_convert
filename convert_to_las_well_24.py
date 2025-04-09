import lasio
import numpy as np
import pandas as pd

def make_new_array_wich_null_value_between_values(init_array, null_value = -999.25):
    new_array = np.ones(len(init_array) * 2 - 1) * null_value
    count = 0
    for i in range(len(new_array)):
        if i % 2 == 0:
            new_array[i] = init_array[count]
            count += 1
    return new_array
    
def make_LASFile_with_point(depth_array, value_array, null_value = -999.25):
    depth_array_new = make_new_array_wich_null_value_between_values(depth_array, null_value=null_value)
    values_array_new = make_new_array_wich_null_value_between_values(value_array, null_value=null_value)
    las_file = lasio.LASFile()
    las_file.append_curve("DEPTH", depth_array_new, unit="m", descr="Depth")
    las_file.append_curve("VALUE", values_array_new, unit="", descr="")
    return(las_file)

def make_LASFile_with_point_full_depth(depth_array, value, name_curve = "Value", null_value = -999.25):
    start_depth = 0
    stop_depth = 6000
    step_depth = 0.1524

    depth_values = np.arange(start_depth, stop_depth, step_depth)
    point_array = np.ones(len(depth_values)) * null_value
    for point in depth_array:
        top = np.where(depth_values < point)[0][-1]
        low = top + 1

        mask = top
        if np.abs(point - top) > np.abs(point - low):
            mask = low

        point_array[mask] = value 
    las_file = lasio.LASFile()
    las_file.append_curve("DEPTH", depth_values, unit="m", descr="Depth")
    las_file.append_curve(f"{name_curve}", point_array, unit="", descr="")
    return(las_file)

def make_LASFile_with_interval(start_interval_array, stop_interval_array, value, null_value = -999.25):
    start_depth = 0
    stop_depth = 6000
    step_depth = 0.1524

    depth_values = np.arange(start_depth, stop_depth, step_depth)
    interval_array = np.ones(len(depth_values)) * null_value
    for start, stop in zip(start_interval_array, stop_interval_array):
        mask = np.logical_and(depth_values >= start, depth_values <= stop)
        interval_array[mask] = value 

    las_file = lasio.LASFile()
    las_file.append_curve("DEPTH", depth_values, unit="m", descr="Depth")
    las_file.append_curve("interval_array", interval_array, unit="", descr="")
    
    return las_file


#well 24
well_name = 24
file_name = f"well_24\kern_infa_well_{well_name}.xlsx"
df = pd.read_excel(file_name)
count = 1
for key in df.keys():
    key = df.keys()[10]
    depth_array = df[key].dropna()
    print(depth_array)
    las_file_point = make_LASFile_with_point_full_depth(depth_array, 1, name_curve=f"kern_test")
    las_file_point.write(f"well_24\новые ласы\point_kern_{well_name}_{key}.las")
    count += 1
