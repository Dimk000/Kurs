import time

import FreqToStruct as FTS
import SoloCompare as SC
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar
from matplotlib.figure import Figure

mpl.rc('font', family='Verdana')


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QRadioButton,
                                     QTabWidget,
                                     QProgressBar, QWidget, QVBoxLayout)

        QWidget.__init__(self, parent)
        #  создаем поля текста, отображаемого на эвкранчике
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

        self.voice_wLine = QLabel("Введите частоту")

        self.StartXGraphLabel = QLabel("Начало графика по x")
        self.StartYGraphLabel = QLabel("Начало графика по y")
        self.quantStepLabel = QLabel("Шаг квантования")
        self.wStepLabel = QLabel("wStep")

        self.CSTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CSTitle.setStyleSheet("QLabel {background-color: #FFFFFF;border: 1px solid black;}")
        #  поля ввода
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
        self.quantStepEdit = QLineEdit("2")
        self.wStepEdit = QLineEdit("0.05")

        self.voice_w = QLineEdit("1.5")

        self.StartXGraphEdit = QLineEdit("0")
        self.StartYGraphEdit = QLineEdit("0")

        self.test = QPlainTextEdit("1.5")

        self.CSsin = QRadioButton("Для внешних \nпомех")
        self.CScos = QRadioButton("Для внутренних \nпомех")
        #  соединяем нажатие на радио кнопушки с функциями
        self.CSsin.toggled.connect(self.CSsinClick)
        self.CScos.toggled.connect(self.CScosClick)
        #  ставим по умолчанию выбор на синус
        self.CSsin.setChecked(True)
        #  основные кнопушки
        self.btnQuit = QPushButton("Закрыть")
        self.btnSave = QPushButton("Сохранить")
        self.btnClear = QPushButton("Очистить")
        self.btnCalculate = QPushButton("Вычислить")
        self.btnFound = QPushButton("Найти")

        self.btnDrawGraph = QPushButton("Нарисовать")
        self.btnLoadFromDb = QPushButton("Загрузить из БД")
        self.btnCompare = QPushButton("Сравнить")

        self.stat = QProgressBar()  # обьявляем переменную для виджета прогресса выполнения

        #  херня справа, создаем многострочное поле ввода
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEditWin2 = QPlainTextEdit()

        self.hbox_win1 = QHBoxLayout()  # гор. бокс для основного окна.
        self.hbox_win2 = QHBoxLayout()  # гор бокс для второго окна
        self.hbox_win3 = QHBoxLayout()  # гор бокс для третьего окна

        self.hbox_name = QHBoxLayout()  # бокс для трех полей(массив)
        self.hbox_edit = QHBoxLayout()  # бокс для трех полей ввода(массив)

        self.hbox_sin_cos = QHBoxLayout()  # гор бокс для радиокнопушек синуса, косинуса

        self.vbox = QVBoxLayout()  # бокс для ввода значений
        self.vbox_graph = QVBoxLayout()  # бокс для графика
        self.vbox_dop_character = QVBoxLayout()  # бокс для правого окна

        self.vboxWin2 = QVBoxLayout()
        self.vbox_graphWin2 = QVBoxLayout()

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

        # назначаем на кнопушки действия
        self.btnQuit.clicked.connect(self.close)
        self.btnSave.clicked.connect(self.SaveToDb)
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnClear.clicked.connect(self.clear)
        self.btnFound.clicked.connect(self.fnd)

        self.btnDrawGraph.clicked.connect(self.drw2)
        self.btnLoadFromDb.clicked.connect(self.LoadFromDb)
        self.btnCompare.clicked.connect(self.compare)

        # добавляем в верт блок виджеты с основными кнопушками
        self.vbox.addWidget(self.btnCalculate)
        self.vbox.addWidget(self.btnSave)
        self.vbox.addWidget(self.btnQuit)
        self.vbox.addWidget(self.btnClear)
        self.vboxWin2.addWidget(self.quantStepLabel)
        self.vboxWin2.addWidget(self.quantStepEdit)
        self.vboxWin2.addWidget(self.wStepLabel)
        self.vboxWin2.addWidget(self.wStepEdit)

        self.vboxWin2.addWidget(self.StartXGraphLabel)
        self.vboxWin2.addWidget(self.StartXGraphEdit)
        self.vboxWin2.addWidget(self.StartYGraphLabel)
        self.vboxWin2.addWidget(self.StartYGraphEdit)

        self.vboxWin2.addWidget(self.btnDrawGraph)
        self.vboxWin2.addWidget(self.btnLoadFromDb)
        self.vboxWin2.addWidget(self.btnCompare)

        self.vboxWin2.addWidget(self.plainTextEditWin2)

        # обьявляем все нужные виджеты для графика + тулбокс
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # 111 - признак расположения нескольких графиков)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolBar(self.canvas, self)

        self.hbox_graph_menu = QHBoxLayout()  # создаем гор бокс для менюшки для графика
        self.hbox_graph_menu.addWidget(self.toolbar)  # добавляем в менюшку графика тулбокс

        self.figureWin2 = Figure()
        self.axesWin2 = self.figureWin2.add_subplot(111)
        # 111 - признак расположения нескольких графиков)

        self.canvasWin2 = FigureCanvas(self.figureWin2)
        self.toolbarWin2 = NavigationToolBar(self.canvasWin2, self)

        self.hbox_graph_menuWin2 = QHBoxLayout()  # создаем гор бокс для менюшки для графика
        self.hbox_graph_menuWin2.addWidget(self.toolbarWin2)  # добавляем в менюшку графика тулбокс

        self.vbox_graph.addWidget(self.canvas)  # добавляем во второй верт бокс график
        self.vbox_graph.addLayout(self.hbox_graph_menu)  # в верт бокс графика добавляем менюшку

        self.vbox_graphWin2.addWidget(self.canvasWin2)
        self.vbox_graphWin2.addLayout(self.hbox_graph_menuWin2)

        self.vbox_dop_character.addWidget(self.voice_wLine)
        self.vbox_dop_character.addWidget(self.voice_w)
        self.vbox_dop_character.addWidget(self.btnFound)

        self.vbox_dop_character.addWidget(self.plainTextEdit)  # в третий бокс добавляем многострочное поле вв/выв
        self.vbox_dop_character.addWidget(self.stat)  # в третий бокс добавляем виджет прогресса выполнения

        self.hbox_win1.addLayout(self.vbox)  # в первое окно добавляем основной бокс
        self.hbox_win1.addLayout(self.vbox_graph)  # во второе окно добавляем основной бокс
        self.hbox_win1.addLayout(self.vbox_dop_character)  # в третье окно добавляем основной бокс

        self.hbox_win2.addLayout(self.vbox_graphWin2)
        self.hbox_win2.addLayout(self.vboxWin2)

        # ебашим три фрейма, ибо без фрейма вкладочка не робит
        self.frame_win1 = QFrame()
        self.frame_win2 = QFrame()
        self.frame_win3 = QFrame()
        # добавляем во фреймы основные гор боксы
        self.frame_win1.setLayout(self.hbox_win1)
        self.frame_win2.setLayout(self.hbox_win2)
        self.frame_win3.setLayout(self.hbox_win3)
        # еще один вертикальный бокс, для ВООбще всего окна + вкладочки
        self.mainV = QVBoxLayout()
        # создаем виджет вкладочки
        self.tab = QTabWidget()
        self.tab.addTab(self.frame_win1, "lol")  # добавляем сами вкладочки(заполненные) и обзываем их
        self.tab.addTab(self.frame_win2, "lol2")
        self.tab.addTab(self.frame_win3, "lol3")

        self.mainV.addWidget(self.tab)  # добавляем на главное окно виджет вкладочек
        self.setLayout(self.mainV)  # добавляем к САМОМУ окну слой со всем этим дерьмом

    def SaveToDb(self):
        import datetime
        outfile = open('/home/user/V 2.0/Sohranenie/sign/kurs/datas/{:%Y-%m-%d %H-%M-%S}.csv'.format(datetime.datetime.now()), 'w')
        WFCoeff = list(map(float, self.WFCoeffEdit.text().split()))
        Tmass = list(map(float, self.TmassEdit.text().split()))
        for i in range(len(Tmass)):
            outfile.write('%.3f' % Tmass[i] + ",")
        outfile.write('\n')

        for i in range(len(WFCoeff)):
            outfile.write('%.3f' % WFCoeff[i] + ",")
        outfile.write('\n')
        outfile.close()

    def LoadFromDb(self):
        import os
        import csv
        count = 1


        for (dirpath, dirnames, filenames) in os.walk('/home/user/V 2.0/Sohranenie/sign/kurs/datas'):
            for filename in filenames:
                self.plainTextEditWin2.appendPlainText(str(count) + " file: " + filename + "\n")
                # print(filename)  # Просто имя файла
                # print(os.path.join(dirpath, filename))  # Имя с путём. os.path.join склеивает две части пути
                f = open(os.path.join(dirpath, filename), 'r',
                         encoding='utf-8')  # Если есть путь к файлу, то его можно открыт

                table = []
                temp = []
                for row in csv.reader(f):
                    self.plainTextEditWin2.appendPlainText(str(row) + "\n")
                    table.append(row)
                    TmassLen = len(row)
                    for c in range(len(row)-1):
                        temp.append(float(row[c]))

                Tmass1 = []
                WFCoeff1 = []
                i = 0
                while i < TmassLen:
                    Tmass1.append(temp[i])
                    i += 1
                while i < len(temp):
                    WFCoeff1.append(temp[i])
                    i += 1
                S1 = np.zeros(len(MassForRes))
                Stemp = self.fn1(CSch, MassForRes, S1, Tmass1, WFCoeff1, timeStep)
                M1 = FTS.FreqToStruct(MassForRes, Stemp, WFCoeff1, wStep, quantStep)
                f.close()
                # self.plainTextEditWin2.appendPlainText("\n" + file_data)
                # print(file_data)
                count += 1
                return M1

    def DrawGraph(self):
        global StartGraphX
        global StartGraphY
        StartGraphX = float(self.StartXGraphEdit.text())
        StartGraphY = float(self.StartYGraphEdit.text())
        meh()

    # функции для косинуса и синуса(радио кнопушки)
    def CScosClick(self, enabled):
        if enabled:
            self.CSTitle.setText('Для внутренних помех ')  # и выводим в заголовке, что у нас косинус
            self.CS.setText('1')  # если будет нажат косинус, то мы принимаем значение как 1

    def CSsinClick(self, enabled):
        if enabled:
            self.CSTitle.setText('Для внешних помех')
            self.CS.setText('2')

    def valuesForCalc(self):
        Step = float(self.StepMasEdit.text())
        Start = float(self.StartMasEdit.text())
        End = float(self.EndMasEdit.text())
        global WFCoeff, CSch, timeStep, Tmass
        WFCoeff = list(map(float, self.WFCoeffEdit.text().split()))
        Tmass = list(map(float, self.TmassEdit.text().split()))
        timeStep = float(self.timeStepEdit.text())
        CSch = int(self.CS.text())
        return CSch, End, Start, Step, Tmass, WFCoeff, timeStep

    def calculate(self):
        t1 = time.time()
        self.stat.reset()
        CSch, End, Start, Step, Tmass, WFCoeff, timeStep = self.valuesForCalc()
        global MassForRes
        MassForRes = np.arange(Start, End, Step, dtype=float)

        self.stat.setMinimum(0)
        self.stat.setMaximum(len(MassForRes))
        if len(Tmass) == len(WFCoeff) + 1:
            global S
            S = np.zeros(len(MassForRes), dtype=float)
            self.fn(CSch, MassForRes, S, Tmass, WFCoeff, timeStep)
        self.drw1(Start, Step, End)
        self.stat.setValue(len(MassForRes))
        print(time.time() - t1)

    def drw1(self, Start, Step, End):
        self.axes.plot(MassForRes, abs(S)/sum(WFCoeff), label="for {} : {} : {}".format(Start, Step, End))
        self.axes.set_xbound(lower=0, upper=MassForRes.max())
        self.axes.set_xlabel('ω - относительная частота')
        self.axes.set_ylabel('Коэффициент передачи')
        self.axes.grid(True)
        self.axes.legend()
        self.canvas.draw()

    def drw2(self):
        self.axesWin2.plot(MassForRes, abs(S)/sum(WFCoeff), label="From lol1")
        self.axesWin2.set_xlabel('ω - относительная частота')
        self.axesWin2.set_ylabel('Коэффициент передачи')
        self.axesWin2.grid(True)
        self.axesWin2.legend()
        self.canvasWin2.draw()

    def drw(self):
        self.axesWin2.plot(Xdatag, Ydatag, label="draw")
        self.axesWin2.set_xlabel('ω - относительная частота')
        self.axesWin2.set_ylabel('Коэффициент передачи')
        self.axesWin2.grid(True)
        self.axesWin2.legend()
        self.canvas.draw()

    def compare(self):
        global quantStep, wStep, Mmain
        quantStep = int(self.quantStepEdit.text())
        wStep = float(self.wStepEdit.text())
        Mmain = FTS.FreqToStruct(MassForRes, S, WFCoeff, wStep, quantStep)
        Mall = []
        Mall.append(self.LoadFromDb())
        for i in range(len(Mall)):
            SC.solocomp(Mmain, Mall[i])
        # print(Mmain)
        # print(Mall)


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
                S[j] += round(SetCurrent * WFCoeff[i - 1], 10)
            self.stat.setValue(int(j))
        # print(S)

    def fn1(self, CSch, MassForRes, S1, Tmass1, WFCoeff1, timeStep):
        from math import sin, cos, pi
        for j in range(0, len(MassForRes), 1):
            S1[j] = 0
            for i in range(1, len(Tmass1), 1):
                t = np.arange(Tmass1[i - 1], Tmass1[i], timeStep)
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
                S1[j] += round(SetCurrent * WFCoeff1[i - 1], 10)
        return S1

            # self.plainTextEdit.setPlainText("S =" + str(S))
            # self.plainTextEdit.appendPlainText("Step="+str(Step)+",   w="+str(MassForRes))

    def clear(self):
        self.axes.clear()
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


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        line.get_xdata(1)
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        global Xdatag, Ydatag
        print(event.xdata)
        print(event.ydata)
        Xdatag.append(event.xdata)
        Ydatag.append(event.ydata)
        if event.inaxes != self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


def meh():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click to build line segments')
    line, = ax.plot([0, 100, 0.5],[0, 100, 0.5], color = 'green', alpha=0.0)  # empty line
    line2, = ax.plot([StartGraphX], [StartGraphY], 'r-')  # empty line
    line2.set_antialiased(True)
    linebuilder = LineBuilder(line2)
    plt.show()
    # print(Xdatag)
    # print(Ydatag)
    # plt.plot(Xdatag, Ydatag)
    # plt.show()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    Xdatag = []
    Ydatag = []
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Функция для нахождения площадей основных гармонических составляющих")
    window.setFixedSize(1000, 600)
    window.show()
    sys.exit(app.exec_())