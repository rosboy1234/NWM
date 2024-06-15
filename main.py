import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore, QtWidgets
import math

style_circle = """
QPushButton {
    background-color: #00008B; /* Dark blue color */
    color: white;
    border: none;
    border-radius: 45px; /* Make the border-radius half of the button height to achieve a full circle */
    padding: 10px;
}
QPushButton:hover {
    background-color: #1E90FF; /* Lighter shade of blue on hover */
    border-radius: 45px; /* Match the border radius */
    padding: 10px;
}
"""

style_default = """
QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 15px; /* Adjust the radius as per your preference */
    padding: 10px; /* Add padding to make buttons slightly larger */
}
QPushButton:hover {
    background-color: #0056b3;
    border-radius: 15px; /* Match the border radius and padding */
    padding: 10px; /* Match the padding */
}
"""

class Ui_MainWindow(QtWidgets.QMainWindow):
    fontname = "SF Pro"

    def hoverEnterEvent(self, button):
        if button.text() in ["%", "!", "/", "+", "-", "=", "(", ")", "*", "^", "√", "ClrScr"]:
            button.setStyleSheet("background-color: #1E90FF; color: white; border-radius: 45px; padding: 10px;")
        else:
            button.setStyleSheet("background-color: #00008B; color: white; border-radius: 15px; padding: 10px;")

    def hoverLeaveEvent(self, button):
        if button.text() in ["%", "!", "/", "+", "-", "=", "(", ")", "*", "^", "√", "ClrScr"]:
            button.setStyleSheet("background-color: #00008B; color: white; border: none; border-radius: 45px; padding: 10px;")
        else:
            button.setStyleSheet("background-color: #007bff; color: white; border: none; border-radius: 15px; padding: 10px;")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Calculator")
        MainWindow.setFixedSize(550, 680)
        font = QtGui.QFont(self.fontname)
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: black;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFixedSize(500, 90)
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 5)
        self.lineEdit.setStyleSheet("color: white;")

        button_texts = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", "00", ".", "+",
            "(", ")", "ClrScr", "=",
            "%", "√", "^", "!"  # Added exponentiation and factorial buttons
        ]

        positions = [(i // 4 + 1, i % 4) for i in range(len(button_texts))]

        self.buttons = []
        for text, pos in zip(button_texts, positions):
            button = QtWidgets.QPushButton(text, self.centralwidget)
            button.setFont(font)
            button.setObjectName(f"pushButton_{text}")
            button.setFixedSize(120, 90)
            if text in ["%", "!", "/", "+", "-", "=", "(", ")", "*", "^", "√", "ClrScr"]:
                button.setStyleSheet(style_circle)
            else:
                button.setStyleSheet(style_default)
            button.clicked.connect(lambda checked, text=text: self.button_clicked(text))
            button.enterEvent = lambda event, button=button: self.hoverEnterEvent(button)
            button.leaveEvent = lambda event, button=button: self.hoverLeaveEvent(button)
            self.gridLayout.addWidget(button, *pos)
            self.buttons.append(button)
            
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Keyboard shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), MainWindow, self.calculate)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), MainWindow, self.calculate)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Equal), MainWindow, self.calculate)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculator"))
        for i, text in enumerate([
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", "00", ".", "+",
            "(", ")", "ClrScr", "=",
            "%", "√", "^", "!"  # Updated button texts
        ]):
            self.buttons[i].setText(_translate("MainWindow", text))

    def evaluateExp(self, expression):
        try:
            result = eval(expression)
        except (ValueError, SyntaxError, ArithmeticError):
            result = "Error"
        return result

    def button_clicked(self, text):
        if text == "ClrScr":
            self.clear()
        elif text == "=":
            self.calculate()
        elif text == "%":
            self.calculatePercentage()
        elif text == "√":
            self.calculateSquareRoot()
        elif text == "^":
            self.lineEdit.setText(self.lineEdit.text() + "**")
        elif text == "!":
            self.calculateFactorial()
        else:
            self.lineEdit.setText(self.lineEdit.text() + text)

    def clear(self):
        self.lineEdit.setText('')

    def calculate(self):
        exp = self.lineEdit.text()
        res = str(self.evaluateExp(exp))
        self.lineEdit.setText(res)

    def calculatePercentage(self):
        try:
            expression = self.lineEdit.text()
            result = eval(expression) / 100.0
            self.lineEdit.setText(str(result))
        except (ValueError, SyntaxError, ArithmeticError):
            self.lineEdit.setText("Error")

    def calculateSquareRoot(self):
        try:
            expression = self.lineEdit.text()
            result = math.sqrt(eval(expression))
            self.lineEdit.setText(str(result))
        except (ValueError, SyntaxError, ArithmeticError):
            self.lineEdit.setText("Error")

    def calculateFactorial(self):
        try:
            n = int(self.lineEdit.text())
            result = math.factorial(n)
            self.lineEdit.setText(str(result))
        except (ValueError, TypeError, ValueError):
            self.lineEdit.setText("Error")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle("Calculator")
    MainWindow.show()
    sys.exit(app.exec_())
