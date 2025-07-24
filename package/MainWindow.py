
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
        self.data = DataManager()
        self.stack = QStackedWidget()
        self.main_view = QWidget()
        self.delete_view = QWidget()

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


        # Delete view
        
        self.delete_layout = QVBoxLayout()
        self.list_widget = QListWidget()    # to store the records as items
        self.list_widget.setMinimumSize(300, 200)
        self.delete_layout.addWidget(self.list_widget)

        # Buttons of the delete view

        button_delete_this = QPushButton("Delete")
        button_delete_this.clicked.connect(self.button_delete_selected_record)
        buton_back = QPushButton("Back")
        buton_back.clicked.connect(self.button_back_pressed)

        button_container = QHBoxLayout()
        button_container.addWidget(buton_back)
        button_container.addWidget(button_delete_this)
        self.delete_layout.addLayout(button_container)

        # the layout of the delete view is established
        self.delete_view.setLayout(self.delete_layout)

        # delete view is added to the stacks
        self.stack.addWidget(self.delete_view)  

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
        # Changes the curren widget (main_view) to the delete_view
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

    def button_back_pressed(self):
        self.stack.setCurrentWidget(self.main_view)

    def button_view_pressed(self):
        records = self.data.get_all()
        print("All the records: ")
        show_list(records)

    def button_edit_pressed(self):
        self.data.edit()
