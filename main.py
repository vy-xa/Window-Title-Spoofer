import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QHBoxLayout
import psutil
import win32gui
import win32process

class WindowTitleChanger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Title Spoofer")
        self.setGeometry(100, 100, 400, 200)

        self.radio_process = QRadioButton("Change based on process name")
        self.radio_process.clicked.connect(self.select_process_name)

        self.radio_window = QRadioButton("Change based on window name")
        self.radio_window.clicked.connect(self.select_window_name)

        self.process_name_label = QLabel("Enter the name of the process:")
        self.process_name_input = QLineEdit()
        self.process_name_input.setEnabled(False)

        self.window_name_label = QLabel("Enter the window name:")
        self.window_name_input = QLineEdit()
        self.window_name_input.setEnabled(False)

        self.new_title_label = QLabel("Enter the new window title:")
        self.new_title_input = QLineEdit()

        self.change_button = QPushButton("Change Window Title")
        self.change_button.clicked.connect(self.change_window_title)

        process_layout = QVBoxLayout()
        process_layout.addWidget(self.process_name_label)
        process_layout.addWidget(self.process_name_input)

        window_layout = QVBoxLayout()
        window_layout.addWidget(self.window_name_label)
        window_layout.addWidget(self.window_name_input)

        input_layout = QHBoxLayout()
        input_layout.addLayout(process_layout)
        input_layout.addLayout(window_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.radio_process)
        layout.addWidget(self.radio_window)
        layout.addLayout(input_layout)
        layout.addWidget(self.new_title_label)
        layout.addWidget(self.new_title_input)
        layout.addWidget(self.change_button)

        self.setLayout(layout)

        self.selected_input = "process"

    def select_process_name(self):
        self.process_name_input.setEnabled(True)
        self.window_name_input.setEnabled(False)
        self.selected_input = "process"

    def select_window_name(self):
        self.process_name_input.setEnabled(False)
        self.window_name_input.setEnabled(True)
        self.selected_input = "window"

    def change_window_title(self):
        if self.selected_input == "process":
            name = self.process_name_input.text()
        else:
            name = self.window_name_input.text()
        new_title = self.new_title_input.text()

        hwnds = []
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                if self.selected_input == "process":
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    try:
                        p = psutil.Process(pid)
                        if name.lower() in p.name().lower():
                            hwnds.append(hwnd)
                    except psutil.NoSuchProcess:
                        pass
                else:
                    title = win32gui.GetWindowText(hwnd)
                    if name.lower() in title.lower():
                        hwnds.append(hwnd)
            return True

        win32gui.EnumWindows(callback, None)

        if hwnds:
            for hwnd in hwnds:
                win32gui.SetWindowText(hwnd, new_title)
            print("Window title successfully changed.")
        else:
            print("Error: Window not found.")

def main():
    app = QApplication(sys.argv)
    window = WindowTitleChanger()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
