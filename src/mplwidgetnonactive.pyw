import sys, os, datetime
import matplotlib
matplotlib.use('Qt5Agg') 

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pymongo import MongoClient

class MplWidgetNonActive(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplWidgetNonActive, self).__init__(fig)

        self.server = "localhost"
        self.port = int("27017")
        self.db = "seminarity"
        self.col = "users"
        self.conserv = MongoClient(self.server, self.port)
        self.condb = self.conserv[self.db]
        self.concol = self.condb[self.col]
        self.db_result = self.concol.count_documents({})

        file_name = datetime.date.today().strftime("%d-%m-%Y")
        _path = os.path.dirname(__file__)
        # file_path = os.path.join(_path, "../data/"+file_name+".txt")
        file_path = 'data/'+file_name+".txt"
        with open(file_path, "r") as fi:          
            lines = len(fi.readlines())

        non = int(self.db_result)-int(lines)
        print("non active", non)
        self.NonActiveUserGet(non)

    def NonActiveUserGet(self, non):
        labels = 'Non-Active', 'None'
        sizes = [int(non),100]
        self.ax.pie(sizes, labels=labels,
               colors=['red', 'lightgrey'])
        
