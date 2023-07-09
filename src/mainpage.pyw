import sys, os, webbrowser
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import* 
import datetime
from pymongo import MongoClient
from mainpage_ui import Ui_MainWindow
from intropage import IntroPage

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle("Demo-Seminariy Manager")
        self.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))

        # todo: initial setup for mainpage
        self.ui.frame_2.hide()
        self.ui.stackedWidget.setCurrentIndex(0)

        # todo: db configuration from setting
        global db_result
        self.server = "localhost"
        self.port = int("27017")
        self.db = "seminarity"
        self.col = "users"
        self.conserv = MongoClient(self.server, self.port)
        self.condb = self.conserv[self.db]
        self.concol = self.condb[self.col]
        self.db_result = self.concol.count_documents({})

        

        # todo: create func for sidebar icons
        self.ui.statusbar.showMessage("Welcome to Demo-Seminariy Manager")
        self.ui.pushButton_2.setChecked(True)
        self.ui.pushButton.clicked.connect(self.AboutPage)
        self.ui.pushButton_2.clicked.connect(lambda : self.home_page(self.ui.statusbar))
        self.ui.pushButton_3.clicked.connect(lambda : self.static_page(self.ui.statusbar))
        self.ui.pushButton_4.clicked.connect(lambda : self.setting_page(self.ui.statusbar))
        self.ui.pushButton_17.clicked.connect(lambda : self.search_page(self.ui.statusbar))

        self.ui.pushButton_6.clicked.connect(self.AboutPage)
        self.ui.pushButton_7.clicked.connect(lambda : self.home_page(self.ui.statusbar))
        self.ui.pushButton_8.clicked.connect(lambda : self.static_page(self.ui.statusbar))
        self.ui.pushButton_18.clicked.connect(lambda : self.search_page(self.ui.statusbar))
        self.ui.pushButton_9.clicked.connect(lambda : self.setting_page(self.ui.statusbar))

        # todo: create func for view stack
        self.ui.staticview.clicked.connect(lambda : self.static_page(self.ui.statusbar))
        self.ui.settingview.clicked.connect(lambda : self.setting_page(self.ui.statusbar))
        self.ui.searchview.clicked.connect(lambda : self.search_page(self.ui.statusbar))
        self.ui.moreinfoview.clicked.connect(self.OpenURL)
        self.ui.logoutview.clicked.connect(self.ExitPage)
        # todo: create function for search
        self.ui.pushButton_12.clicked.connect(lambda : self.SearchPage(self.ui.label_17, self.ui.lineEdit))

        # todo: open website url
        self.ui.pushButton_13.clicked.connect(self.OpenURL)

        # todo: create function for setting page
        self.ui.pushButton_14.clicked.connect(lambda :self.settingPage(self.ui.statusbar))

        # todo: create function for exit page
        self.ui.pushButton_5.clicked.connect(self.ExitPage)
        self.ui.pushButton_10.clicked.connect(self.ExitPage)

    def ExitPage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Demo-Seminariy Manager")
        msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
        msg.setText("Are you sure to want exit ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel )
        r = msg.exec_()
        if r == QMessageBox.Yes:
            self.close()
        else:
            self.ui.statusbar.showMessage("Exit operation canceled by user...")
    def search_page(self, statusbar):
        self.setWindowTitle("Demo-Seminariy Manager - Search")
        self.ui.stackedWidget.setCurrentIndex(3)
        self.SearchView()
        self.ui.statusbar.showMessage("Search opened...", 2000)
    def setting_page(self, statusbar):
        self.setWindowTitle("Demo-Seminariy Manager - Settings")
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.statusbar.showMessage("Settings opened...", 2000)
    def static_page(self, statusbar):
        self.setWindowTitle("Demo-Seminariy Manager - User Statics")
        self.ui.stackedWidget.setCurrentIndex(1)
        self.StaticView()
        self.ui.statusbar.showMessage("Statics opened & Updated...", 2000)
    def home_page(self, statusbar):
        self.setWindowTitle("Demo-Seminariy Manager - Home")
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.statusbar.showMessage("Home opened...", 2000)
    def settingPage(self, statusbar):
        self.setWindowTitle("Demo-Seminariy Manager - Settings")
        if self.ui.pushButton_14.isChecked():
            self.ui.statusbar.show()
        else:
            self.ui.statusbar.hide()

    def OpenURL(self):
        def open_link(url):
            webbrowser.open(url)
        url = "https://www.github.com/balacharyadev/Demo-SeminarityManager"
        open_link(url)

        
    def SearchPage(self, label_17, lineEdit):
        if len(self.ui.lineEdit.text()) <= 2:
            self.ui.statusbar.showMessage("Alert : Minimum 3 charecters required")
            self.ui.label_17.setText("Alert : Minimum 3 charecters required")
        else:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.pushButton_18.setChecked(True)
            self.ui.label_17.setText(self.ui.lineEdit.text())
            self.ui.label_17.setStyleSheet(
                'font-size:14pt;'
                )
            self.ui.statusbar.showMessage("Results Fetched....", 2000)

    def StaticView(self):
        global db_result
        self.ui.label_17.setText('Not Found...')
        self.ui.label_17.setStyleSheet(
                'font-size:14pt;'
                )
        self.ui.lineEdit.clear()
        self.ui.stackedWidget.setCurrentIndex(1)

    def SearchView(self):
        self.ui.lineEdit.setFocus(True)
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def AboutPage(self):
        self.setWindowTitle("Demo-Seminariy Manager - About Me")
        def open_link(url):
            webbrowser.open(url)
        url = "https://www.github.com/balacharyadev/Demo-SeminarityManager"
        open_link(url)

def main():
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
