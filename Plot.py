import logging as Logger
import logging
import seaborn as sns
import matplotlib.pyplot as plt

class Plot:
    # Constructor
    def __init__(self):
        self.logger = Logger(name="Plot_Logger")
        self.logger.setLevel(logging.INFO)

        # Configure logging to send messages to stdout
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    # Function to plot a bar chart
    def bar_chart(self, data, x, y, title, xlabel, ylabel):
        sns.barplot(data=data, x=x, y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    # Function to plot a line chart
    def line_chart(self, data, x, y, title, xlabel, ylabel):
        sns.lineplot(data=data, x=x, y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    # Function to plot a scatter chart
    def scatter_chart(self, data, x, y, title, xlabel, ylabel):
        sns.scatterplot(data=data, x=x, y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    # Function to plot a pie chart
    def pie_chart(self, data, x, title):
        plt.pie(data[x], labels=data[x], autopct='%1.1f%%')
        plt.title(title)
        plt.show()