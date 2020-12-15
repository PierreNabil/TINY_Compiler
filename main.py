"""
4th CSE - FoE ASU
System Software (Compilers)
Project 1: TINY Scanner

Team Members:
	Pierre Nabil
	Girgis Michael
	John Bahaa
	Hazem Mohammed
"""

from tiny_scanner import scan_file
from tiny_parser import Parser
from parserError import MatchingError

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 781, 561))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CodeLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CodeLabel.setFont(font)
        self.CodeLabel.setObjectName("CodeLabel")
        self.verticalLayout_2.addWidget(self.CodeLabel)
        self.CodeText = QtWidgets.QTextEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.CodeText.setFont(font)
        self.CodeText.setObjectName("CodeText")
        self.verticalLayout_2.addWidget(self.CodeText)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.TokensLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TokensLabel.setFont(font)
        self.TokensLabel.setObjectName("TokensLabel")
        self.verticalLayout.addWidget(self.TokensLabel)
        self.TokensText = QtWidgets.QTextEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TokensText.setFont(font)
        self.TokensText.setReadOnly(True)
        self.TokensText.setObjectName("TokensText")
        self.verticalLayout.addWidget(self.TokensText)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ShowParseTreeChkBox = QtWidgets.QRadioButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ShowParseTreeChkBox.setFont(font)
        self.ShowParseTreeChkBox.setChecked(False)
        self.ShowParseTreeChkBox.setObjectName("ShowParseTreeChkBox")
        self.verticalLayout_5.addWidget(self.ShowParseTreeChkBox)
        self.ShowSyntaxTreeChkBox = QtWidgets.QRadioButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ShowSyntaxTreeChkBox.setFont(font)
        self.ShowSyntaxTreeChkBox.setChecked(True)
        self.ShowSyntaxTreeChkBox.setObjectName("ShowSyntaxTreeChkBox")
        self.verticalLayout_5.addWidget(self.ShowSyntaxTreeChkBox)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.CompCurrentBtn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CompCurrentBtn.sizePolicy().hasHeightForWidth())
        self.CompCurrentBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CompCurrentBtn.setFont(font)
        self.CompCurrentBtn.setObjectName("CompCurrentBtn")
        self.CompCurrentBtn.clicked.connect(self.compileFromText)
        self.horizontalLayout.addWidget(self.CompCurrentBtn)
        self.CompFileBtn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CompFileBtn.sizePolicy().hasHeightForWidth())
        self.CompFileBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CompFileBtn.setFont(font)
        self.CompFileBtn.setObjectName("CompFileBtn")
        self.CompFileBtn.clicked.connect(self.compileFromFile)
        self.horizontalLayout.addWidget(self.CompFileBtn)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TINY Language Compiler"))
        self.CodeLabel.setText(_translate("MainWindow", "Code:"))
        self.CodeText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
			"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
			"p, li { white-space: pre-wrap; }\n"
			"</style></head><body style=\" font-family:\'Courier New\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
			"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">{Write TINY Code Here!}</span></p></body></html>"))
        self.TokensLabel.setText(_translate("MainWindow", "Tokens:"))
        self.TokensText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
			"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
			"p, li { white-space: pre-wrap; }\n"
			"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
			"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.ShowParseTreeChkBox.setText(_translate("MainWindow", "Show Parse Tree"))
        self.ShowSyntaxTreeChkBox.setText(_translate("MainWindow", "Show Syntax Tree"))
        self.CompCurrentBtn.setText(_translate("MainWindow", "Compile Current Code"))
        self.CompFileBtn.setText(_translate("MainWindow", "Compile Code from File"))

    def compileFromText(self):
        with open('data/current_code.txt', 'w') as input_file:
            input_file.write(self.CodeText.toPlainText())
        self._compile()

    def compileFromFile(self):
        input_filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Code File')
        if input_filename[0][-4:] == '.txt':
            self._compile(input_filename[0])
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please select a ".txt" file')
            msg.setWindowTitle("Error")
            msg.exec_()

    def _compile(self, input_filename='data/current_code.txt'):
        scan_file(input_filename, 'data/token_list.txt')

        with open('data/token_list.txt', 'r') as output_file:
            self.TokensText.setText(output_file.read())

        if self.ShowParseTreeChkBox.isChecked() or self.ShowSyntaxTreeChkBox.isChecked():
            parser = Parser('data/token_list.txt')
            try:
                parser.parse_tokens()
            except Exception as err:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(err))
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                parser.show(self.ShowParseTreeChkBox.isChecked(), self.ShowSyntaxTreeChkBox.isChecked())
                parser.save()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
