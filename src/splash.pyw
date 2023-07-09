import sys , time, subprocess
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import*
from PyQt5.QtWidgets import* 
from splash_ui import Ui_Form
from welcomepage import WelcomePage

class SplashScreen(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))

		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.counter = 0
		self.n = 300 # total instance
		self.timer = QTimer()
		self.timer.timeout.connect(self.progress)
		self.timer.start(30)

	def progress(self):
		self.ui.progressBar.setValue(self.counter)
		time.sleep(0.1)
		self.counter += 1
		if self.counter == 100:
			self.close()
			# subprocess.call("python src\welcomepage.py", shell=True)
			w = WelcomePage()
			w.show()
def main():
	app = QApplication(sys.argv)
	s = SplashScreen()
	s.progress()
	s.show()
	try:
		sys.exit(app.exec_())
	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()
