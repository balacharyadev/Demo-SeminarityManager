import sys ,os ,datetime
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplWidgetActive(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplWidgetActive, self).__init__(fig)
        
        file_name = datetime.date.today().strftime("%d-%m-%Y")
        # current_dir = os.getcwd()
        # print(current_dir)
        # absolute_path = os.path.abspath("../data/"+file_name+".txt")
        # file_path = os.path.relpath(absolute_path, current_dir)
        file_path = 'data/'+file_name+".txt"

        with open(file_path, "r") as fi:          
            lines = len(fi.readlines())
            print("counted lines", lines)
        self.ActiveUserGet(lines)

    def ActiveUserGet(self, lines):
        labels = 'Active', 'None'
        sizes = [int(lines),100]
        self.ax.pie(sizes, labels=labels,
               colors=['green', 'lightgrey'])