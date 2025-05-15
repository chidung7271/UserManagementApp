from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)

    def plot(self, dates, weights, heights):
        self.axes.clear()
        self.axes.plot(dates, weights, label="Cân nặng (kg)", marker='o', color='blue')
        self.axes.plot(dates, heights, label="Chiều cao (cm)", marker='o', color='green')

        # Định dạng trục X (ngày)
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        self.axes.xaxis.set_major_locator(mdates.MonthLocator())
        self.axes.tick_params(axis='x', rotation=45)

        self.axes.set_title("Sự phát triển cân nặng và chiều cao")
        self.axes.set_xlabel("Thời gian")
        self.axes.set_ylabel("Giá trị")
        self.axes.legend()
        self.draw()