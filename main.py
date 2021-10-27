import sys
from functools import partial

import database
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *

class To_Do_List(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load('To Do.ui', None)
        self.ui.show()

        self.ui.btn_add.clicked.connect(self.addNewTaskToDatabase)
        

        self.readFromDatabase()

    def deleteTasksFromDatabase(self,checkbox, label, delete, title):
        database.delete(title)
        checkbox.deleteLater()
        label.deleteLater()
        delete.deleteLater()

    def doneTasksInDatabase(self, check, title):
        if check.isChecked():
            database.update(1, title)
        else:
            database.update(0, title)
        self.readFromDatabase()

    def addNewTaskToDatabase(self):
        results = database.getAll()
        id = len(results)
        title = self.ui.tb_title.text()
        description = self.ui.tb_description.text()
        time = self.ui.tb_time.text()
        date = self.ui.tb_date.text()
        database.add(id, title, description, time, date)

        self.readFromDatabase()
        self.ui.tb_title.setText('')
        self.ui.tb_description.setText('') 
        self.ui.tb_time.setText('')
        self.ui.tb_date.setText('')       

    def readFromDatabase(self):
        results = database.getAll()

        for i in range(len(results)):
            new_checkbox = QCheckBox()
            new_checkbox.clicked.connect(partial(self.doneTasksInDatabase, new_checkbox, results[i][1]))
            if results[i][3] == 1:
                new_checkbox.setChecked(True)

            new_label = QLabel()
            new_label.setText(results[i][1])

            new_delete_button = QPushButton()
            new_delete_button.setText('❌')
            new_delete_button.clicked.connect(partial(self.deleteTasksFromDatabase,new_checkbox, new_label, new_delete_button, results[i][1]))

            self.ui.gridLayout.addWidget(new_checkbox, i, 0)
            self.ui.gridLayout.addWidget(new_label, i, 1)
            self.ui.gridLayout.addWidget(new_delete_button, i, 2)

app = QApplication(sys.argv)
window = To_Do_List()
app.exec()