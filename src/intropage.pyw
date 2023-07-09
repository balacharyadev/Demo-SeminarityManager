import sys, webbrowser, os
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import* 
from about_ui import Ui_Dialog


class IntroPage(QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Demo-Seminariy Manager - About Me")
		self.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
		self.ui.pushButton.clicked.connect(self.OpenLicense)
		self.ui.pushButton_2.clicked.connect(self.OpenURL)

	def OpenLicense(self):
		current_dir = os.getcwd()
		absolute_path = os.path.abspath("../License.txt")
		# file_path = os.path.relpath(absolute_path, current_dir)
		file_path = "License.txt"
		if file_path:
			os.system("notepad.exe License.txt")#+file_path)
		else:
			print("eroor")
	def OpenURL(self):
		def open_link(url):
			webbrowser.open(url)
		url = "https://www.github.com/balacharyadev/Demo-SeminariyManager"
		open_link(url)

def main():
	app = QApplication(sys.argv)
	i = IntroPage()
	i.show()
	try:
		sys.exit(app.exec_())
	except Exception as e:
		print(e)
if __name__ == '__main__':
	main()