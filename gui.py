# Script used for GUI

import sys
import os
from configparser import ConfigParser
from pathlib import Path
from typing import List, Dict
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QProgressBar, QTextEdit, QLineEdit, QComboBox, QDialog, QCheckBox
)
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QThread, pyqtSignal
import inference
import grade
import export
import explain
import ollama

# Configuration path
path = "config.ini"

# Worker class for grading assignments via gui
# Coordinates explanation, grading, and inferencing.
class GradingWorker(QThread):
    gui_state = pyqtSignal(bool)
    export_btn_signal = pyqtSignal(bool)
    progress = pyqtSignal(int)
    result = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, paths):
        super().__init__()
        self.paths = paths

    def run(self):
        global grades
        global wrong_answers_final
        global explanations

        config = ConfigParser()
        config.read(path)
        model = config.get("General", "Model")

        # Change UI state, disable button
        self.gui_state.emit(False)
        self.export_btn_signal.emit(False)

        graded = {}
        grades = []
        explanations = []
        wrong_answers_final = []

        # If ollama.show(model) fails, the model does not exist.
        model_exists = False
        try:
            ollama.show(model)
            model_exists = True
        except Exception:
            # Any error here (usually a 404) means download
            model_exists = False
          
        if not model_exists:
            self.result.emit(f"\nModel '{model}' not found locally.")
            self.result.emit("\nDownloading Now . . .")
            self.progress.emit(0)

            try:
                # Pull the model, streaming progress
                for event in ollama.pull(model, stream=True):
                    if 'completed' in event and 'total' in event:
                        completed = event['completed']
                        total = event['total']
                        if total > 0:
                            percent = (completed / total) * 100
                            self.progress.emit(int(percent))
                        elif 'status' in event:
                            self.result.emit(f"\n{event['status']}")
            except Exception as exc:
                self.result.emit(f"\nError during download: {exc}")

        self.progress.emit(0)
        graded_total = sum(len(v['homework']) + len(v['keys']) for v in self.paths.values())
        explained_total = sum(len(v['homework']) for v in self.paths.values()) + graded_total
        index = 0
            
        for name, files in self.paths.items():
            homework_list = []
            key_list = []
            wrong_answers = []
            question_count = []
            key_answers = []
            student_answers = []

            for hw_path in files['homework']:
                # Inference with the LLM
                output = inference.guirun(hw_path, self)
                # Parse the output
                while True:
                    try:
                        parsed = [item.split(":")[1].strip() for item in output.split(",")]
                        question_count.append(len(parsed))
                        break
                    except IndexError:
                        self.result.emit("Rerunning Prompt!")
                        output = inference.guirun(hw_path, self)
                homework_list.extend(parsed)
                student_answers.append(parsed)
                # Show the output in the GUI
                self.result.emit(f"\n{Path(hw_path).name}: {parsed}")
                index += 1
                if int(config.get("General", "Explain Incorrect Answers")) == 2:
                    self.progress.emit(int((index / explained_total) * 100))
                elif int(config.get("General", "Explain Incorrect Answers")) == 0:
                    self.progress.emit(int((index / graded_total) * 100))

            self.result.emit("\n")
            for key_path in files['keys']:
                # Inference with the LLM
                output = inference.guirun(key_path, self)
                # Parse the output
                while True:
                    try:
                        parsed = [item.split(":")[1].strip() for item in output.split(",")]
                        break
                    except IndexError:
                        self.result.emit("Rerunning Prompt!")
                        output = inference.guirun(key_path, self)
                key_answers.append(parsed)
                key_list.extend(parsed)
                # Show the output in the GUI
                self.result.emit(f"\n{Path(key_path).name}: {parsed}")
                index += 1
                if int(config.get("General", "Explain Incorrect Answers")) == 2:
                    self.progress.emit(int((index / explained_total) * 100))
                elif int(config.get("General", "Explain Incorrect Answers")) == 0:
                    self.progress.emit(int((index / graded_total) * 100))
            score = grade.run(homework_list, key_list)
            graded[name] = score[0]
            grades.append(score[0])
            wrong_answers = score[1]
            wrong_answers_final.append(wrong_answers)
            if int(config.get("General", "Explain Incorrect Answers")) == 2:
                explanations_output = (explain.run(self, files["homework"], wrong_answers, student_answers, key_answers, explained_total, index))
                explanations = explanations_output[0]
                index = explanations_output[1]
        self.finished.emit("All assignments graded.")
        # Add all grades in output box when finished
        for i in range(0, len(grades)):
            self.result.emit(f"\n{names_list[i]} → Grade: {grades[i]}%")
            self.result.emit(f"\nWrong Answers: {wrong_answers_final[i]}")
            if int(config.get("General", "Explain Incorrect Answers")) == 2:
                self.result.emit(f"\nExplanations: {explanations[i]}")
        # Enable and disable text boxes when the assignments are done grading
        self.export_btn_signal.emit(True)
        self.gui_state.emit(True)

