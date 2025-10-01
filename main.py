import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,\
      QWidget, QPushButton, QFileDialog, QLabel, QRadioButton, QGroupBox, QLineEdit
from funcs_convert import read_exel_file, make_LASFile_for_curve_data, make_LASFile_for_interval_data, make_LASFile_for_point_data

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("LAS-converter")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        MainVerticalLayout = QVBoxLayout(central_widget)
        self.setAcceptDrops(True)

        GroupBoxForModes = QGroupBox("Формат входных данных")
        GorizontalLayoutForRadioButton = QHBoxLayout()
        self.radio_CurveData = QRadioButton("Данные в виде кривой")
        self.radio_PointData = QRadioButton("Точечные данные")
        self.radio_IntervalData = QRadioButton("Данные по интервалам")
        self.radio_PointData.setChecked(True)
        GorizontalLayoutForRadioButton.addWidget(self.radio_CurveData)
        GorizontalLayoutForRadioButton.addWidget(self.radio_PointData)
        GorizontalLayoutForRadioButton.addWidget(self.radio_IntervalData)
        GroupBoxForModes.setLayout(GorizontalLayoutForRadioButton)

        GroupBoxForSelectFile = QGroupBox("Выбор файла")
        VerticalLayoutForSelectFileWidget = QVBoxLayout()
        self.btn_FileSelection = QPushButton('Выбрать файл')
        self.lbl_SelectedFile = QLabel("Файл не выбран")                                          
        VerticalLayoutForSelectFileWidget.addWidget(self.btn_FileSelection)
        VerticalLayoutForSelectFileWidget.addWidget(self.lbl_SelectedFile)
        GroupBoxForSelectFile.setLayout(VerticalLayoutForSelectFileWidget)

        GroupBoxForConvertFile = QGroupBox("Преобразование")
        VerticalLayoutForConvertFileWidget = QVBoxLayout()
        GorizontalLayoutForEnterStepDiskret = QHBoxLayout()
        self.ent_Step_diskret = QLineEdit("0.1524")
        self.btn_FileConvert = QPushButton('Конвектировать файл')
        self.lbl_SavedFile = QLabel("")
        VerticalLayoutForConvertFileWidget.addWidget(self.ent_Step_diskret)
        VerticalLayoutForConvertFileWidget.addWidget(self.btn_FileConvert)
        VerticalLayoutForConvertFileWidget.addWidget(self.lbl_SavedFile)
        GroupBoxForConvertFile.setLayout(VerticalLayoutForConvertFileWidget)

        MainVerticalLayout.addWidget(GroupBoxForModes)
        MainVerticalLayout.addWidget(GroupBoxForSelectFile)
        MainVerticalLayout.addWidget(GroupBoxForConvertFile)

        self.btn_FileSelection.clicked.connect(self.FileSelection)
        self.btn_FileConvert.clicked.connect(self.FileConvert)
        

    def FileSelection(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        if fname:
            self.lbl_SelectedFile.setText(fname)

    def FileConvert(self):
        fname, _ = QFileDialog.getSaveFileName(
            self,                         
            "Сохранить файл",              # Заголовок окна
            "",                           # Начальная директория (пусто = текущая)
            "LAS Files (*.las);;All Files (*)"  # Фильтры расширений
        )
        if fname:
            try:
                df = read_exel_file(self.lbl_SelectedFile.text())
                
                if self.radio_CurveData.isChecked():
                    las = make_LASFile_for_curve_data(df)
                elif self.radio_PointData.isChecked():
                    las = make_LASFile_for_point_data(df)
                elif self.radio_IntervalData.isChecked():
                    las = make_LASFile_for_interval_data(df)
                
                las.write(fname)
                self.lbl_SavedFile.setText(f"Файл сохранен как: {fname}")
            except:
                print("Error")

def application():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()