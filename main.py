import json

from PyQt5 import QtWidgets

from app.ai.enums.subject import Subject
from app.ai.questionGenerator import QuestionGenerator


class TopicFrame(QtWidgets.QWidget):
    def __init__(self, remove_callback):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout(self)
        self.entry = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.entry)
        self.remove_btn = QtWidgets.QPushButton("X", self)
        self.remove_btn.clicked.connect(lambda: remove_callback(self))
        self.layout.addWidget(self.remove_btn)


class QuizQuestionGenerator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.genAi = QuestionGenerator()
        self.topic_frames = []
        self.num_questions_input = None
        self.subject_combo = None
        self.topics_container = None
        self.age_group_input = None
        self.generate_button = None
        self.result_label = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Quiz Question Generator")
        self.setGeometry(100, 100, 800, 600)  # Window size

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)  # Spacing between widgets

        self.num_questions_input = QtWidgets.QLineEdit(self)
        self.num_questions_input.setPlaceholderText("Number of questions (1-5)")
        layout.addWidget(self.num_questions_input)

        self.subject_combo = QtWidgets.QComboBox(self)
        self.subject_combo.addItems([s.name for s in Subject])
        self.subject_combo.setFixedWidth(500)  # Set fixed width for the combo box
        layout.addWidget(self.subject_combo)

        self.topics_container = QtWidgets.QVBoxLayout()
        layout.addLayout(self.topics_container)

        add_topic_btn = QtWidgets.QPushButton("Add Topic", self)
        add_topic_btn.clicked.connect(self.add_topic_field)
        layout.addWidget(add_topic_btn)

        self.age_group_input = QtWidgets.QLineEdit(self)
        self.age_group_input.setPlaceholderText("Age Group")
        layout.addWidget(self.age_group_input)

        self.generate_button = QtWidgets.QPushButton("Generate Questions", self)
        self.generate_button.clicked.connect(self.generate_questions)
        layout.addWidget(self.generate_button)

        self.result_label = QtWidgets.QLabel("", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # UI Enhancements for a tech-style look
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;  /* Dark background */
                font-family: 'Segoe UI', sans-serif;  /* Modern font */
                color: #ffffff;  /* White text */
            }
            QComboBox, QLineEdit {
                padding: 15px;
                border: 1px solid #444;
                border-radius: 5px;
                font-size: 16px;
                background-color: #3c3c3c;  /* Darker input field */
                color: #ffffff;  /* White text */
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 15px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;  /* Darker blue on hover */
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);  /* Shadow effect */
            }
            QLabel {
                font-size: 16px;
                color: #ffffff;  /* White text */
            }
        """)

    def add_topic_field(self):
        frame = TopicFrame(self.remove_topic_field)
        self.topic_frames.append(frame)
        self.topics_container.addWidget(frame)

    def remove_topic_field(self, frame):
        frame.deleteLater()
        self.topic_frames.remove(frame)

    def generate_questions(self):
        try:
            number = int(self.num_questions_input.text())
            if number < 1 or number > 5:
                raise ValueError("Number out of range")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Error", "Please enter a number between 1 and 5.")
            return

        try:
            subject = Subject(self.subject_combo.currentText())
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Error", "Please enter a valid subject.")
            return

        topics = [frame.entry.text().strip() for frame in self.topic_frames if frame.entry.text().strip()]
        age_group = self.age_group_input.text()

        if not age_group:
            QtWidgets.QMessageBox.critical(self, "Error", "Age Group cannot be empty.")
            return

        self.result_label.setText("Generating questions...\nIt may take a minute to generate quiz questions.")
        QtWidgets.QApplication.processEvents()

        all_questions = []
        try:
            if topics:
                for topic in topics:
                    questions = self.genAi.generateQuestions(number, subject, age_group, topic)
                    all_questions.extend(questions)
            else:
                questions = self.genAi.generateQuestions(number, subject, age_group)
                all_questions.extend(questions)
            self.result_label.setText("Finished generating questions!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            return

        with open("output.json", "w") as file:
            file.write(json.dumps([question.__dict__ for question in all_questions], indent=4))

        QtWidgets.QMessageBox.information(self, "Success", "Questions generated and saved to output.json!")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QuizQuestionGenerator()
    window.show()
    sys.exit(app.exec_())
