import os.path
from funcs import read_exel_file, make_LASFile_for_curve_data, save_lasfile

def main():
    input_file_path = input("input exel file: ")
    foldef_for_saved = input("foldef for saved: ")
    filename = os.path.splitext(os.path.basename(input_file_path))[0]
    df = read_exel_file(input_file_path)
    las_file = make_LASFile_for_curve_data(df)
    save_lasfile(las_file, foldef_for_saved, filename)

if __name__ == "__main__":
    main()

