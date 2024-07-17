from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QFileDialog
from  gpx_txt_dxf import read_coordinates, convert_coordinates, convert_to_gpx, save_to_gpx, read_coordinates_dxf
import os

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        self.file_choice = QLineEdit('- plik txt -', self)
        self.file_choice.setFixedWidth(250)
        self.file_choice.move(25, 120)

        choose_file_btn = QPushButton("Wybierz plik", self)
        choose_file_btn.move(50, 150)
        choose_file_btn.clicked.connect(self.choose_file)

        convert_to_gpx_btn = QPushButton("Konwertuj na GPX", self)
        convert_to_gpx_btn.move(150, 150)
        convert_to_gpx_btn.clicked.connect(self.convert_to_gpx)

        quit_btn = QPushButton("Wyjście", self)
        quit_btn.move(220, 270)
        quit_btn.clicked.connect(QApplication.instance().quit)

        self.setFixedSize(300, 300)
        self.setWindowTitle("GPX")

        self.show()

    def choose_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik txt", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            self.file_choice.setText(file_name)

    def convert_to_gpx(self):
        input_file = self.file_choice.text()
        if input_file == '- plik txt -':
            QMessageBox.warning(self, "Brak pliku", "Proszę wybrać plik tekstowy przed konwersją.")
            return

        # Pobierz nazwę pliku bez ścieżki
        base_name = os.path.basename(input_file)

        # Zmień przyrostek i zachowaj oryginalną nazwę pliku
        output_file = os.path.join(os.path.dirname(input_file), base_name[:-4] + "_gpx.gpx")

        # Wczytaj współrzędne
        points = read_coordinates(input_file)

        # Przekształć współrzędne do formatu GPX
        lat_lon_list = convert_coordinates(points)
        gpx_tree = convert_to_gpx(lat_lon_list)

        # Zapisz do pliku GPX
        save_to_gpx(gpx_tree, output_file)

        QMessageBox.information(self, "Konwersja zakończona", f"Plik GPX został zapisany jako {output_file}.")


    def closeEvent(self, event: QCloseEvent):
        should_close = QMessageBox.question(self, "Zamknięcie aplikacji",  "Czy na pewno chcesz zamknąć?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if should_close == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication([])

    login_window = LoginWindow()

    app.exec()
