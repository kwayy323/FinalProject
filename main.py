import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow


def main() -> None:
    """
    Entry point for the Student Grades application.

    This function initializes the Qt application, creates the main window,
    displays it, and starts the event loop.
    """
    # Create a QApplication object to manage application-wide resources
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the Qt event loop and exit when it's done
    sys.exit(app.exec())


if __name__ == '__main__':
    # Run the main function only if this script is executed directly
    main()
