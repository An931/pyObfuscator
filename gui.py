#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QPushButton, QFileDialog, QWidget, QMainWindow, QTextEdit, QAction, QApplication, 
QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QIcon
from start import *


class ObfuscatorApp(QMainWindow):

	def __init__(self):
			super().__init__()
			self.initUI()


	def initUI(self):

		self.origin_text = QTextEdit(self)
		self.changed_text = QTextEdit(self)
		self.changed_text.setReadOnly(True)
		# list_font = QFont()
		# list_font.fromString(self.list.font().toString())
		# self.text.setFont(list_font)

		button = QPushButton('obfuscate', self)
		button.clicked.connect(self.obfuscate_code)

		hlayout = QHBoxLayout()
		vlayout = QVBoxLayout(self)
		hlayout.addWidget(self.origin_text)
		hlayout.addWidget(button)
		hlayout.addWidget(self.changed_text)
		vlayout.addLayout(hlayout)

		central_widget = QWidget()
		central_widget.setLayout(vlayout)
		self.setCentralWidget(central_widget)
		# self.setCentralWidget(button)
		# self.setCentralWidget(self.origin_text)

		fileMenu = self.menuBar().addMenu("&File")
		openAction = fileMenu.addAction("&Open...")
		openAction.setShortcut("Ctrl+O")
		openAction.triggered.connect(self.open_code)

		self.setGeometry(150, 100, 1000, 700)
		self.setWindowTitle('Obfuscator')
		self.show()


	def open_code(self, path=None):
		if not path:
			path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
						"Image Files (*.py)")

		if path:
			with open(path) as f:
				self.text_to_obfuscate = f.read()
				self.origin_text.setText(self.text_to_obfuscate)
			# if not newImage.load(path):
			# 	QMessageBox.warning(self, "Open Image",
			# 					"The image file could not be loaded.",
			# 					QMessageBox.Cancel)
				# return

	def obfuscate_code(self):
		if not self.origin_text.toPlainText():
			return
		new_text = Obfuscator.obfuscate(self.origin_text.toPlainText())
		self.changed_text.setText(new_text)
		# self.changed_text.setText(self.origin_text.toPlainText())



if __name__ == '__main__':

		app = QApplication(sys.argv)
		ex = ObfuscatorApp()
		sys.exit(app.exec_())