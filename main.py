import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QAction, QLineEdit, QStyledItemDelegate, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QRegularExpressionValidator
from PyQt5.QtCore import Qt, QRegularExpression

class NumberDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.validator = QIntValidator()

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(self.validator)
        return editor

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

class NumberTableWidgetItem(QTableWidgetItem):
    def __init__(self, text=''):
        super().__init__(text)

    def setData(self, role, value):
        if role == Qt.EditRole and value:
            try:
                int(value)
            except ValueError:
                return
        super().setData(role, value)

class StudyMateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudyMate")
        self.setWindowIcon(QIcon('rasm.png'))
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        # Create main widget and layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Create GCD and LCM Calculator section
        self.gcdLabel = QLabel("Calculates the Greatest Common Divisor and Least Common Multiple of two or more numbers.")
        self.gcdLabel.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        self.layout.addWidget(self.gcdLabel)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['Integer'])
        self.tableWidget.setRowCount(2)
        self.tableWidget.setItem(0, 0, NumberTableWidgetItem(""))
        self.tableWidget.setItem(1, 0, NumberTableWidgetItem(""))
        self.tableWidget.resizeColumnsToContents()
        self.layout.addWidget(self.tableWidget)

        self.addButton = QPushButton("+")
        self.addButton.setFixedWidth(30)
        self.addButton.setStyleSheet("QPushButton { background-color: #99ccff; color: white; font-weight: bold; font-size: 16px; border-radius: 5px; } QPushButton:hover { background-color: #66a3ff; }")
        self.removeButton = QPushButton("-")
        self.removeButton.setFixedWidth(30)
        self.removeButton.setStyleSheet("QPushButton { background-color: #ff8080; color: white; font-weight: bold; font-size: 16px; border-radius: 5px; } QPushButton:hover { background-color: #ff6666; }")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        self.layout.addLayout(buttonLayout)

        self.clearButton = QPushButton("Clear")
        self.executeButton = QPushButton("Execute")
        self.clearButton.setStyleSheet("QPushButton { background-color: #ff9999; color: white; font-weight: bold; font-size: 14px; border-radius: 5px; } QPushButton:hover { background-color: #ff6666; }")
        self.executeButton.setStyleSheet("QPushButton { background-color: #99ff99; color: white; font-weight: bold; font-size: 14px; border-radius: 5px; } QPushButton:hover { background-color: #66cc66; }")
        self.layout.addWidget(self.clearButton)
        self.layout.addWidget(self.executeButton)

        self.gcdResultLabel = QLabel("GCD:")
        self.gcdResultLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.lcmResultLabel = QLabel("LCM:")
        self.lcmResultLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.gcdResultLabel)
        self.layout.addWidget(self.lcmResultLabel)

        # Connect button signals to slots
        self.addButton.clicked.connect(self.addRow)
        self.removeButton.clicked.connect(self.removeRow)
        self.clearButton.clicked.connect(self.clearTable)
        self.executeButton.clicked.connect(self.calculateGcdLcm)

        # Set custom delegate for the table
        delegate = NumberDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)

    def addRow(self):
        row_count = self.tableWidget.rowCount()
        if row_count < 20:
            self.tableWidget.insertRow(row_count)

    def removeRow(self):
        row_count = self.tableWidget.rowCount()
        if row_count > 2:
            self.tableWidget.removeRow(row_count - 1)

    def clearTable(self):
        row_count = self.tableWidget.rowCount()
        for row in range(row_count):
            self.tableWidget.setItem(row, 0, NumberTableWidgetItem(""))
    def clearZeros(self):
        row_count = self.tableWidget.rowCount()
        for row in range(row_count):
            item = self.tableWidget.item(row, 0)
            if item is not None:
                int_text = item.text()
                if int_text:
                    integer = int(int_text)
                    if integer == 0:
                        self.tableWidget.setItem(row, 0, NumberTableWidgetItem(""))
    def calculateGcdLcm(self):
        row_count = self.tableWidget.rowCount()
        integers = []
        for row in range(row_count):
            item = self.tableWidget.item(row, 0)
            if item is not None:
                integer_text = item.text()
                if integer_text:
                    integer = int(integer_text)
                    if integer == 0:
                        QMessageBox.warning(self, "Error", "Can't be zero!")
                        self.clearZeros()
                        return
                    integers.append(integer)

        if integers:
            gcd = self.calculateGcd(integers)
            lcm = self.calculateLcm(integers)
            self.gcdResultLabel.setText(f"GCD: {gcd}")
            self.lcmResultLabel.setText(f"LCM: {lcm}")
        else:
            self.gcdResultLabel.setText("GCD:")
            self.lcmResultLabel.setText("LCM:")

    def calculateGcd(self, numbers):
        # Calculate the Greatest Common Divisor (GCD) using Euclidean algorithm
        a = numbers[0]
        b = numbers[1]
        while b != 0:
            a, b = b, a % b
        gcd = a
        for i in range(2, len(numbers)):
            gcd = self.calculateGcd([gcd, numbers[i]])
        return gcd

    def calculateLcm(self, numbers):
        # Calculate the Least Common Multiple (LCM) using GCD
        lcm = numbers[0]
        for i in range(1, len(numbers)):
            gcd = self.calculateGcd([lcm, numbers[i]])
            lcm = lcm * numbers[i] // gcd
        return lcm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyMateApp()
    window.show()
    sys.exit(app.exec_())
