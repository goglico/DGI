import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget
from pyqtgraph import PlotWidget
import numpy as np
import wave
import io

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("client")
        layout = QVBoxLayout()

        self.listWidget = QListWidget()
        self.listWidget.clicked.connect(self.on_file_selected)

        self.plotWidget = PlotWidget()

        self.getFilesButton = QPushButton("Получить файл")
        self.getFilesButton.clicked.connect(self.populate_file_list)

        layout.addWidget(self.getFilesButton)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.plotWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_file_list(self):
        response = requests.get("http://localhost:3000/get_files")
        if response.status_code == 200:
            self.listWidget.clear()
            for file_info in response.json():
                self.listWidget.addItem(file_info["filename"])

    def on_file_selected(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            filename = current_item.text()
            response = requests.get(f"http://localhost:3000/get_file/{filename}")
            if response.status_code == 200:
                audio_data = wave.open(io.BytesIO(response.content))
                frames = audio_data.readframes(audio_data.getnframes())
            
                audio_np = np.frombuffer(frames, dtype=np.int16)
                self.plotWidget.clear()
                self.plotWidget.plot(audio_np)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())


