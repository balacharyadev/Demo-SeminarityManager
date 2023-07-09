
import sys
from PyQt5.QtWidgets import* 
from PyQt5.QtCore import* 
from PyQt5.QtGui import* 
from splash import SplashScreen


class SrcInit(object):
	app = QApplication(sys.argv)
	w = SplashScreen()
	w.show()
	try:
		sys.exit(app.exec_())
	except Exception as e:
		print(e)

if __name__ == '__main__':
	SrcInit()