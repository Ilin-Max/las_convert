import matplotlib.pyplot as plt
import numpy as np
import lasio
from numba import prange
import os


def Make_Filtr_StartDrill_by_Time (WOB_array = np.array([]), Time_array = np.array([]), n_second_delete = 60):
    
    Filtr = np.empty(len(Time_array))
    
    select = True
    for i in range(len(Time_array) - 1):

        if WOB_array[i] == 0 and WOB_array[i + 1] > 0:
            count = 0
            select = False
        elif not select:
            count += 1 
            if count == n_second_delete + 1:
                select = True
         
        Filtr[i] = select
        
    return Filtr
    
def Make_Filtr_StartDrill_by_MD (MD_array = np.array([]), WOB_array = np.array([]), n_meters_delete = 1):
    
    Filtr = np.empty(len(MD_array))
    
    select = True
    for i in range(len(MD_array) - 1):
        
        if WOB_array[i] == 0 and WOB_array[i + 1] > 0:
            start_md = MD_array[i]
            select = False
        elif not select:
            if MD_array[i] >= start_md + n_meters_delete:
                select = True  
                
        Filtr[i] = select
        
    return Filtr    

def Make_Filtr_Drilling(MD_array = np.array([])):
    
    Filtr = np.empty(len(MD_array))

    MD_max = 0

    select = False
    for i in range(len(MD_array) - 1):
        if MD_array[i] > MD_max:
            MD_max = MD_array[i]
        if MD_array[i + 1] > MD_max:
            select = True
        else:
            select = False
            
        Filtr[i] = select

    return(Filtr)

def Make_Filtr_Drilling_with_start_MD(MD_array = np.array([]), start_md = 0):
    
    Filtr = np.empty(len(MD_array))

    MD_max = start_md

    select = False
    for i in range(len(MD_array) - 1):
        if MD_array[i] > MD_max:
            MD_max = MD_array[i]
        if MD_array[i + 1] > MD_max:
            select = True
        else:
            select = False
            
        Filtr[i] = select

    return(Filtr)


def Select_Date(array, filtr):
        
    index_select = np.where((filtr == 1))[0]
    
    selected_data = np.empty(len(index_select))
    for i in range(len(index_select)):
        selected_data[i] = array[index_select[i]]

    return selected_data

def Drow_Arrays(Axis_Y, *arrgs, titles_list = [], suptitle = ""):
    colors = [
    'blue',       # Синий
    'green',      # Зеленый
    'red',        # Красный
    'magenta',    # Пурпурный
    'orange',     # Оранжевый
    'purple',     # Фиолетовый
    'brown'       # Коричневый
    ]

    n_arrgs = len(arrgs)
    fig, axes = plt.subplots(1,n_arrgs, figsize=(10, 20), sharey=True)
    
    if len(titles_list) == 0:
        titles_list = [f"График {i + 1}" for i in range(n_arrgs)]
    fig.suptitle(suptitle)
    if n_arrgs == 1:
        axes = [axes]
    
    axes[0].invert_yaxis()
    for i in range(n_arrgs):
        
        data_for_axes = arrgs[i]
        
        if type(data_for_axes) == list:
            for j in range(len(data_for_axes)):
                if j == 0:
                    axes[i].plot(data_for_axes[j], Axis_Y, c = colors[i])
                    axes[i].set_title(titles_list[i], fontsize= 8)
                else:
                    axes[i].plot(data_for_axes[j], Axis_Y,"--", c = 'black', lw = 1)
                    axes[i].grid()
                    
        if type(data_for_axes) == np.ndarray:
            data_for_axes = [data_for_axes]
            for j in range(len(data_for_axes)):
                if j == 0:
                    axes[i].plot(data_for_axes[j], Axis_Y, c = colors[i])
                    axes[i].set_title(titles_list[i], fontsize=8)
                    axes[i].grid()
                else:
                    axes[i].plot(data_for_axes[j], Axis_Y,"--", c = 'black', lw = 1)
    plt.show()

