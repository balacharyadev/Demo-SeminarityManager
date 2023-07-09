import sys, os , datetime
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pymongo import MongoClient


class MplWidgetOverAll(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=4, dpi=100, **pushButton_14,):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplWidgetOverAll, self).__init__(fig)

        self.server = "localhost"
        self.port = int("27017")
        self.db = "seminarity"
        self.col = "users"
        self.conserv = MongoClient(self.server, self.port)
        self.condb = self.conserv[self.db]
        self.concol = self.condb[self.col]
        self.db_result = self.concol.count_documents({})
        print("overall doc count", self.db_result)
        file_name = datetime.date.today().strftime("%d-%m-%Y")
        current_dir = os.getcwd()
        print(current_dir)
        absolute_path = os.path.abspath("../data/"+file_name+".txt")
        # file_path = os.path.relpath(absolute_path, current_dir)
        file_path = 'data/'+file_name+".txt"


        with open(file_path, "r") as fi:          
            lines = len(fi.readlines())
            print("counted lines", lines)
        self.OverAllUserGet(self.db_result, lines)

    def OverAllUserGet(self, db_result, lines):
        labels = 'Active', 'Non-Active', 'OverAll'
        sizes = [int(lines), (int(self.db_result)-int(lines)), int(self.db_result)]
        self.ax.pie(sizes, labels=labels,
               colors=['green', 'red', 'orange'])
