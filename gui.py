import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QProgressBar, QTextEdit, QLineEdit
)
from PyQt6.QtCore import QThread, pyqtSignal
import inference
import grade

class GradingWorker(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, paths):
        super().__init__()
        self.paths = paths  # {'Assignment Name': {'homework': [...], 'keys': [...]}}

    def run(self):
        graded = {}
        total = sum(len(v['homework']) + len(v['keys']) for v in self.paths.values())
        index = 0

        for name, files in self.paths.items():
            homework_list = []
            key_list = []

            for hw_path in files['homework']:
                output = inference.run(hw_path)
                parsed = [item.split(":")[1].strip() for item in output.split(",")]
                homework_list.extend(parsed)
                self.result.emit(f"{Path(hw_path).name}: {parsed}")
                index += 1
                self.progress.emit(int((index / total) * 100))

            for key_path in files['keys']:
                output = inference.run(key_path)
                parsed = [item.split(":")[1].strip() for item in output.split(",")]
                key_list.extend(parsed)
                self.result.emit(f"{Path(key_path).name}: {parsed}")
                index += 1
                self.progress.emit(int((index / total) * 100))

            score = grade.run(homework_list, key_list)
            graded[name] = score
            self.result.emit(f"\n{name} → Grade: {score}%")

        self.finished.emit("All assignments graded.")

class GradingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assignment Grader")
        self.resize(700, 500)

        self.paths = {}  # {'Assignment Name': {'homework': [...], 'keys': [...]}}

        # Widgets
        self.label = QLabel("Enter assignment name and upload files:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Assignment name")

        self.pick_homework_btn = QPushButton("Add Homework Pages")
        self.pick_key_btn = QPushButton("Add Answer Key Pages")
        self.add_assignment_btn = QPushButton("Save Assignment")
        self.start_btn = QPushButton("Start Grading")
        self.start_btn.setEnabled(False)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.pick_homework_btn)
        btn_layout.addWidget(self.pick_key_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(self.add_assignment_btn)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

        # Temp storage for current assignment
        self.current_homework = []
        self.current_keys = []

        # Connect buttons
        self.pick_homework_btn.clicked.connect(self.add_homework)
        self.pick_key_btn.clicked.connect(self.add_keys)
        self.add_assignment_btn.clicked.connect(self.save_assignment)
        self.start_btn.clicked.connect(self.start_grading)

    def add_homework(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Homework Pages", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.current_homework.extend(files)
            self.label.setText(f"Homework pages selected: {len(self.current_homework)}")

    def add_keys(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Answer Key Pages", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.current_keys.extend(files)
            self.label.setText(f"Key pages selected: {len(self.current_keys)}")

    def save_assignment(self):
        name = self.name_input.text().strip()
        if not name:
            name = f"Assignment {len(self.paths) + 1}"
        if self.current_homework and self.current_keys:
            self.paths[name] = {
                'homework': self.current_homework.copy(),
                'keys': self.current_keys.copy()
            }
            self.output_box.append(f"Saved {name} with {len(self.current_homework)} homework and {len(self.current_keys)} key pages.")
            self.current_homework.clear()
            self.current_keys.clear()
            self.name_input.clear()
            self.label.setText("Assignment saved. You can add another or start grading.")
            self.start_btn.setEnabled(True)
        else:
            self.label.setText("Please select both homework and key pages before saving.")

    def start_grading(self):
        self.output_box.append("\nGrading...\n")
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.show()
        self.label.setText("Grading in progress...")

        self.worker = GradingWorker(self.paths)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.result.connect(self.output_box.append)
        self.worker.finished.connect(self.show_final_result)
        self.worker.start()

    def show_final_result(self, message):
        self.label.setText(message)
        self.progress_bar.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradingApp()
    window.show()
    sys.exit(app.exec())
