import sys , re, datetime, subprocess, socket
from PyQt5.QtWidgets import* 
from PyQt5.QtCore import* 
from PyQt5.QtGui import* 
from pymongo import MongoClient
import os, math, random, smtplib, ssl

# todo: import custom class 
from welcome_ui import Ui_Form
from mainpage import Main

class WelcomePage(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        
        # todo: create initial setup for ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle("Demo-SeminariyManager")
        self.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))

        # todo: create stackedwidget index
        self.ui.stackedWidget.setCurrentIndex(0)

        # todo: create db connection with assigned in global
        global my_col 
        self.con = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.con["seminarity"]
        self.my_col = self.db["users"]

        # todo: signin page
        # todo: create function for signin button
        self.ui.signinbt.clicked.connect(lambda: self.SignIn_Page(
            self.ui.userget,
            self.ui.passget
        ))
        # todo: signup button function
        self.ui.signupbtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        # todo: creat exit function
        self.ui.exitbtn.clicked.connect(self.exitPage)
        # todo: create function for showhide buttons
        self.ui.passget.setEchoMode(QLineEdit.Password)
        self.ui.pushButton.setChecked(True)
        self.ui.pushButton.clicked.connect(lambda: self.showKey3(
            self.ui.passget
        ))

        #####################################################################################################

        # todo: signup page 
        # todo: create function for signup button
        self.ui.signupbtn_2.clicked.connect(lambda: self.signUp_Page(
            self.ui.fnameget,
            self.ui.lnameget,
            self.ui.mailget,
            self.ui.passsget,
            self.ui.conpasssget
        ))
        # todo: create function for showhide buttons
        self.ui.passsget.setEchoMode(QLineEdit.Password)
        self.ui.conpasssget.setEchoMode(QLineEdit.Password)
        self.ui.showhide.setChecked(True)
        self.ui.showhide2.setChecked(True)
        self.ui.showhide.clicked.connect(lambda: self.showKey1(
            self.ui.passsget
        ))
        self.ui.showhide2.clicked.connect(lambda: self.showKey2(
            self.ui.conpasssget
        ))
        # todo: create function for back button
        self.ui.back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.back_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        #####################################################################################################
        # todo: forget password page
        self.ui.forgetpass.mousePressEvent = lambda event:self.ForgetPass(self.ui.stackedWidget)
        self.ui.sentotp.clicked.connect(lambda:self.sentOTP(
            self.ui.emailsent
        ))
        self.ui.changepassbtn.clicked.connect(lambda : self.ChangePass(
            self.ui.otpget,
            self.ui.passcreate,
            self.ui.conpasscreate
        ))
    def ActiveUsersGet(self):
        file_name = datetime.date.today().strftime("%d-%m-%Y")
        current_dir = os.getcwd()
        absolute_path = os.path.abspath("data/"+file_name+".txt")
        file_path = os.path.relpath(absolute_path, current_dir)
        if not os.path.isfile(file_path):
            f_create = open(file_path, "w")
            print(file_path, "created successfully")

        filename = file_path
        line_to_check = self.ui.userget.text()
        if self.check_line_exists(filename, line_to_check):
            print("Line already exists.")
        else:
            print("Line does not exist.")
            self.insert_new_line(filename, line_to_check)
            print("New line inserted.")
    def check_line_exists(self,filename, line):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for existing_line in lines:
                if existing_line.strip() == line.strip():
                    # Line exists
                    return True
        # Line does not exist
        return False
    def insert_new_line(self,filename, new_line):
        with open(filename, 'a') as file:
            file.write(new_line + '\n')
    ###################################### Forgetpasswd Page Functions ####################################
    def isConnected(self):
        try:
            sock = socket.create_connection(("www.google.com", 80))
            if sock is not None:
                print('Clossing socket')
                sock.close
            return True
        except OSError:
            pass
        return False

    def ForgetPass(self, stackedWidget):
        if self.isConnected():  
            self.ui.stackedWidget.setCurrentIndex(2)
        else:
            from tkinter import messagebox
            messagebox.showerror("Demo-SeminariyManager", "Internet isn't connected, Please connect for connect with us.\nApplication is start to need internet.")         

    def ChangePass(self, otp, passcreate, conpasscreate):
        global msg
        global my_col
        print(msg)
        if self.ui.otpget.text() =="" or self.ui.passcreate.text() == "" or self.ui.conpasscreate.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
            msg.setWindowTitle("Error")
            msg.setText("All fields requires")
            msg.setStandardButtons(QMessageBox.Ok)
            r = msg.exec_()

        elif self.ui.otpget.text() == msg:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                msg.setWindowTitle("Error")
                msg.setText("Check Your One Time Password (OTP)")
                msg.setStandardButtons(QMessageBox.Ok)
                r = msg.exec_()
                if r == QMessageBox.Ok:
                    self.ui.otpget.clear()

        else:
            
            if self.ui.passcreate.text() != self.ui.conpasscreate.text():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                msg.setText("Passwords are mismatch, Try again")
                msg.setStandardButtons(QMessageBox.Ok)
                r = msg.exec_()
            if len(self.ui.passcreate.text()) <= 6:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                msg.setText("Passwords are minimum 6 charecters, Try again")
                msg.setStandardButtons(QMessageBox.Ok)
                r = msg.exec_()
            else:
                result = self.my_col.find_one_and_update(
                    {"email":self.ui.emailsent.text()},
                    {'$set': { "passwd" : self.ui.conpasscreate.text()}}
                )
                if result:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Information")
                    msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                    msg.setText("Password successfully reseted.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    r = msg.exec_()
                    if r == QMessageBox.Ok:
                        self.ui.stackedWidget.setCurrentIndex(0)
                else:
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                    msg.setText("Something went wrong, try again")
                    msg.setStandardButtons(QMessageBox.Ok)
                    r = msg.exec_()

    def sentOTP(self, emailsent):
        global my_col
        if self.my_col.find_one({"email":self.ui.emailsent.text()}):
            self.ui.stackedWidget_2.setCurrentIndex(1)
            try:
                otpsentmail = self.Email_Send(reciver_email=self.ui.emailsent.text())
                if otpsentmail:
                    self.ui.stackedWidget_2.setCurrentIndex(1)

            except Exception as e:
                print(e)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
            msg.setText("Could't found your email address, try again")
            msg.setStandardButtons(QMessageBox.Ok)
            r = msg.exec_()
            if r == QMessageBox.Ok:
                self.ui.emailsent.clear()
            else:
                None

    def Email_Send(self, reciver_email):
        global msg
        digits="0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = OTP
        msg= otp

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "bkdev.kiru@gmail.com"  # Enter your address
        receiver_email = reciver_email # Enter receiver address
        password = "nqneefqqgqjomdaq"
        message = """\
Subject: Reset Your Password - One Time Password

This is Demo mail verfication process, If you want more information about this please visit https://github.com/balacharyadev. This is you OTP """ +msg 

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)



    ###################################### Sign-In Page Functions ####################################

    def exitPage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirmation")
        msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
        msg.setText("Are you sure to want exit?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        r = msg.exec_()
        if r == QMessageBox.Yes:
            self.close()
        else:
            None

    def showKey3(self, passget):
        if self.ui.pushButton.isChecked():
            self.ui.passget.setEchoMode(QLineEdit.Password)
        else:
            self.ui.passget.setEchoMode(QLineEdit.Normal)
    
    def SignIn_Page(self, userget, passget):
        if self.ui.userget.text() == "" or self.ui.passget.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
            msg.setText("All fields requires and try again")
            msg.setStandardButtons(QMessageBox.Ok)
            r = msg.exec_()
        elif (len(self.ui.passget.text())) <= 6:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
            msg.setText("Password must be 6 charecters is minimum")
            msg.setStandardButtons(QMessageBox.Ok)
            r = msg.exec_()
        else:
            global my_col 
            try:
                data_find = {
                    "email": self.ui.userget.text(),
                    "passwd": self.ui.passget.text()
                }
                # print(data_find)
                result = self.my_col.find_one(data_find)
                if result:
                    self.ActiveUsersGet()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Login Status")
                    msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                    msg.setText("Logined Successfully.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    r = msg.exec_()
                    if r == QMessageBox.Ok:
                        self.nextpageCall()
                        # todo: create active users for static
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                    msg.setText("Email and password are mismatch. Try again")
                    msg.setStandardButtons(QMessageBox.Ok)
                    r = msg.exec_()
                    if r == QMessageBox.Ok:
                        self.ui.userget.clear()
                        self.ui.passget.clear()

            except Exception as e:
                print(e)

    def nextpageCall(self, *args):
        path = "src\mainpage.py"
        try:
            if path:
                self.close()
                Main().show()
        except Exception as e:
            print(e)


    ###################################### Sign-Up Page Functions ####################################
    def showKey2(self, conpasssget):
        if self.ui.showhide2.isChecked():
            self.ui.conpasssget.setEchoMode(QLineEdit.Password)
        else:
            self.ui.conpasssget.setEchoMode(QLineEdit.Normal)

    def showKey1(self, passsget):
        if self.ui.showhide.isChecked():
            self.ui.passsget.setEchoMode(QLineEdit.Password)
        else:
            self.ui.passsget.setEchoMode(QLineEdit.Normal)
    def clearData(self, fnameget, lnameget, mailget, passsget, conpasssget):
        self.ui.fnameget.clear()
        self.ui.lnameget.clear()
        self.ui.mailget.clear()
        self.ui.passsget.clear()
        self.ui.conpasssget.clear()
        

    def signUp_Page(self, fnameget, lnameget, mailget, passsget, conpasssget):
        try:
            if self.ui.fnameget.text() == "" or self.ui.lnameget.text() == "" or self.ui.mailget.text() == "" or self.ui.passsget.text() == "" or self.ui.conpasssget.text() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                msg.setText("All fields requires and try again")
                msg.setStandardButtons(QMessageBox.Ok)
                r = msg.exec_()

            elif self.ui.passsget.text() != self.ui.conpasssget.text():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                msg.setText("Password should be in same and try again")
                msg.setStandardButtons(QMessageBox.Ok)
                r = msg.exec_()                
            
            else:
                global mycol 
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                if(re.fullmatch(regex, self.ui.mailget.text())):
                    
                    try:
                        data = {
                            "fullname": self.ui.fnameget.text()+" "+self.ui.lnameget.text(),
                            "email": self.ui.mailget.text(),
                            "passwd":self.ui.conpasssget.text()
                        }
                        # chk_1 = self.my_col.find_one({"fullname": self.ui.fnameget.text()+" "+self.ui.lnameget.text()})
                        chk_2 = self.my_col.find_one({'email': self.ui.mailget.text()})

                        if chk_2:
                            global my_col
                            self.ui.emailerror.setText("EMail-Id already registered, choose another one.")
                            
                        else:
                            try:
                                if self.my_col.find_one({'email': self.ui.mailget.text()}):
                                    self.ui.emailerror.setText("EMail-Id already registered, choose another one.")
                                elif (len(self.ui.passsget.text())) <= 6:
                                    msg = QMessageBox()
                                    msg.setIcon(QMessageBox.Information)
                                    msg.setWindowTitle("Error")
                                    msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                                    msg.setText("Password must be 6 charecters is minimum")
                                    msg.setStandardButtons(QMessageBox.Ok)
                                    r = msg.exec_()
                                else:
                                    self.ui.emailerror.setText(" ")
                                    result = self.my_col.insert_one(data)
                                    if result:
                                        msg = QMessageBox()
                                        msg.setIcon(QMessageBox.Information)
                                        msg.setWindowTitle("Success")
                                        msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                                        msg.setText(f"{self.ui.fnameget.text()+' '+self.ui.lnameget.text()}, profile created successfully.")
                                        msg.setStandardButtons(QMessageBox.Ok)
                                        r = msg.exec_()
                                        if r == QMessageBox.Ok:
                                            self.clearData(
                                                self.ui.fnameget,
                                                self.ui.lnameget,
                                                self.ui.mailget,
                                                self.ui.passsget,
                                                self.ui.conpasssget
                                            )
                                            self.ui.stackedWidget.setCurrentIndex(0)
                                    
                                    
                                    else:
                                        msg = QMessageBox()
                                        msg.setIcon(QMessageBox.Information)
                                        msg.setWindowTitle("Error")
                                        msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                                        msg.setText("Something went wrong. try again later")
                                        msg.setStandardButtons(QMessageBox.Ok)
                                        r = msg.exec_()
                            except Exception as e:
                                print(e)
                            
                    except Exception as e:
                        print(e)

                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(QIcon("assets/logo/__smlogo.ico"))
                    msg.setText("Email id is invalid and try with different one.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    r = msg.exec_()
        except:
            print("its work")



def main():
    app = QApplication(sys.argv)
    w = WelcomePage()
    w.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()