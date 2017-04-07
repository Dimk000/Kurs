from PyQt5 import QtCore, QtGui
import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from matplotlib.figure import Figure
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        self.CSsin = QRadioButton("Sin")
        self.CScos = QRadioButton("Cos")

        self.CSsin.toggled.connect(self.CSsinClick)
        self.CScos.toggled.connect(self.CScosClick)

        self.CSsin.setChecked(True)

        self.btnQuit = QPushButton("Закрыть")
        self.Button1 = QPushButton("Вычислить")
        self.BtnClear = QPushButton("Очистить")

        self.plainTextEdit = QPlainTextEdit()

        self.hbox_main = QHBoxLayout()
        self.hbox_name = QHBoxLayout()
        self.hbox_edit = QHBoxLayout()
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
        self.vbox.addWidget(self.BtnClear)
        self.vbox.addWidget(self.btnQuit)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        ### 111 - признак расположения нескольких графиков)

        self.canvas = FigureCanvas(self.figure)
        # self.canvasWeight = FigureCanvas(self.figure)

        self.vbox_graph.addWidget(self.canvas)
        self.vbox_dop_character.addWidget(self.plainTextEdit)

        self.hbox_main.addLayout(self.vbox)
        self.hbox_main.addLayout(self.vbox_graph)
        self.hbox_main.addLayout(self.vbox_dop_character)

        self.frame_win1 = QFrame()
        self.frame_win1.setLayout(self.hbox_main)
        # self.setLayout(self.hbox_main)
        self.mainV = QVBoxLayout()

        self.tab = QTabWidget()
        self.tab.addTab(self.frame_win1, "lol")

        self.mainV.addWidget(self.tab)
        self.setLayout(self.mainV)

        self.btnQuit.clicked.connect(self.close)
        self.BtnClear.clicked.connect(self.clear)
        self.Button1.clicked.connect(self.calculate)


    def CScosClick(self, enabled):
        if enabled:
            self.CS.setText('1')
            self.CSTitle.setText('for cos')

    def CSsinClick(self, enabled):
        if enabled:
            self.CS.setText('2')
            self.CSTitle.setText('for sin')

    def calculate(self):
        Step = float(self.StepMasEdit.text())
        Start = float(self.StartMasEdit.text())
        End = float(self.EndMasEdit.text())
        WFCoeff = list(map(float, self.WFCoeffEdit.text().split()))
        Tmass = list(map(float, self.TmassEdit.text().split()))
        timeStep = float(self.timeStepEdit.text())
        CSch = int(self.CS.text())

        MassForRes = np.arange(Start, End, Step)
        # S = np.arange(0, (len(MassForRes)), 1)
        S = []

        i = 2
        if len(Tmass) == len(WFCoeff)+1:
            for j in range(len(MassForRes)):
                for i in range(len(Tmass)):  # от 2 до 4
                    t = []
                    n = Tmass[0]
                    while n < Tmass[len(Tmass)-1]:
                        n += timeStep
                        t.append(n)
                    y = np.zeros(len(t))
                    if CSch == 2:
                        for k in range(len(t)):
                            y[k] = math.cos(2 * math.pi * MassForRes[j] * t[k])
                    if CSch == 1:
                        for k in range(len(t)):
                            y[k] = math.sin(2 * math.pi * MassForRes[j] * t[k])
                n = len(y)
                test = (sum(y[2:n - 2]))
                Scurrent = abs(test * timeStep + (y[1] + y[n - 1]) * timeStep / 2)
                print(Scurrent)
                S.append(Scurrent*WFCoeff[i-1])

        self.plainTextEdit.setPlainText("S=" + str(S))
        self.plainTextEdit.appendPlainText("Step="+str(Step)+",   w="+str(MassForRes))

        self.axes.plot(MassForRes, S, label="fck this shit")
        self.axes.set_xbound(lower=0, upper=MassForRes.max())
        self.axes.set_xlabel('w')
        self.axes.set_ylabel('S')
        self.axes.grid(True)
        self.axes.legend()
        self.canvas.draw()

    def clear(self):
        self.axes.clear()

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
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())