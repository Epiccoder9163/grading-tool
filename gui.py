import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QProgressBar, QTextEdit
)
from PyQt6.QtCore import QThread, pyqtSignal
import inference
import grade

class GradingWorker(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, homework_files, key_files):
        super().__init__()
        self.homework_files = homework_files
        self.key_files = key_files

    def run(self):
        homework_list = []
        key_list = []
        total = len(self.homework_files) + len(self.key_files)
        index = 0

        # Process homework
        for path in self.homework_files:
            output = inference.run(path)
            parsed = [item.split(":")[1].strip() for item in output.split(",")]
            homework_list.extend(parsed)
            self.result.emit(f"{Path(path).name}: {parsed}")
            index += 1
            self.progress.emit(int((index / total) * 100))

        # Process keys
        for path in self.key_files:
            output = inference.run(path)
            parsed = [item.split(":")[1].strip() for item in output.split(",")]
            key_list.extend(parsed)
            self.result.emit(f"{Path(path).name}: {parsed}")
            index += 1
            self.progress.emit(int((index / total) * 100))

        # Grade
        score = grade.run(homework_list, key_list)
        self.finished.emit(f"\nFinal Grade: {score}%")

class GradingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assignment Grader")
        self.resize(700, 500)

        self.homework_files = []
        self.key_files = []

        # Widgets
        self.label = QLabel("Upload homework and answer key images")
        self.pick_homework_btn = QPushButton("Upload Homework Files")
        self.pick_key_btn = QPushButton("Upload Answer Key Files")
        self.start_btn = QPushButton("Start Grading")
        self.start_btn.setEnabled(False)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.pick_homework_btn)
        btn_layout.addWidget(self.pick_key_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

        # Connect buttons
        self.pick_homework_btn.clicked.connect(self.pick_homework)
        self.pick_key_btn.clicked.connect(self.pick_keys)
        self.start_btn.clicked.connect(self.start_grading)

    def pick_homework(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Homework Images", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.homework_files = files
            self.label.setText(f"{len(files)} homework file(s) selected.")
            self.check_ready()

    def pick_keys(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Answer Key Images", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.key_files = files
            self.label.setText(f"{len(files)} key file(s) selected.")
            self.check_ready()

    def check_ready(self):
        if self.homework_files and self.key_files:
            self.start_btn.setEnabled(True)

    def start_grading(self):
        self.output_box.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.show()
        self.label.setText("Running OCR and grading...")

        self.worker = GradingWorker(self.homework_files, self.key_files)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.result.connect(self.output_box.append)
        self.worker.finished.connect(self.show_final_result)
        self.worker.start()

    def show_final_result(self, message):
        self.output_box.append(message)
        self.label.setText("Grading complete.")
        self.progress_bar.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradingApp()
    window.show()
    sys.exit(app.exec())
