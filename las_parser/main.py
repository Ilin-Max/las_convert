import numpy as np
import lasio
import pandas as pd
import os

def linear_interpolation(x1, y1, x2, y2, x):
    y = y1 + ((y2 - y1) / (x2 - x1)) * (x - x1)
    return y

def find_index_low_top_border(depth_array, depth_to_search):
    low_border_index = np.where(depth_array <= depth_to_search)[0][-1]
    top_border_index = low_border_index + 1
    return low_border_index, top_border_index


def make_DataFrame_with_GIS_value_in_diskret_depth(exel_file, las_file):
    df = pd.read_excel(exel_file)
    depth_to_search_array = np.array(df[df.keys()[0]])

    las = lasio.LASFile(las_file)
    depth_curves_array = np.array(las.index)
    curves_name = las.curves.keys()
    data = np.ones((len(curves_name[1:]), len(depth_to_search_array)))

    for i in range(0, len(depth_to_search_array)):
        low_border_index, top_border_index = find_index_low_top_border(depth_curves_array, depth_to_search_array[i])
        for j in range(1, len(las.curves)):
            x1 = depth_curves_array[low_border_index]
            x2 = depth_curves_array[top_border_index]
            y1 = las.curves[j].data[low_border_index]
            y2 = las.curves[j].data[top_border_index]
            x = depth_to_search_array[i]
            data[j - 1, i] = linear_interpolation(x1, y1, x2, y2, x)

    output_data = {df.keys()[0]: depth_to_search_array}

    for i in range(len(data)):
        output_data[las.curves[i+1].mnemonic] = data[i]

    return pd.DataFrame(output_data)

def saved_exel_file(df: pd.DataFrame, new_file_path):
    df.to_excel(new_file_path, index=False)
    
def main():
    input_exel_file_path = input("exel-file wich point depth: ")
    input_las_file_path = input("las-file for parsing: ")
    foldef_for_saved = input("foldef for saved: ")
    
    df_output_exel = make_DataFrame_with_GIS_value_in_diskret_depth(input_exel_file_path, input_las_file_path)
    output_file_name = os.path.splitext(os.path.basename(input_exel_file_path))[0]
    output_file_path = (os.path.join(foldef_for_saved, output_file_name) + "_parsing" ".xlsx")

    saved_exel_file(df_output_exel, output_file_path)
    print(f"Файл {output_file_path} сохранен\n")


if __name__ == "__mane__":
    main()