def GetStatistic_Depht(MD, LOG, WIN_Depht, border_point = False, nan = np.nan):
    
    if len(MD) != len(LOG):
        print("Длина массивов не одинакова")
        return [0,0,0,0]

    if border_point: # усредненния с учетом граничных точек
        
        MD_new = np.empty(len(MD))        
        MEAN_LOG = np.empty(len(MD))
        MAX_LOG = np.empty(len(MD))
        MIN_LOG = np.empty(len(MD))
        
        for i in range(len(MD)):
            
            if MD[i] < (MD[0] + WIN_Depht/2):
                list_index_window = np.where(MD <= MD[i] + WIN_Depht)[0]
                
            elif MD > (MD[-1] - WIN_Depht/2):
                pass
            else:
                pass
        
    if not border_point: # усредненния без учета граничных точек
        
        list_index_sort_array = np.where((MD > MD[0] + WIN_Depht/2) & (MD < MD[-1] - WIN_Depht/2))[0]
        start_index_sort_array = list_index_sort_array[0]
        stop_index_sort_array = list_index_sort_array[-1]
        len_sort_array = len(list_index_sort_array)
        
       
        MEAN_LOG = np.empty(len(MD))
        MAX_LOG = np.empty(len(MD))
        MIN_LOG = np.empty(len(MD))


        for i in range(len(MD)):
            if start_index_sort_array <= i <= stop_index_sort_array:
                list_index_window = np.where((MD >= MD[i] - WIN_Depht/2) & (MD <= MD[i] + WIN_Depht/2))[0]
                
                if len(list_index_window) > 1:
                    start_index_window = list_index_window[0]
                    stop_index_window = list_index_window[-1] 
                    MEAN_LOG[i] = np.mean(LOG[start_index_window : stop_index_window])
                    MAX_LOG[i] = np.max(LOG[start_index_window : stop_index_window])
                    MIN_LOG[i] = np.min(LOG[start_index_window : stop_index_window])
                else:
                    MEAN_LOG[i] = nan
                    MAX_LOG[i] = nan
                    MIN_LOG[i] = nan
                    
            else:
                    MEAN_LOG[i] = nan
                    MAX_LOG[i] = nan
                    MIN_LOG[i] = nan
                
            
    return(MEAN_LOG, MAX_LOG, MIN_LOG)

def GetStatistic_Time(LOG, WIN):
    
    """
    Рачитывает усредненные, максимальные, минимальные значения массива в скользящем окне
    
    Аргументы:
        LOG (ndarray): Масиив над которым проводится операция.
        WIN (int): Количество элементов для усреднения, определения максимума и минимума.

    Возвращает:
        list[ndarray, ndarray, ndarray]: Массив усредненных, максимальных, минимальных значений. 
    """
    
    ROL_WIN = [LOG[i:i+WIN] for i in prange(len(LOG)-WIN)]
    MEAN = np.empty(len(ROL_WIN))
    MAX = np.empty(len(ROL_WIN))
    MIN = np.empty(len(ROL_WIN))
    
    for i in range(len(ROL_WIN)):
        MEAN[i] = np.mean(ROL_WIN[i])
        MAX[i] = np.max(ROL_WIN[i])
        MIN[i] = np.min(ROL_WIN[i])
        
    return(MEAN, MAX, MIN)

def Convert_GTI_to_DEPTH(LASFile, MD_mnemonic = "MD", target_curve = [], skip_time_colume = 0):
    las = LASFile
    MD_time = las[MD_mnemonic]
    Filtr_drillig = Make_Filtr_Drilling(MD_array = MD_time)
    MD = Select_Date(MD_time, Filtr_drillig)

    new_las = lasio.LASFile()
    new_las.append_curve("DEPTH", MD, unit="m", descr="MD")
    for i in range(skip_time_colume, len(las.curves)):
        try:
            curve = las.curves[i]
            if len(target_curve) == 0:
                new_las.append_curve(curve.mnemonic, Select_Date(curve.data, Filtr_drillig), curve.unit, descr=curve.descr)
            else:
                if curve.mnemonic in target_curve:
                    new_las.append_curve(curve.mnemonic, Select_Date(curve.data, Filtr_drillig), curve.unit, descr=curve.descr)
        except ValueError:
            continue
    return new_las

def Convert_GTI_to_DEPTH_with_start_MD(LASFile, MD_mnemonic = "MD", start_md = 0, target_curve = []):
    las = LASFile
    MD_time = las[MD_mnemonic]
    Filtr_drillig = Make_Filtr_Drilling_with_start_MD(MD_array = MD_time, start_md = start_md)
    MD = Select_Date(MD_time, Filtr_drillig)
    
    new_las = lasio.LASFile()
    new_las.append_curve("DEPTH", MD, unit="m", descr="MD")
    for i in range(2, len(las.curves)):
        curve = las.curves[i]
        if len(target_curve) == 0:
            new_las.append_curve(curve.mnemonic, Select_Date(curve.data, Filtr_drillig), curve.unit, descr=curve.descr)
        else:
            if curve.mnemonic in target_curve:
                new_las.append_curve(curve.mnemonic, Select_Date(curve.data, Filtr_drillig), curve.unit, descr=curve.descr)

    max_md = np.max(MD)
    
    return new_las, max_md


def save_las_file(LASFile, new_file_path):
    LASFile.write(new_file_path, version=2.0)

def main():
    input_las_file_path = input("Time las file: ")
    input_mnemonic_MD_array = input("Mnemonic MD curve: ")
    input_target_curve = input("required curves (space): ").strip(" ")
    foldef_for_saved = input("foldef for saved: ")
    
    "Чтение LAS"
    las = lasio.read(input_las_file_path)
    convert_las = Convert_GTI_to_DEPTH(las, MD_mnemonic = input_mnemonic_MD_array, target_curve = input_target_curve)
    
    output_file_name = os.path.splitext(os.path.basename(input_las_file_path))[0]
    output_file_path = (os.path.join(foldef_for_saved, output_file_name) + "_Convert" + ".las")
        
    save_las_file(convert_las, output_file_path)
    print(f"Файл {output_file_path} сохранен\n")


if __name__ == "__main__":
    main()