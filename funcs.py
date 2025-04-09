import lasio 
import numpy as np
import pandas as pd
import os.path

def read_exel_file(file_exel: str) -> pd.DataFrame: 
    df = pd.read_excel(file_exel)
    return df

def save_lasfile(las_file: lasio.LASFile, folder_for_save: str, file_name: str) -> None: 
    output_file_path = os.path.join(folder_for_save, file_name) + ".las"
    las_file.write(output_file_path)
    print(f"file {output_file_path} was saved\n")

def find_index_nearest_value_in_sort_array(value: float, array: np.ndarray) -> np.ndarray: 
    
    mask = np.where(array < value)[0][-1]

    if np.abs(value - mask) > np.abs(value - mask):
        mask += 1
    
    return mask

def make_LASFile_for_curve_data(df: pd.DataFrame) -> lasio.LASFile:
    keys = list(df.keys())
    
    las_file = lasio.LASFile()
    for i in range(len(keys)):
        las_file.append_curve(keys[i], df[keys[i]], unit="", descr="")
    
    return las_file

def make_LASFile_for_point_data(df: pd.DataFrame, null_value = -999.25) -> lasio.LASFile:
    las_file = lasio.LASFile()

    keys = df.keys()
    depth_point_data = df[keys[0]]
    step = 0.01
    depth_array = np.arange(np.min(depth_point_data) - step * 2, np.max(depth_point_data) + step * 2, step)
    las_file.append_curve("DEPTH", depth_array, unit="m", descr="")
    for key in keys[1:]:
        point_array = np.ones(len(depth_array)) * null_value
        for i in range(len(depth_point_data)):
            mask = find_index_nearest_value_in_sort_array(depth_point_data[i], depth_array)
            point_array[mask] = df[key][i]
        las_file.append_curve(key + "_core", point_array, unit="", descr="")
    return las_file

def make_LASFile_for_interval_data(df: pd.DataFrame, null_value = -999.25) -> lasio.LASFile:
    las_file = lasio.LASFile()

    keys = df.keys()
    depth_start_interval_data = df[keys[0]]
    depth_stop_interval_data = df[keys[1]]
    step = 0.1524
    depth_array = np.arange(np.min(depth_start_interval_data), np.max(depth_stop_interval_data) + step * 2, step)
    las_file.append_curve("DEPTH", depth_array, unit="m", descr="")
    for key in keys[2:]:
        interval_array = np.ones(len(depth_array)) * null_value
        for i, (start, stop) in enumerate(zip(depth_start_interval_data, depth_stop_interval_data)):
            mask = (depth_array >= start) & (depth_array <= stop)
            value = df[key].iloc[i]  # значение параметра для данного интервала
            interval_array[mask] = value
        las_file.append_curve(key, interval_array, unit="", descr="")

    return las_file