from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from Logic import GradeManager
import matplotlib.pyplot as plt

class MainWindow(QWidget):
    """Main application window for managing student grades."""

    def __init__(self):
        """Initialize the GUI components and load initial data."""
        super().__init__()
        self.setWindowTitle("Student Grades")
        self.resize(700, 500)

        # Create instance of logic manager
        self.grade_manager = GradeManager("students.csv")

        # Main layout for arranging widgets vertically
        layout = QVBoxLayout(self)

        # Setup the table to display student name, score, and letter grade
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Student Name", "Score", "Grade"])
        layout.addWidget(self.table)

        # Setup buttons
        button_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add Student")
        self.btn_calc = QPushButton("Calculate Grades")
        self.btn_clear = QPushButton("Clear All")
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_calc)
        button_layout.addWidget(self.btn_clear)
        layout.addLayout(button_layout)

        # Label for displaying statistics (avg, median, etc.)
        self.stats_label = QLabel("")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.stats_label)

        # Connect buttons to their respective event handlers
        self.btn_add.clicked.connect(self.add_student)
        self.btn_calc.clicked.connect(self.calculate_grades)
        self.btn_clear.clicked.connect(self.clear_all)

        # Load existing data from CSV into the table
        self.load_data()

    def load_data(self):
        """Load existing student data from the CSV file into the table."""
        for name, score, grade in self.grade_manager.load_data():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(score))
            self.table.setItem(row, 2, QTableWidgetItem(grade))

    def add_student(self):
        """Add a new empty row to the table for entering student information."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem(""))

    def calculate_grades(self):
        """
        Validate input, calculate letter grades, update table and CSV,
        and display statistics and distribution chart.
        """
        scores = []
        valid_data = []
        grades = []

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            score_item = self.table.item(row, 1)

            name = name_item.text().strip() if name_item else ""
            score_text = score_item.text().strip() if score_item else ""

            # Reset cell styles and tooltips
            name_item.setBackground(QColor("white"))
            score_item.setBackground(QColor("white"))
            name_item.setToolTip("")
            score_item.setToolTip("")

            # Validate student name
            if not self.grade_manager.is_valid_name(name):
                name_item.setBackground(QColor("red"))
                name_item.setToolTip("Invalid name (must contain letters only)")
                continue

            # Validate score
            if not self.grade_manager.is_valid_score(score_text):
                score_item.setBackground(QColor("red"))
                score_item.setToolTip("Invalid score (0–100 expected)")
                continue

            # Process valid input
            score = float(score_text)
            grade = self.grade_manager.get_letter_grade(score)

            # Update grade column
            self.table.setItem(row, 2, QTableWidgetItem(grade))

            # Track valid data
            scores.append(score)
            grades.append(grade)
            valid_data.append((name, score_text, grade))

        # Save valid data to CSV and update statistics and chart
        self.grade_manager.save_data(valid_data)
        self.stats_label.setText(self.grade_manager.compute_statistics(scores))
        self.grade_manager.show_distribution(grades)

    def clear_all(self):
        """Clear the table and reset the CSV file and stats label."""
        self.table.setRowCount(0)
        self.grade_manager.clear_data()
        self.stats_label.setText("")
