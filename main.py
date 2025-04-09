
import sys
from time import sleep
import convert_exel_to_las_for_curve_data, convert_exel_to_las_for_point_data, convert_exel_to_las_for_interval_data

mode = 0

def command_new_mode():
    global mode
    print("""Select mode:
    1 - convert Excel to LAS for curve data
    2 - convert Excel to LAS for interval data
    3 - convert Excel to LAS for point data\n""")
    
    try:
        mode = int(input("mode: "))
        if mode not in (1, 2, 3):
            print("unknown command")
            mode = 0  
    except ValueError:
        print("enter number")
        mode = 0
        
def command_exit():
    print("Завершение программы.")
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

if __name__ == "__main__":
    main()
        






