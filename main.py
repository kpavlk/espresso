import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Эспрессо")
        self.connection = sqlite3.connect("coffee.sqlite")
        self.view_info()
        self.addButton.clicked.connect(self.adding)

    def view_info(self):
        result = self.connection.cursor().execute("SELECT * FROM coffee")
        self.tableWidget.setColumnCount(7)
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def adding(self):
        rows = list(set(i.row() for i in self.tableWidget.selectedItems()))
        new_item = [(self.tableWidget.item(i, 0).text(),
                     self.tableWidget.item(i, 1).text(),
                     self.tableWidget.item(i, 2).text(),
                     self.tableWidget.item(i, 3).text(),
                     self.tableWidget.item(i, 4).text(),
                     self.tableWidget.item(i, 5).text(),
                     self.tableWidget.item(i, 6).text()) for i in rows]
        if len(new_item) > 0:
            self.add_form = AddWidget(self, p_id=new_item[0][0],
                                      p_name=new_item[0][1],
                                      p_roasting=new_item[0][2],
                                      p_type=new_item[0][3],
                                      p_description=new_item[0][4],
                                      p_price=new_item[0][5],
                                      p_volume=new_item[0][6])
        else:
            self.add_form = AddWidget(self)
        self.add_form.show()


class AddWidget(QMainWindow):
    def __init__(self, parent=None, p_id=0, p_name="", p_roasting="", p_type="",
                 p_description="", p_price=0, p_volume=0):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.p_id = p_id
        self.pushButton.clicked.connect(self.get_adding_verdict)
        self.id.setPlainText(f"{p_id}")
        self.name.setPlainText(f"{p_name}")
        self.roasting.setPlainText(f"{p_roasting}")
        self.description.setPlainText(f"{p_description}")
        self.comboBox.setCurrentText(p_type)
        self.price.setPlainText(f"{p_price}")
        self.volume.setPlainText(f"{p_volume}")
        if p_name != "":
            self.isEdit = True
        else:
            self.isEdit = False

    def get_adding_verdict(self):
        id = self.id.toPlainText()
        name = self.name.toPlainText()
        roasting = self.roasting.toPlainText()
        description = self.description.toPlainText()
        price = self.price.toPlainText()
        volume = self.volume.toPlainText()
        if self.isEdit:
            self.cur.execute(f'DELETE FROM Coffee WHERE id = {self.p_id}')
        self.cur.execute("""INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?);""", (id, name,
                                                                                  roasting, self.comboBox.currentText(),
                                                                                  description, price, volume))
        self.con.commit()
        self.parent().view_info()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