# Class used to build settings menu
# Stores, saves, and loads settings file from 'config.ini'
# Change this path at the top of the script
class Settings(QDialog):
    def open_config(self):
        global config
        config = ConfigParser()

        # Create file if it doesn't exist
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                pass  # Just create an empty file

        # Load existing config
        config.read(path)

        # Add sections and options if missing
        if not config.has_section("General"):
            config.add_section("General")
        if not config.has_option("General", "Export Format"):
            config.set("General", "Export Format", "CSV")
        if not config.has_option("General", "Ollama Server"):
            config.set("General", "Ollama Server", "127.0.0.1:11434")
        if not config.has_option("General", "Explain Incorrect Answers"):
            config.set("General", "Explain Incorrect Answers", "0")
        if not config.has_option("General", "Model"):
            config.set("General", "Model", "qwen3-vl:8b")

        self.export_type.setCurrentText(config.get("General", "Export Format"))
        self.server_address.setText(config.get("General", "Ollama Server"))
        self.vision_model.setText(config.get("General", "Model"))
        if int(config.get("General", "Explain Incorrect Answers")) == 2:
            self.explain_answers.setChecked(True)
        elif int(config.get("General", "Explain Incorrect Answers")) == 0:
            self.explain_answers.setChecked(False)
        
        # Write back to file
        with open(path, "w", encoding="utf-8") as f:
            config.write(f)
        
    def save_config(self, section, key, value):
        config = ConfigParser()
        config.read(path)
        config.set(section, key, value)

        with open(path, "w", encoding="utf-8") as file:
            config.write(file)

    def reset_config(self):
        config = ConfigParser()
        config.read(path)
        config.set("General", "Export Format", "CSV")
        self.export_type.setCurrentText("CSV")
        config.set("General", "Ollama Server", "127.0.0.1:11434")
        self.server_address.setText("127.0.0.1:11434")
        config.set("General", "Explain Incorrect Answers", "False")
        self.explain_answers.setChecked(False)
        config.set("General", "Model", "qwen3-vl:8b")
        self.vision_model.setText("qwen3-vl:8b")

        with open(path, "w", encoding="utf-8") as file:
            config.write(file)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()

        self.export_type = QComboBox()
        self.export_type.addItems(export.types)
        export_label = QLabel("Export Format:")

        self.server_address = QLineEdit()
        server_address_label = QLabel("Ollama Server Address:")
        self.server_address.setPlaceholderText("127.0.0.1:11434")

        self.vision_model = QLineEdit()
        self.vision_model.setToolTip("Some models will work better than others, a vision model is required")
        vision_model_label = QLabel("Vision Model Used:")
        self.vision_model.setPlaceholderText("qwen3-vl:8b")

        self.explain_answers = QCheckBox()
        explain_answers_label = QLabel("Explain Incorrect Answers")

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)

        reset_btn = QPushButton("Reset Settings")
        reset_btn.clicked.connect(self.reset_config)

        export_layout = QHBoxLayout()
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.export_type)
        export_layout.addStretch()
        layout.addLayout(export_layout)

        server = QHBoxLayout()
        server.addWidget(server_address_label)
        server.addWidget(self.server_address)
        server.addStretch()
        layout.addLayout(server)

        model = QHBoxLayout()
        model.addWidget(vision_model_label)
        model.addWidget(self.vision_model)
        model.addStretch()
        layout.addLayout(model)

        explain_layout = QHBoxLayout()
        explain_layout.addWidget(explain_answers_label)
        explain_layout.addWidget(self.explain_answers)
        layout.addLayout(explain_layout)

        layout.addWidget(reset_btn)
        layout.addWidget(close_btn)

        self.setLayout(layout)
        
        self.export_type.currentTextChanged.connect(lambda value: self.save_config("General", "Export Format", value))
        self.server_address.textEdited.connect(lambda value: self.save_config("General", "Ollama Server", value))
        self.vision_model.textEdited.connect(lambda value: self.save_config("General", "Model", str(value)))
        self.explain_answers.stateChanged.connect(lambda value: self.save_config("General", "Explain Incorrect Answers", str(value)))
        self.open_config()

