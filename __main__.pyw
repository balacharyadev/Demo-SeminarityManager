import os, sys
import subprocess

def initUi():
	relative_path = "src\__init__.py"
	if relative_path:
		os.system("cls")
		os.system("echo Program is running")
		subprocess.call(relative_path, shell=True)

def main():
	path = "requirements.txt"
	if path:
		os.system("echo Checking Python Libraries...please wait ")
		os.system("timeout /t 3 /nobreak")
		os.system("pip install -r "+path)
		initUi()
			
	else:
		print("error")
if __name__ == '__main__':
	# main()
	initUi()
