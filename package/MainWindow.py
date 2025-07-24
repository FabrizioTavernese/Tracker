
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QListWidget, QListWidgetItem
from package.DataManager import DataManager
from package.list_functions import show_list


class MainWindow(QWidget):
    '''
    The class of the Main Window of the application, with all of his
    variables and methods.
    Handles the interface and presentation logic.
    '''

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tracker")
        self.setFixedSize(300, 145)
        self.data = DataManager()
        self.stack = QStackedWidget()
        self.main_view = QWidget()
        self.delete_view = QWidget()
        self.edit_view = QWidget()

        self.list_widget = QListWidget()
        self.list_widget.setMinimumSize(100, 90)

        # Unique and dinamic container
        self.list_container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.list_container.setLayout(layout)

        self.setup_ui()
        self.refresh_list_widget()


    def setup_ui(self):

        ## Label
        label = QLabel("Horas ")
        self.line_edit = QLineEdit()

        h_layout_label = QHBoxLayout()
        h_layout_label.addWidget(label)
        h_layout_label.addWidget(self.line_edit)

        ## Layouts and buttons

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

        # main_view_layout have the label and the buttons
        main_view_layout = QVBoxLayout()
        main_view_layout.addLayout(h_layout_label)
        main_view_layout.addLayout(h_layout_button)

        # main_view (widget) have main_view_layout as layout 
        self.main_view.setLayout(main_view_layout)

        # main_view is setted up as a widget of the stack
        self.stack.addWidget(self.main_view)

        # finally, a main_layout with stack as widget is the one which is showed with self.
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)



        ######################## DELETE VIEW ##################################
        
        self.delete_layout = QHBoxLayout()

        # Buttons of the delete view

        button_delete_selected = QPushButton("Delete")
        button_delete_selected.clicked.connect(self.button_delete_selected_record)

        button_back_delete = QPushButton("Back")
        button_back_delete.clicked.connect(self.button_back_pressed)

        button_container_delete = QVBoxLayout()
        button_container_delete.addWidget(button_back_delete)
        button_container_delete.addWidget(button_delete_selected)

        self.delete_layout.addLayout(button_container_delete)

        # the layout of the delete view is established
        self.delete_view.setLayout(self.delete_layout)

        # delete view is added to the stacks
        self.stack.addWidget(self.delete_view)  

        ########################## EDIT VIEW ###################################

        self.edit_layout = QHBoxLayout()

        button_edit_selected = QPushButton("Edit")
        button_edit_selected.clicked.connect(self.button_edit_pressed)

        button_back_edit = QPushButton("Back")
        button_back_edit.clicked.connect(self.button_back_pressed)

        button_container_edit = QVBoxLayout()

        button_container_edit.addWidget(button_back_edit)
        button_container_edit.addWidget(button_edit_selected)

        self.edit_layout.addLayout(button_container_edit)
        self.edit_view.setLayout(self.edit_layout)
        self.stack.addWidget(self.edit_view)


    # METHODS

    # Rebuilds the entire list from scratch with updated data
    def refresh_list_widget(self):
        self.list_widget.clear()                                    # 1. Clear all the visual list
        for record in self.data.records:                            # 2. Run all the records in DataManager
            item_text = f"{record['hours']} hrs - {record['date']}" # 3. Give format to the text
            self.list_widget.addItem(QListWidgetItem(item_text))    # 4. Add every record to the visual list


    def button_add_pressed(self):
        if self.line_edit.text().isdigit():
            # the text of the line edit is given
            text = int(self.line_edit.text())
            record = self.data.add(text)
            item_text = f"{record['hours']} hrs - {record['date']}"
            self.list_widget.addItem(QListWidgetItem(item_text))    # Add only the new record
            self.line_edit.clear()  
        else:
            print("Please enter a valid entry")


    def button_delete_pressed(self):
        self.delete_layout.insertWidget(0, self.list_container)
        self.stack.setCurrentWidget(self.delete_view)

    def button_delete_selected_record(self):
        # 1. Gets all selected items from the visual list
        selected_items = self.list_widget.selectedItems()

        if not selected_items:       # 2. If there's no selection, ends
            print("No item selected")
            return 
        
        # 3. For every selected items
        for item in selected_items:
            text = item.text()  # Gets the text of the item (e.i: "5 hrs - 25/07/2023")

            # 4. Find the corresponding record in the data
            for record in self.data.records:
                expected_text = f"{record['hours']} hrs - {record['date']}"

                # 5. If they match
                if text == expected_text:

                    #6. Deletes the record from the backend (DataManager)
                    self.data.delete_record(record)

                    # 7. Deletes the item from the visual list (QMainWindow)
                    self.list_widget.takeItem(self.list_widget.row(item))
                    break   #8. Ends the loop for this item 

    def button_edit_pressed(self):
        self.edit_layout.insertWidget(0, self.list_container)
        self.stack.setCurrentWidget(self.edit_view)

    def button_view_pressed(self):
        records = self.data.get_all()
        print("All the records: ")
        show_list(records)

    def button_back_pressed(self):
        self.clear_list_container()  # Clears before change the view
        self.stack.setCurrentWidget(self.main_view)

    def clear_list_container(self):
        if self.list_container.parent():
            old_layout = self.list_container.parent().layout()
            old_layout.removeWidget(self.list_container)