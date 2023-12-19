from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox
from interface import Ui_Form
import sys
import json
from PyQt6.QtCore import Qt, QIODevice

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_note_create.clicked.connect(self.add_note)
        self.list_notes.itemClicked.connect(self.show_note)
        self.button_note_save.clicked.connect(self.save_note)
        self.button_note_del.clicked.connect(self.del_note)
        self.button_tag_add.clicked.connect(Tags.add_tag)
        self.button_tag_del.clicked.connect(Tags.del_tag)


        self.notes = {
            "Добро пожаловать!" : {
                "текст" : "Это самое лучшее приложение для заметок в мире!",
                "теги" : ["добро", "инструкция"]
            }
        }
        with open("notes_data.json", "w") as json_file:
            json.dump(self.notes, json_file)
            
        with open('notes_data.json','r') as file:
            notes = json.load(file)
            self.list_notes.addItems(notes)
            

    def show_note(self):
        key = self.list_notes.selectedItems()[0].text()
        print(key)
        self.field_text.setText(self.notes[key]['текст'])
        self.list_tags.clear()
        self.list_tags.addItems(self.notes[key]['теги'])


    def add_note(self):
        note_name, ok = QInputDialog.getText(self, 'Добавить заметку', 'Название заметки' )
        if ok and note_name != '':
            self.notes[note_name] = { 'текст':'', 'теги':[]}
        self.list_notes.addItem(note_name)
        self.list_tags.addItems(self.notes[note_name]['теги'])
        print(self.notes)

    def save_note(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            self.notes[key]['текст'] = self.field_text.toPlainText()
            with open('notes_data.json','w') as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
        else:
            print('Заметка не выбрана для сохранения!')

    def del_note(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            del self.notes[key]
            self.list_notes.clear()
            self.list_tags.clear()
            self.list_notes.addItems(self.notes)
            with open('notes_data.json','w') as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
        else:
            print('Заметка не выбрана для удаления!')

    

class Tags(MainWindow):
    def add_tag(self):
        if self.list_notes.selectedItems():
            self.key = self.list_notes.selectedItems()[0].text()
            self.tag = self.field_tag.text()
            if not self.tag in self.notes[self.key]['теги']:
                self.notes[self.key]['теги'].append(self.tag)
                self.list_tags.addItem(self.tag)
                self.field_tag.clear()
            with open('notes_data.json','w') as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
        else:
            print('Заметка для добавления тега не выбрана!')

    def del_tag(self):
        if self.list_tags.selectedItems()[0].text():
            self.key = self.list_notes.selectedItems()[0].text()
            self.tag = self.list_tags.selectedItems()[0].text()
            self.notes[self.key]['теги'].remove(self.tag)
            self.list_tags.clear()
            self.list_tags.addItems(self.notes[self.key]['теги'])
            with open('notes_data.json','w') as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
        else:
            print('Тег для удаления не выбран!')
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    note_app = MainWindow()
    note_app.show()
    sys.exit(app.exec())



    