# Class used to build GUI
# Has events for button presses, etc
# Coordinates with the gradingworker class
class GradingApp(QWidget):
    # When new text is added, scroll to the bottom automatically
    def append_and_scroll(self, text):
        self.output_box.moveCursor(QTextCursor.MoveOperation.End)
        self.output_box.insertPlainText(text)
        self.output_box.verticalScrollBar().setValue(
            self.output_box.verticalScrollBar().maximum()
        )
    def __init__(self):
        super().__init__()
        self.settings = Settings
        # Set window title
        self.setWindowTitle("Assignment Grader")
        # Set default window size
        self.resize(700, 700)

        self.paths = {}  # {'Assignment Name': {'homework': [...], 'keys': [...]}}

        # Build GUI

        # Widgets
        self.label = QLabel("Enter assignment name and upload files:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Assignment name")

        self.pick_homework_btn = QPushButton("Add Homework Pages")
        self.pick_key_btn = QPushButton("Add Answer Key Pages")
        self.add_assignment_btn = QPushButton("Save Assignment")
        self.menu_btn = QPushButton("Settings")
        self.start_btn = QPushButton("Start Grading")
        self.export_btn = QPushButton("Export Data")
        self.export_btn.setEnabled(False)
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
        layout.addWidget(self.export_btn)
        layout.addWidget(self.menu_btn)

        self.setLayout(layout)

        # Temp storage for current assignment
        self.current_homework = []
        self.current_keys = []

        # Connect buttons
        self.pick_homework_btn.clicked.connect(self.add_homework)
        self.pick_key_btn.clicked.connect(self.add_keys)
        self.add_assignment_btn.clicked.connect(self.save_assignment)
        self.start_btn.clicked.connect(self.start_grading)
        self.export_btn.clicked.connect(self.export_grades)
        self.menu_btn.clicked.connect(self.show_menu)
        settings = Settings()
        settings.open_config()

    def show_menu(self):
        self.menu = Settings()
        self.menu.exec() 

    def add_homework(self):
        # File picker
        files, _ = QFileDialog.getOpenFileNames(self, "Select Homework Pages", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.current_homework.extend(files)
            self.label.setText(f"Homework pages selected: {len(self.current_homework)}")

    def add_keys(self):
        # File picker
        files, _ = QFileDialog.getOpenFileNames(self, "Select Answer Key Pages", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.current_keys.extend(files)
            self.label.setText(f"Key pages selected: {len(self.current_keys)}")

    def save_assignment(self):
        global names_list
        if 'names_list' not in globals():
            names_list = []
        name = self.name_input.text().strip()
        if not name:
            name = f"Assignment {len(self.paths) + 1}"
        names_list.append(name)
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

    def export_grades(self):
        config = ConfigParser()
        config.read(path)
        export_type = config.get("General", "Export Format")

        function_name = export_type.lower()

        self.output_box.append(f"\n {export_type} file exported.")
        getattr(export, f"to_{function_name}")(names_list, grades, wrong_answers_final, explanations)



    def toggle_export_btn(self, enabled):
        self.export_btn.setEnabled(enabled)

    def toggle_inputs(self, enabled):
        self.name_input.setEnabled(enabled)
        self.add_assignment_btn.setEnabled(enabled)
        self.pick_key_btn.setEnabled(enabled)
        self.pick_homework_btn.setEnabled(enabled)
        self.start_btn.setEnabled(enabled)

    def start_grading(self):
        self.output_box.append("\nGrading...\n")
        self.output_box.moveCursor(QTextCursor.MoveOperation.End)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.show()
        self.label.setText("Grading in progress...")

        # Listeners to listen for UI changes, and update the UI as needed
        self.worker = GradingWorker(self.paths)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.result.connect(self.append_and_scroll)
        self.worker.finished.connect(self.show_final_result)
        self.worker.gui_state.connect(self.toggle_inputs)
        self.worker.export_btn_signal.connect(self.toggle_export_btn)
        self.worker.start()


    def show_final_result(self, message):
        self.label.setText(message)
        self.progress_bar.hide()

if __name__ == "__main__":
    # Initialize program
    app = QApplication(sys.argv)
    window = GradingApp()
    window.show()
    sys.exit(app.exec())
