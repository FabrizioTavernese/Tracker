
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from package.DataManager import DataManager
from package.list_functions import show_list
class MainWindow(QWidget):
    '''
    The class of the Main Window of the application, with all of his
    variables and methods.
    '''

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tracker")
        self.data = DataManager()

        ## Label

        label = QLabel("Horas ")
        self.line_edit = QLineEdit()

        h_layout_label = QHBoxLayout()
        h_layout_label.addWidget(label)
        h_layout_label.addWidget(self.line_edit)

        ## Button

        button_add = QPushButton("Add")
        button_edit = QPushButton("Edit")
        button_delete = QPushButton("Delete")
        button_view = QPushButton("View")

        button_add.clicked.connect(self.button_add_pressed)
        button_edit.clicked.connect(self.button_edit_pressed)
        button_delete.clicked.connect(self.button_delete_pressed)
        button_view.clicked.connect(self.button_view_pressed)
        

        h_layout_button = QHBoxLayout()
        h_layout_button.addWidget(button_add)
        h_layout_button.addWidget(button_edit)
        h_layout_button.addWidget(button_delete)
        h_layout_button.addWidget(button_view)

        layout = QVBoxLayout()

        layout.addLayout(h_layout_label)
        layout.addLayout(h_layout_button)

        self.setLayout(layout)


    # Slots

    def button_add_pressed(self):
        
        if self.line_edit.text().isdigit():
            # the text of the line edit is given
            text = int(self.line_edit.text())
            record = self.data.add(text)
            print("Saved", record)
        else:
            print("Please enter a valid entry")


    def button_edit_pressed(self):
        self.data.edit()


    def button_delete_pressed(self):
        record = self.data.delete_last()
        if record:
            print("Last records deleted succesfully", record)
        else:
            print("There is no record to delete")


    def button_view_pressed(self):
        records = self.data.get_all()
        print("All the records: ")
        show_list(records)