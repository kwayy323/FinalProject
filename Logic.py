import csv
import os
import re
from statistics import mean, median
import matplotlib.pyplot as plt


class GradeManager:
    """
    A class to manage student grade data, including reading/writing CSV files,
    calculating grades, validating input, computing statistics, and displaying charts.
    """

    def __init__(self, csv_file: str):
        """
        Initialize the GradeManager with a CSV file.
        If the file doesn't exist, create an empty one.

        :param csv_file: Path to the CSV file used for storing student data.
        """
        self.csv_file = csv_file
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                pass  # Create an empty file if it doesn't exist

    def load_data(self) -> list[tuple[str, str, str]]:
        """
        Load student data from the CSV file.

        :return: List of tuples in the format (name, score, grade).
        """
        data = []
        with open(self.csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    data.append((row[0], row[1], row[2]))  # Full row
                elif len(row) == 2:
                    data.append((row[0], row[1], ""))  # Missing grade
        return data

    def save_data(self, data: list[tuple[str, str, str]]) -> None:
        """
        Save student data (name, score, grade) to the CSV file.

        :param data: List of tuples containing student name, score, and letter grade.
        """
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def clear_data(self) -> None:
        """
        Clear the contents of the CSV file.
        """
        with open(self.csv_file, 'w', newline='') as f:
            pass  # Empty the file

    def calculate_grades(self, scores: list[float]) -> list[str]:
        """
        Convert a list of numeric scores into letter grades.

        :param scores: List of numerical scores (float).
        :return: List of corresponding letter grades.
        """
        return [self.get_letter_grade(score) for score in scores]

    def get_letter_grade(self, score: float) -> str:
        """
        Convert a numeric score into a letter grade.

        :param score: A numeric grade between 0 and 100.
        :return: Letter grade as a string (A, B, C, D, F).
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def compute_statistics(self, scores: list[float]) -> str:
        """
        Compute basic statistics from the score list.

        :param scores: List of numeric scores.
        :return: A formatted string with average, median, high, and low values.
        """
        if not scores:
            return "No valid scores to calculate."
        avg = mean(scores)
        med = median(scores)
        return (f"📊 Stats — Count: {len(scores)}, "
                f"Avg: {avg:.2f}, Med: {med:.2f}, "
                f"High: {max(scores):.2f}, Low: {min(scores):.2f}")

    def show_distribution(self, grades: list[str]) -> None:
        """
        Display a bar chart showing distribution of letter grades.

        :param grades: List of letter grades (A–F).
        """
        from collections import Counter
        grade_counts = Counter(grades)  # Count how many of each grade
        categories = ["A", "B", "C", "D", "F"]
        counts = [grade_counts.get(g, 0) for g in categories]

        # Create and display the bar chart
        plt.figure("Grade Distribution")
        plt.bar(categories, counts, color="skyblue")
        plt.title("Grade Distribution")
        plt.xlabel("Letter Grade")
        plt.ylabel("Number of Students")
        plt.tight_layout()
        plt.show()

    def is_valid_name(self, name: str) -> bool:
        """
        Validate that the name contains only letters and spaces.

        :param name: Student name input.
        :return: True if valid, False otherwise.
        """
        return bool(re.fullmatch(r"[A-Za-z\s]+", name))

    def is_valid_score(self, score: str) -> bool:
        """
        Validate that the score is a number between 0 and 100.

        :param score: Score input as a string.
        :return: True if score is valid, False otherwise.
        """
        try:
            val = float(score)
            return 0 <= val <= 100
        except ValueError:
            return False

