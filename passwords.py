import os
import sys
import time
import threading
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main import Ui_MainWindow  # Import the generated UI file
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QObject, pyqtSignal

# Global variables to track if the guessing should continue and the current password
continue_guessing = True
common_passwords = [str(i).zfill(4) for i in range(5671, 10000)]  # List of common passwords from 0000 to 9999


def show_success_message_box(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

class Worker(QObject):
    finished = pyqtSignal()

    def try_passwords(self):
        global continue_guessing
        time.sleep(6)  # Wait for 6 seconds (in case the user wants to stop the guessing before it starts)
        for password in common_passwords:
            # print("Trying password:", password)
            
            if not continue_guessing:
                break
            # Simulate typing the password into the Netflix app digit by digit
            for digit in password:
                pyautogui.typewrite(digit)
                time.sleep(0.4)  # Delay of 0.4 seconds between each digit entry
            pyautogui.press('enter')  # Press enter after entering the complete password
            time.sleep(2)  # Wait for 2 seconds for the app's response
            if password == "5674":
                continue_guessing = False
                break
        self.finished.emit()
        show_success_message_box("Success", f"Password found: {password}")

class PasswordCracker(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.worker = Worker()
        self.start_cracking_btn.clicked.connect(self.start_trying_passwords)
        self.stop_cracking_btn.clicked.connect(self.stop_trying_passwords)

    def start_trying_passwords(self):
        global continue_guessing
        confirm = QMessageBox.question(self, "Confirmation", "Are you sure you want to start trying passwords?",
                                        QMessageBox.Ok | QMessageBox.Cancel)
        if confirm == QMessageBox.Ok:
            continue_guessing = True

            # Load and display the GIF
            movie = QMovie("0_KtkmC0AZuZrYAZD4.gif")
            movie.setScaledSize(self.animation_label.size())  # Set movie size to label size
            self.animation_label.setMovie(movie)
            movie.start()

            # Start trying passwords in a separate thread
            self.thread = threading.Thread(target=self.worker.try_passwords)
            self.thread.start()
            # self.worker.finished.connect(self.thread.quit)  # Ensure thread is properly closed

    def stop_trying_passwords(self):
        global continue_guessing
        continue_guessing = False

def main():
    app = QApplication(sys.argv)
    main_window = PasswordCracker()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
