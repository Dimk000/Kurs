import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFrame, QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPlainTextEdit
from PyQt5.QtWidgets import QPushButton, QRadioButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTabWidget, QProgressBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        group_character = QGroupBox()

        self.StartMas = QLabel("Начальная ω")
        self.StartMas.setFixedWidth(100)

        self.StepMas = QLabel("Δω")
        self.StepMas.setFixedWidth(50)

        self.EndMas = QLabel("Конечная ω")
        self.EndMas.setFixedWidth(100)

        self.Tmass = QLabel("Tmass")

        self.WFCoeffLine = QLabel("Весовая функция")

        self.timeStepLine = QLabel("Шаг моделирования")

        self.test = QPlainTextEdit("1.5")
        s = []

        self.StartMasEdit = QLineEdit("0.001")
        self.StartMasEdit.setFixedWidth(100)

        self.StepMasEdit = QLineEdit("0.001")
        self.StepMasEdit.setFixedWidth(50)

        self.EndMasEdit = QLineEdit("5")
        self.EndMasEdit.setFixedWidth(100)

        self.TmassEdit = QLineEdit("-0.5 0.5")

        self.WFCoeffEdit = QLineEdit("1")
        self.timeStepEdit = QLineEdit("0.01")
        self.CS = QLineEdit("0")
        self.CSTitle = QLabel("CS")
        self.CSTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CSTitle.setStyleSheet("QLabel {background-color: #FFFFFF;border: 1px solid black;}")
        self.CSsin = QRadioButton("Для внешних")
        self.CScos = QRadioButton("Для внутренних")

        self.CSsin.toggled.connect(self.CSsinClick)
        self.CScos.toggled.connect(self.CScosClick)

        self.CSsin.setChecked(True)

        self.btnQuit = QPushButton("Закрыть")
        self.btnClear = QPushButton("Очистить")
        self.Button1 = QPushButton("Вычислить")

        self.plainTextEdit = QPlainTextEdit()

        self.hbox_main = QHBoxLayout()
        self.hbox_name = QHBoxLayout()
        self.hbox_edit = QHBoxLayout()
        self.hbox_win2 = QHBoxLayout()
        self.hbox_win3 = QHBoxLayout()

        self.hbox_sin_cos = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox_graph = QVBoxLayout()
        self.vbox_dop_character = QVBoxLayout()

        self.hbox_sin_cos.addWidget(self.CScos)
        self.hbox_sin_cos.addWidget(self.CSsin)

        self.hbox_name.addWidget(self.StartMas)
        self.hbox_name.addWidget(self.StepMas)
        self.hbox_name.addWidget(self.EndMas)
        self.vbox.addLayout(self.hbox_name)

        self.hbox_edit.addWidget(self.StartMasEdit)
        self.hbox_edit.addWidget(self.StepMasEdit)
        self.hbox_edit.addWidget(self.EndMasEdit)
        self.vbox.addLayout(self.hbox_edit)

        self.vbox.addWidget(self.Tmass)
        self.vbox.addWidget(self.TmassEdit)

        self.vbox.addWidget(self.WFCoeffLine)
        self.vbox.addWidget(self.WFCoeffEdit)
        self.vbox.addWidget(self.timeStepLine)
        self.vbox.addWidget(self.timeStepEdit)
        self.vbox.addWidget(self.CSTitle)
        self.vbox.addLayout(self.hbox_sin_cos)

        self.vbox.addWidget(self.Button1)
        self.vbox.addWidget(self.btnQuit)
        self.vbox.addWidget(self.btnClear)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        ### 111 - признак расположения нескольких графиков)

        self.canvas = FigureCanvas(self.figure)
        # self.canvasWeight = FigureCanvas(self.figure)
        self.toolbar = NavigationToolBar(self.canvas, self)

        self.vbox_graph.addWidget(self.canvas)
        self.vbox_dop_character.addWidget(self.plainTextEdit)
        # self.vbox_graph.addWidget(self.toolbar)
        self.hbox_graph_menu = QHBoxLayout()
        self.hbox_graph_menu.addWidget(self.toolbar)

        self.vbox_graph.addLayout(self.hbox_graph_menu)
        self.stat = QProgressBar()

        self.vbox_dop_character.addWidget(self.stat)

        self.hbox_main.addLayout(self.vbox)
        self.hbox_main.addLayout(self.vbox_graph)
        self.hbox_main.addLayout(self.vbox_dop_character)

        self.frame_win1 = QFrame()
        self.frame_win2 = QFrame()
        self.frame_win3 = QFrame()

        self.frame_win1.setLayout(self.hbox_main)
        self.frame_win2.setLayout(self.hbox_win2)
        self.frame_win3.setLayout(self.hbox_win3)
        # self.setLayout(self.hbox_main)
        self.mainV = QVBoxLayout()

        self.tab = QTabWidget()
        self.tab.addTab(self.frame_win1, "lol")
        self.tab.addTab(self.frame_win2, "lol2")
        self.tab.addTab(self.frame_win3, "lol3")

        self.mainV.addWidget(self.tab)
        self.setLayout(self.mainV)

        self.btnQuit.clicked.connect(self.close)
        self.Button1.clicked.connect(self.calculate)
        self.btnClear.clicked.connect(self.clear)

    def CScosClick(self, enabled):
        if enabled:
            self.CS.setText('1')
            self.CSTitle.setText('Для внутренних')

    def CSsinClick(self, enabled):
        if enabled:
            self.CS.setText('2')
            self.CSTitle.setText('Для внешних')

    def calculate(self):
        self.stat.reset()
        Step = float(self.StepMasEdit.text())
        Start = float(self.StartMasEdit.text())
        End = float(self.EndMasEdit.text())
        WFCoeff = list(map(float, self.WFCoeffEdit.text().split()))
        Tmass = list(map(float, self.TmassEdit.text().split()))
        timeStep = float(self.timeStepEdit.text())
        CSch = int(self.CS.text())

        MassForRes = np.arange(Start, End, Step)
        # S = np.arange(0, (len(MassForRes)), 1)
        #  определение значения ачх на заданнйо частоте
        #  найти похожую, база данных
        #
        self.stat.setMinimum(0)
        self.stat.setMaximum(len(MassForRes))
        if len(Tmass) == len(WFCoeff) + 1:
            S = np.zeros(len(MassForRes))
            for j in range(0, len(MassForRes), 1):
                S[j] = 0
                for i in range(1, len(Tmass), 1):  # от 2 до 4
                    t = np.arange(Tmass[i - 1], Tmass[i], timeStep)
                    y = np.zeros(len(t))
                    if CSch == 2:
                        for k in range(0, len(t), 1):
                            y[k] = math.cos(2 * math.pi * MassForRes[j] * t[k])
                    if CSch == 1:
                        for k in range(0, len(t), 1):
                            y[k] = math.sin(2 * math.pi * MassForRes[j] * t[k])
                    n = len(y)
                    test = (sum(y[0:(n-1)]))
                    SetCurrent = test * timeStep + (y[0] + y[n-1]) * timeStep / 2
                    S[j] += SetCurrent * WFCoeff[i - 1]/sum(WFCoeff)
                self.stat.setValue(int(j))
                    # self.plainTextEdit.setPlainText("S=" + str(S))
        # self.plainTextEdit.appendPlainText("Step="+str(Step)+",   w="+str(MassForRes))

        self.axes.plot(MassForRes, abs(S), label="for" + str(Tmass))
        self.axes.set_xbound(lower=0, upper=MassForRes.max())
        self.axes.set_xlabel('w')
        self.axes.set_ylabel('S')
        self.axes.grid(True)
        self.axes.legend()
        self.canvas.draw()
        self.stat.setValue(len(MassForRes))

    def clear(self):
        self.axes.clear()
        self.canvas.draw()
        # self.axes.clear()
        # self.axes.plot(([-5, 5]), Tmass, label="Weight")
        # self.axes.set_xlabel('w')
        # self.axes.set_ylabel('S')
        # self.axes.grid(True)
        # self.axes.legend()
        # self.canvasWeight.draw()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Функция для нахождения площадей основных гармонических составляющих")
    window.setFixedSize(1000, 600)
    window.show()
    sys.exit(app.exec_())
