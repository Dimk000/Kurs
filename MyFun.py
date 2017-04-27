import time

import FreqToStruct as FTS
import matplotlib as mpl
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QRadioButton,
                             QTabWidget,
                             QProgressBar, QWidget, QVBoxLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar
from matplotlib.figure import Figure

mpl.rc('font', family='Verdana')


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)
        #  создаем поля текста, отображаемого на эвкранчике
        self.lbl()
        #  поля ввода
        self.edt()
        self.btnSinCos()
        #  ставим по умолчанию выбор на синус
        self.CSsin.setChecked(True)
        #  основные кнопушки
        self.btnDef()
        #  херня справа, создаем многострочное поле ввода
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEditWin2 = QPlainTextEdit()
        self.box()
        self.addPar()
        # назначаем на кнопушки действия
        self.btnClick()
        # добавляем в верт блок виджеты с основными кнопушками
        self.addBtn()
        # обьявляем все нужные виджеты для графика + тулбокс
        self.addGraph()
        self.plParam()

        self.vbox_dop_character.addWidget(self.plainTextEdit)  # в третий бокс добавляем многострочное поле вв/выв
        self.vbox_dop_character.addWidget(self.stat)  # в третий бокс добавляем виджет прогресса выполнения

        self.vbox_dop_characterWin2.addWidget(self.plainTextEditWin2)
        self.addLay_win()
        self.frameadd()
        # еще один вертикальный бокс, для ВООбще всего окна + вкладочки
        self.mainV = QVBoxLayout()
        # создаем виджет вкладочки
        self.tab = QTabWidget()
        self.tab.addTab(self.frame_win1, "lol")  # добавляем сами вкладочки(заполненные) и обзываем их
        self.tab.addTab(self.frame_win2, "lol2")
        self.tab.addTab(self.frame_win3, "lol3")
        self.mainV.addWidget(self.tab)  # добавляем на главное окно виджет вкладочек
        self.setLayout(self.mainV)  # добавляем к САМОМУ окну слой со всем этим дерьмом

    def frameadd(self):
        # ебашим три фрейма, ибо без фрейма вкладочка не робит
        self.frame_win1 = QFrame()
        self.frame_win2 = QFrame()
        self.frame_win3 = QFrame()
        # добавляем во фреймы основные гор боксы
        self.frame_win1.setLayout(self.hbox_win1)
        self.frame_win2.setLayout(self.hbox_win2)
        self.frame_win3.setLayout(self.hbox_win3)

    def addLay_win(self):
        self.hbox_win1.addLayout(self.vbox)  # в первое окно добавляем основной бокс
        self.hbox_win1.addLayout(self.vbox_graph)  # во второе окно добавляем основной бокс
        self.hbox_win1.addLayout(self.vbox_dop_character)  # в третье окно добавляем основной бокс

        self.hbox_win2.addLayout(self.vboxWin2)  # в первое окно добавляем основной бокс
        self.hbox_win2.addLayout(self.vbox_graphWin2)  # во второе окно добавляем основной бокс
        self.hbox_win2.addLayout(self.vbox_dop_characterWin2)  # в третье окно добавляем основной бокс

    def plParam(self):
        self.hbox_graph_menu = QHBoxLayout()  # создаем гор бокс для менюшки для графика
        self.hbox_graph_menu.addWidget(self.toolbar)  # добавляем в менюшку графика тулбокс
        self.vbox_graph.addWidget(self.canvas)  # добавляем во второй верт бокс график
        self.vbox_graph.addLayout(self.hbox_graph_menu)  # в верт бокс графика добавляем менюшку
        self.stat = QProgressBar()  # обьявляем переменную для виджета прогресса выполнения
        self.voice_wLine = QLabel("Введите частоту")
        self.voice_w = QLineEdit("1.5")
        self.vbox_dop_character.addWidget(self.voice_wLine)
        self.vbox_dop_character.addWidget(self.voice_w)
        self.vbox_dop_character.addWidget(self.btnFound)

        self.hbox_graph_menuWin2 = QHBoxLayout()  # создаем гор бокс для менюшки для графика
        self.hbox_graph_menuWin2.addWidget(self.toolbarWin2)  # добавляем в менюшку графика тулбокс
        self.vbox_graphWin2.addWidget(self.canvasWin2)  # добавляем во второй верт бокс график
        self.vbox_graphWin2.addLayout(self.hbox_graph_menuWin2)  # в верт бокс графика добавляем менюшку
        self.statWin2 = QProgressBar()  # обьявляем переменную для виджета прогресса выполнения

        self.vbox_dop_characterWin2.addWidget(self.quantStepLbl)
        self.vbox_dop_characterWin2.addWidget(self.quantStepEdit)
        self.vbox_dop_characterWin2.addWidget(self.wStepLbl)
        self.vbox_dop_characterWin2.addWidget(self.wStepEdit)

    def addGraph(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # 111 - признак расположения нескольких графиков)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolBar(self.canvas, self)

        self.figureWin2 = Figure()
        self.axesWin2 = self.figureWin2.add_subplot(111)
        # 111 - признак расположения нескольких графиков)
        self.canvasWin2 = FigureCanvas(self.figureWin2)
        self.toolbarWin2 = NavigationToolBar(self.canvasWin2, self)

    def addBtn(self):
        self.vbox.addWidget(self.btnCalculate)
        self.vbox.addWidget(self.btnSave)
        self.vbox.addWidget(self.btnQuit)
        self.vbox.addWidget(self.btnClear)

        self.vboxWin2.addWidget(self.btnCalculateWin2)
        self.vboxWin2.addWidget(self.btnQuitWin2)

    def btnClick(self):
        self.btnQuit.clicked.connect(self.close)
        self.btnSave.clicked.connect(self.SaveToDb)
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnClear.clicked.connect(self.clear)
        self.btnFound.clicked.connect(self.fnd)

        self.btnQuitWin2.clicked.connect(self.close)
        self.btnCalculateWin2.clicked.connect(self.calculate)

    def addPar(self):
        self.hbox_sin_cos.addWidget(self.CScos)  # добавляем радио кнопушки в гор бокс
        self.hbox_sin_cos.addWidget(self.CSsin)
        self.hbox_name.addWidget(self.StartMas)  # добавляем поля текста в гор бокс
        self.hbox_name.addWidget(self.StepMas)
        self.hbox_name.addWidget(self.EndMas)
        self.hbox_edit.addWidget(self.StartMasEdit)  # добавляем поля ввода в гор бокс
        self.hbox_edit.addWidget(self.StepMasEdit)
        self.hbox_edit.addWidget(self.EndMasEdit)
        # добавляем в верт блок слои с полями значений
        self.vbox.addLayout(self.hbox_name)
        self.vbox.addLayout(self.hbox_edit)
        # добавляем в верт блок виджеты с полями значений
        self.vbox.addWidget(self.Tmass)
        self.vbox.addWidget(self.TmassEdit)
        self.vbox.addWidget(self.WFCoeffLine)
        self.vbox.addWidget(self.WFCoeffEdit)
        self.vbox.addWidget(self.timeStepLine)
        self.vbox.addWidget(self.timeStepEdit)
        self.vbox.addWidget(self.CSTitle)
        # добавляем в верт блок слой с радио кнопушками
        self.vbox.addLayout(self.hbox_sin_cos)

        self.hbox_sin_cosWin2.addWidget(self.CScosWin2)  # добавляем радио кнопушки в гор бокс
        self.hbox_sin_cosWin2.addWidget(self.CSsinWin2)
        self.hbox_nameWin2.addWidget(self.StartMasWin2)  # добавляем поля текста в гор бокс
        self.hbox_nameWin2.addWidget(self.StepMasWin2)
        self.hbox_nameWin2.addWidget(self.EndMasWin2)
        self.hbox_editWin2.addWidget(self.StartMasEditWin2)  # добавляем поля ввода в гор бокс
        self.hbox_editWin2.addWidget(self.StepMasEditWin2)
        self.hbox_editWin2.addWidget(self.EndMasEditWin2)
        # добавляем в верт блок слои с полями значений
        self.vboxWin2.addLayout(self.hbox_nameWin2)
        self.vboxWin2.addLayout(self.hbox_editWin2)
        # добавляем в верт блок виджеты с полями значений
        self.vboxWin2.addWidget(self.TmassWin2)
        self.vboxWin2.addWidget(self.TmassEditWin2)
        self.vboxWin2.addWidget(self.WFCoeffLineWin2)
        self.vboxWin2.addWidget(self.WFCoeffEditWin2)
        self.vboxWin2.addWidget(self.timeStepLineWin2)
        self.vboxWin2.addWidget(self.timeStepEditWin2)
        self.vboxWin2.addWidget(self.CSTitleWin2)
        # добавляем в верт блок слой с радио кнопушками
        self.vboxWin2.addLayout(self.hbox_sin_cosWin2)

    def box(self):
        self.hbox_win1 = QHBoxLayout()  # гор. бокс для основного окна.
        self.hbox_win2 = QHBoxLayout()  # гор бокс для второго окна
        self.hbox_win3 = QHBoxLayout()  # гор бокс для третьего окна
        self.hbox_name = QHBoxLayout()  # бокс для трех полей(массив)
        self.hbox_edit = QHBoxLayout()  # бокс для трех полей ввода(массив)
        self.hbox_sin_cos = QHBoxLayout()  # гор бокс для радиокнопушек синуса, косинуса
        self.vbox = QVBoxLayout()  # бокс для ввода значений
        self.vbox_graph = QVBoxLayout()  # бокс для графика
        self.vbox_dop_character = QVBoxLayout()  # бокс для правого окна


        self.hbox_nameWin2 = QHBoxLayout()  # бокс для трех полей(массив)
        self.hbox_editWin2 = QHBoxLayout()  # бокс для трех полей ввода(массив)
        self.hbox_sin_cosWin2 = QHBoxLayout()  # гор бокс для радиокнопушек синуса, косинуса
        self.vboxWin2 = QVBoxLayout()  # бокс для ввода значений
        self.vbox_graphWin2 = QVBoxLayout()  # бокс для графика
        self.vbox_dop_characterWin2 = QVBoxLayout()  # бокс для правого окна

    def btnDef(self):
        self.btnQuitWin2 = QPushButton("Закрыть")
        self.btnCalculateWin2 = QPushButton("Сравнить")

        self.btnQuit = QPushButton("Закрыть")
        self.btnSave = QPushButton("Сохранить")
        self.btnClear = QPushButton("Очистить")
        self.btnCalculate = QPushButton("Вычислить")
        self.btnFound = QPushButton("Найти")

    def btnSinCos(self):
        self.CSsin = QRadioButton("Для внешних \nпомех")
        self.CScos = QRadioButton("Для внутренних \nпомех")
        #  соединяем нажатие на радио кнопушки с функциями
        self.CSsin.toggled.connect(self.CSsinClick)
        self.CScos.toggled.connect(self.CScosClick)

        self.CSsinWin2 = QRadioButton("Для внешних \nпомех")
        self.CScosWin2 = QRadioButton("Для внутренних \nпомех")
        #  соединяем нажатие на радио кнопушки с функциями
        self.CSsinWin2.toggled.connect(self.CSsinClick)
        self.CScosWin2.toggled.connect(self.CScosClick)

    def edt(self):
        self.StartMasEdit = QLineEdit("0.001")
        self.StartMasEdit.setFixedWidth(100)
        self.StepMasEdit = QLineEdit("0.001")
        self.StepMasEdit.setFixedWidth(50)
        self.EndMasEdit = QLineEdit("3")
        self.EndMasEdit.setFixedWidth(100)
        self.TmassEdit = QLineEdit("0 1 2 3 4 5 6")
        self.WFCoeffEdit = QLineEdit("0.89 5.13 9.97 10.03 4.74 1.35")
        self.timeStepEdit = QLineEdit("0.01")
        #  начальное значение для радио кнопушек синуса, коминуса
        self.CS = QLineEdit("0")
        self.test = QPlainTextEdit("1.5")
        self.quantStepEdit = QLineEdit("2")
        self.wStepEdit = QLineEdit("0.05")

        self.StartMasEditWin2 = QLineEdit("0.001")
        self.StartMasEditWin2.setFixedWidth(100)
        self.StepMasEditWin2 = QLineEdit("0.001")
        self.StepMasEditWin2.setFixedWidth(50)
        self.EndMasEditWin2 = QLineEdit("3")
        self.EndMasEditWin2.setFixedWidth(100)
        self.TmassEditWin2 = QLineEdit("0 1 2 3 4 5 6")
        self.WFCoeffEditWin2 = QLineEdit("0.89 5.13 9.97 10.03 4.74 1.35")
        self.timeStepEditWin2 = QLineEdit("0.01")
        #  начальное значение для радио кнопушек синуса, коминуса
        self.CSWin2 = QLineEdit("0")


    def lbl(self):
        self.StartMas = QLabel("Начальная ω")
        self.StartMas.setFixedWidth(100)
        self.StepMas = QLabel("Δω")
        self.StepMas.setFixedWidth(50)
        self.EndMas = QLabel("Конечная ω")
        self.EndMas.setFixedWidth(100)
        self.Tmass = QLabel("Tmass")
        self.WFCoeffLine = QLabel("Весовая функция")
        self.timeStepLine = QLabel("Шаг моделирования")
        self.CSTitle = QLabel("CS")
        self.CSTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CSTitle.setStyleSheet("QLabel {background-color: #FFFFFF;border: 1px solid black;}")

        self.quantStepLbl = QLabel("Шаг квантования")
        self.wStepLbl = QLabel("wStep")

        self.StartMasWin2 = QLabel("Начальная ω")
        self.StartMasWin2.setFixedWidth(100)
        self.StepMasWin2 = QLabel("Δω")
        self.StepMasWin2.setFixedWidth(50)
        self.EndMasWin2 = QLabel("Конечная ω")
        self.EndMasWin2.setFixedWidth(100)
        self.TmassWin2 = QLabel("Tmass")
        self.WFCoeffLineWin2 = QLabel("Весовая функция")
        self.timeStepLineWin2 = QLabel("Шаг моделирования")
        self.CSTitleWin2 = QLabel("CS")
        self.CSTitleWin2.setAlignment(QtCore.Qt.AlignCenter)
        self.CSTitleWin2.setStyleSheet("QLabel {background-color: #FFFFFF;border: 1px solid black;}")

    # функции для косинуса и синуса(радио кнопушки)
    def CScosClick(self, enabled):
        if enabled:
            self.CSTitle.setText('Для внутренних помех ')  # и выводим в заголовке, что у нас косинус
            self.CS.setText('1')  # если будет нажат косинус, то мы принимаем значение как 1

    def CSsinClick(self, enabled):
        if enabled:
            self.CSTitle.setText('Для внешних помех')
            self.CS.setText('2')

    def calculate(self):
        t1 = time.time()
        self.stat.reset()
        CSch, End, Start, Step, Tmass, WFCoeff, timeStep = self.valuesForCalc()
        global MassForRes, MassForRes1
        MassForRes = np.arange(Start, End, Step, dtype=float)
        MassForRes1 = np.arange(Start, End, Step, dtype=float)
        WFCoeff1 = [1.2, 5.2, 10.2, 10.2, 5.2, 1.2]
        Tmass1 = [0, 1, 2, 3, 4, 5, 6]
        for i in range(len(MassForRes)):
            MassForRes[i] = round(MassForRes[i], 4)
            MassForRes1[i] = round(MassForRes1[i], 4)

        self.stat.setMinimum(0)
        self.stat.setMaximum(len(MassForRes))
        if len(Tmass) == len(WFCoeff) + 1:
            global S
            S = np.zeros(len(MassForRes), dtype=float)
            self.fn(CSch, MassForRes, S, Tmass, WFCoeff, timeStep)
        if len(Tmass1) == len(WFCoeff1) + 1:
            global S1
            S1 = np.zeros(len(MassForRes1), dtype=float)
            self.fn1(CSch, MassForRes1, S1, Tmass1, WFCoeff1, timeStep)
        self.drw(Start, Step, End)
        FTS.FreqToStruct(MassForRes, MassForRes1, S, S1, WFCoeff, WFCoeff1)
        self.stat.setValue(len(MassForRes))
        print(time.time() - t1)

    def SaveToDb(self):
        import sqlite3
        conn = sqlite3.connect('my.db')
        c = conn.cursor()

        #  убрать комментарий при первом запуске
        #  c.execute('''CREATE TABLE datas (tmass, wfcoeff)''')
        def add_data(Tmass, WFCoeff):
            c.execute("INSERT INTO datas (tmass,wfcoeff) VALUES ('%s','%s')" % (Tmass, WFCoeff))
            conn.commit()

        # Делаем запрос в базу
        print("Данные:\n")
        add_data(Tmass, WFCoeff)
        c.execute('SELECT * FROM datas')
        row = c.fetchone()
        while row is not None:
            print(" Tmass: " + row[0] + " | WFCoeff: " + row[1])
            row = c.fetchone()
        # закрываем соединение с базой
        c.close()
        conn.close()

    def valuesForCalc(self):
        Step = float(self.StepMasEdit.text())
        Start = float(self.StartMasEdit.text())
        End = float(self.EndMasEdit.text())
        global WFCoeff
        global Tmass
        WFCoeff = list(map(float, self.WFCoeffEdit.text().split()))
        Tmass = list(map(float, self.TmassEdit.text().split()))
        timeStep = float(self.timeStepEdit.text())
        CSch = int(self.CS.text())
        return CSch, End, Start, Step, Tmass, WFCoeff, timeStep

    def fn(self, CSch, MassForRes, S, Tmass, WFCoeff, timeStep):
        from math import sin, cos, pi
        for j in range(0, len(MassForRes), 1):
            S[j] = 0
            for i in range(1, len(Tmass), 1):
                t = np.arange(Tmass[i - 1], Tmass[i], timeStep)
                y = np.zeros(len(t))
                if CSch == 2:
                    for k in range(0, len(t), 1):
                        y[k] = cos(2 * pi * MassForRes[j] * t[k])
                if CSch == 1:
                    for k in range(0, len(t), 1):
                        y[k] = sin(2 * pi * MassForRes[j] * t[k])
                n = len(y)
                test = (sum(y[1:(n)]))
                SetCurrent = test * timeStep + (y[0] + y[n - 1]) * timeStep / 2
                S[j] += SetCurrent * WFCoeff[i - 1]
        t = 0
        n = 0
        print(S)

    def fn1(self, CSch, MassForRes1, S1, Tmass1, WFCoeff1, timeStep):
        from math import sin, cos, pi
        for j in range(0, len(MassForRes1), 1):
            S1[j] = 0
            for i in range(1, len(Tmass1), 1):
                t = np.arange(Tmass1[i - 1], Tmass1[i], timeStep)
                y = np.zeros(len(t))
                if CSch == 2:
                    for k in range(0, len(t), 1):
                        y[k] = cos(2 * pi * MassForRes1[j] * t[k])
                if CSch == 1:
                    for k in range(0, len(t), 1):
                        y[k] = sin(2 * pi * MassForRes1[j] * t[k])
                n = len(y)
                test = (sum(y[1:(n)]))
                SetCurrent = test * timeStep + (y[0] + y[n - 1]) * timeStep / 2
                S1[j] += SetCurrent * WFCoeff1[i - 1]
            self.stat.setValue(int(j))
        print(S1)

            # self.plainTextEdit.setPlainText("S =" + str(S))
            # self.plainTextEdit.appendPlainText("Step="+str(Step)+",   w="+str(MassForRes))

    def clear(self):
        self.axes.clear()
        self.canvas.draw()

    def drw(self, Start, Step, End):
        self.axes.plot(MassForRes, abs(S / sum(WFCoeff)), label="for {} : {} : {}".format(Start, Step, End))
        self.axes.set_xbound(lower=0, upper=MassForRes.max())
        self.axes.set_xlabel('ω - относительная частота')
        self.axes.set_ylabel('Коэффициент передачи')
        self.axes.grid(True)
        self.axes.legend()
        self.canvas.draw()

    def fnd(self):
        End = float(self.EndMasEdit.text())
        count = float(self.voice_w.text())
        count = int(count * (len(MassForRes) / End))
        self.axes.plot(MassForRes[count], abs(S[count]), 'ro')
        self.canvas.draw()
        self.plainTextEdit.setPlainText(
            "Коэффициент передачи = {} \n\nω - относительная частота = {}".format(round(abs(S[count]), 10),
                                                                                  MassForRes[count]))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Функция для нахождения площадей основных гармонических составляющих")
    window.setFixedSize(1000, 600)
    window.show()
    sys.exit(app.exec_())