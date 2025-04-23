
import sys
from time import sleep
import convert_exel_to_las_for_curve_data, convert_exel_to_las_for_point_data, convert_exel_to_las_for_interval_data
import las_parser.main
import convert_time_to_depth.main

mode = 0

def command_new_mode():
    global mode
    print("""\nSelect mode:
    1 - convert Excel to LAS for curve data
    2 - convert Excel to LAS for interval data
    3 - convert Excel to LAS for point data
    4 - parser LAS-file
    5 - convert Time data to Depth data\n""")
    try:
        mode = int(input("mode: "))
        if mode not in (1, 2, 3, 4, 5):
            print("unknown command\n")
            mode = 0  
    except ValueError:
        print("enter number")

        
def command_exit():
    print("exit programm.")
    sleep(3)
    sys.exit(0)

def mode_curve_data():
    global mode
    convert_exel_to_las_for_curve_data.main()
    mode = 0

def mode_interval_data():
    global mode
    convert_exel_to_las_for_interval_data.main()
    mode = 0

def mode_point_data():
    global mode
    convert_exel_to_las_for_point_data.main()
    mode = 0

def mode_parser_lasfile():
    global mode
    las_parser.main.main()
    mode = 0

def mode_convert_Time_to_Depth():
    global mode
    convert_time_to_depth.main.main()
    mode = 0

def main():
    global mode
    while True:
        if mode == 0:
            command_new_mode()
        elif mode == 1: 
            mode_curve_data()
        elif mode == 2: 
            mode_interval_data()
        elif mode == 3: 
            mode_point_data()
        elif mode == 4:
            mode_parser_lasfile()
        elif mode == 5:
            mode_convert_Time_to_Depth()

if __name__ == "__main__":
    main()