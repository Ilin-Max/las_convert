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
        mask = np.where(depth_values < point)[0][-1]
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


null_value = -999.25
start_depth = 0
stop_depth = 6000
step_depth = 0.1524

nm = ["GrC","PF","PG"]

well_name = 20
test_type = nm[1]
file_name_GrC = f"well_{well_name}\well_{well_name}_{test_type}.xlsx"
file_name_PF = f"well_{well_name}\well_{well_name}_{test_type}.xlsx"
file_name_PG = f"well_{well_name}\well_{well_name}_{test_type}.xlsx"
df = pd.read_excel(file_name_PF)

start_interval_get_kern = df[df.keys()[0]]
stop_interval_get_kern = df[df.keys()[1]]
# L = df[df.keys()[2]]


# depth_array = start_interval_get_kern + L
depth_array = start_interval_get_kern + (stop_interval_get_kern - start_interval_get_kern) / 2

las_file_point = make_LASFile_with_point_full_depth(depth_array, 1, name_curve=f"{test_type}_kern", null_value = null_value)
las_file_point.write(f"new\point_kern_{well_name}_{test_type}.las")




