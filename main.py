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

    def info(self, description, time, date):
        msgBox = QMessageBox()
        msgBox.setText(description+ ' , '+ time+ ' , '+ date)
        msgBox.exec()

    def priority(self, prio, title):
        if prio == 0:
            database.update_priority(1, title)
        elif prio == 1:
            database.update_priority(0, title)
        self.readFromDatabase()

    def deleteTasksFromDatabase(self,checkbox, label, delete, title, info, prio):
        database.delete(title)
        checkbox.deleteLater()
        label.deleteLater()
        delete.deleteLater()
        info.deleteLater()
        prio.deleteLater()

    def doneTasksInDatabase(self, check, label, delete, title, info, prio):
        if check.isChecked():
            database.update(1, title)
        else:
            database.update(0, title)
        check.deleteLater()
        label.deleteLater()
        delete.deleteLater()
        info.deleteLater()
        prio.deleteLater()
        self.readFromDatabase()

    def addNewTaskToDatabase(self):
        results = database.getAll()
        id = len(results) + 1
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
            new_label = QLabel()
            new_info_button = QPushButton()
            new_delete_button = QPushButton()
            new_priority_button = QPushButton()

            new_label.setText(results[i][1])
            new_delete_button.setText('❌')
            new_info_button.setText('🗯')
            if results[i][3] == 1:
                new_checkbox.setChecked(True)
            if results[i][6] == 0:
                new_priority_button.setText('❕')
                new_label.setStyleSheet('background-color: rgb(240, 240, 240);font: 700 9pt "Segoe UI"')
            elif results[i][6] == 1:
                new_priority_button.setText('❗')
                new_label.setStyleSheet('background-color: red;font: 700 9pt "Segoe UI"')

            new_checkbox.setStyleSheet('max-width: 30px; min-height: 30px')
            new_delete_button.setStyleSheet('background-color: pink;max-width: 35px; min-height: 30px; font: 700 9pt "Segoe UI";')
            new_priority_button.setStyleSheet('background-color: purple;max-width: 35px; min-height: 30px;font: 700 9pt "Segoe UI";')
            new_info_button.setStyleSheet('background-color: rgb(222, 0, 111);max-width: 35px; min-height: 30px;font: 700 9pt "Segoe UI";')

            new_checkbox.clicked.connect(partial(self.doneTasksInDatabase, new_checkbox, new_label, new_delete_button, results[i][1], new_info_button, new_priority_button))
            new_delete_button.clicked.connect(partial(self.deleteTasksFromDatabase,new_checkbox, new_label, new_delete_button, results[i][1], new_info_button, new_priority_button))
            new_priority_button.clicked.connect(partial(self.priority, results[i][6], results[i][1]))
            new_info_button.clicked.connect(partial(self.info, results[i][2], results[i][4], results[i][5]))


            if results[i][3] == 0 :
                self.ui.gridLayout.addWidget(new_checkbox, i, 0)
                self.ui.gridLayout.addWidget(new_label, i, 1)
                self.ui.gridLayout.addWidget(new_priority_button, i, 2)
                self.ui.gridLayout.addWidget(new_info_button, i, 3)
                self.ui.gridLayout.addWidget(new_delete_button, i, 4)

            elif results[i][3] == 1:
                self.ui.gridLayout1.addWidget(new_checkbox, i, 0)
                self.ui.gridLayout1.addWidget(new_label, i, 1)
                self.ui.gridLayout1.addWidget(new_priority_button, i, 2)
                self.ui.gridLayout1.addWidget(new_info_button, i, 3)
                self.ui.gridLayout1.addWidget(new_delete_button, i, 4)

app = QApplication(sys.argv)
window = To_Do_List()
app.exec()