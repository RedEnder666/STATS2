# Импорт
import sys
import csv
import pandas as pd
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from Funcs import *
import traceback
from graph import graphic

# Импорт окончен


old_qss = open('old.qss', 'r').read()

new_qss = open('new.qss', 'r').read()


def err(txt):
    e = QMessageBox()
    e.setText(txt)
    return e.exec_()
def log_uncaught_exceptions(ex_cls, e, tb):  # Выловщик ошибок
    text = '{}: {}:\n'.format(ex_cls.__name__, e)

    text += ''.join(traceback.format_tb(tb))

    print(text)
    # QMessageBox.critical(None, 'Error', text)

    # sys.exit()


sys.excepthook = log_uncaught_exceptions


class ShitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dialwindow_tablesize.ui', self)
        self.pushButton.clicked.connect(self.getsize)
        self.tableE.returnPressed.connect(self.getsize)

    def getsize(self):
        if int(self.tableE.text()) <= 10000:
            ex.statistic.setRowCount(int(self.tableE.text()))
        """
        for i in range(2):
            for j in range(ex.statistic.rowCount()):
                ex.statistic.setItem(j, i, QTableWidgetItem('0'))"""
        self.hide()
        ex.alllist.clear()
        ex.onelist.clear()
        ex.twolist.clear()
        ex.result()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.data = None
        self.getData(self.statistic)
        self.statistic.cellChanged.connect(self.result)
        self.svaz.currentIndexChanged.connect(self.result)
        self.execButton.clicked.connect(self.result)
        self.resizeButton.clicked.connect(self.resizeTable)
        self.setFixedSize(self.size())
        self.loadButton.clicked.connect(self.loadTable)
        self.execButton_2.clicked.connect(self.rendergraph)
        self.styleCheck.toggled.connect(self.styleChange)

    def rendergraph(self):
        graphic(self.data[1])
        graphic(self.data[0])

    def styleChange(self):
        x = self.styleCheck.isChecked()
        if x:
            self.setStyleSheet(new_qss)
            self.statistic.resize(402, self.statistic.height())
        else:
            self.setStyleSheet(old_qss)
            self.statistic.resize(400, self.statistic.height())

    def loadTable(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать таблицу', '',
            'Старый формат Excel (*.xlsx);;Таблица (*.xls);;Другая таблица(любой разделитель(*))')[0]
        vals = []
        try:
            xl = pd.ExcelFile(fname)
            vals1 = str(xl.parse(xl.sheet_names[0])).split('\n')
            vals = [[(float(j) if float(j)//1 != float(j) else int(float(j))) if j != "NaN" else '' for j in i.split()[len(i.split()) - 2:3:]] for i in vals1]

        except:
            with open(fname) as f:
                separator, ok = QInputDialog.getText(self, 'Разделитель', 'Введите разделитель')

                if ok:
                    if separator == '\\t':
                        separator = '\t'
                    rd = csv.reader(f, delimiter=separator)
                    vals = [row for row in rd]
        self.statistic.setRowCount(len(vals))
        for i in range(2):
            for j in range(self.statistic.rowCount()):
                self.statistic.setItem(j, i, QTableWidgetItem(str(vals[j][i])))

    def resizeTable(self):
        self.w = ShitWindow()
        self.w.setWindowIcon(QtGui.QIcon('ico.png'))
        self.w.show()

    def getData(self, table):
        rows = table.rowCount()
        cols = table.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                print(tmp)
                try:
                    tmp.append(float(table.item(row, col).text()))

                except:
                    tmp.append(None)
            data.append(tmp)
        data = zip(*data[::-1])
        self.data = list(data)

    def result(self):
        self.getData(self.statistic)
        self.alllist.clear()
        self.onelist.clear()
        self.twolist.clear()
        n = 3  # До скольки знаков округлять.
        print(self.data)
        try:
            self.onelist.addItem(f'Среднее арифмитическое: {round(sredn(self.data[0]), n)}')
            self.onelist.addItem(f'Коэффициент вариаций: {round(koeff_vars(self.data[0]), n)}')
            self.onelist.addItem(f'Среднее отклонение: {round(sredn_otklon(self.data[0]), n)}')
            self.onelist.addItem(f'Мода: {round(moda(self.data[0]), n)}')
            self.onelist.addItem(f'Медиана: {round(median(self.data[0]), n)}')
            self.onelist.addItem(f'Выброс: {round(vibr(self.data[0]), n)}')
            self.onelist.addItem(f'Ошибка средней: {round(error_sredn(self.data[0]), n)}')
            self.onelist.addItem(f'Дисперсия: {round(dispersion(self.data[0]), n)}')
            self.onelist.addItem(f'Разброс: {round(scope(self.data[0]), n)}')
        except Exception as e:
            self.onelist.clear()
        try:
            self.twolist.addItem(f'Среднее арифмитическое: {round(sredn(self.data[1]), n)}')
            self.twolist.addItem(f'Коэффициент вариаций: {round(koeff_vars(self.data[1]), n)}')
            self.twolist.addItem(f'Среднее отклонение: {round(sredn_otklon(self.data[1]), n)}')
            self.twolist.addItem(f'Мода: {round(moda(self.data[1]), n)}')
            self.twolist.addItem(f'Медиана: {round(median(self.data[1]), n)}')
            self.twolist.addItem(f'Выброс: {round(vibr(self.data[1]), n)}')
            self.twolist.addItem(f'Ошибка средней: {round(error_sredn(self.data[1]), n)}')
            self.twolist.addItem(f'Дисперсия: {round(dispersion(self.data[1]), n)}')
            self.twolist.addItem(f'Разброс: {round(scope(self.data[1]), n)}')
        except Exception as e:
            self.twolist.clear()
        try:
            # 1 - независимые, 2 - зависимые
            ttest = eval(f'ttest{self.svaz.currentIndex() + 1}')
            # Я шизоид, поэтому тут сделал такой говнокод. Оно работает круто, но через eval.

            self.alllist.addItem(f'Т-критерий Стьюдента: {round(ttest(*self.data), n)}')
        except Exception as e:
            self.alllist.clear()
        #graphic(self.data[1])
        # Говнокод, за то строк много!!!


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ico.png'))
    ex = MyWidget()
    ex.setWindowIcon(QtGui.QIcon('ico.png'))
    ex.show()
    sys.exit(app.exec_())

