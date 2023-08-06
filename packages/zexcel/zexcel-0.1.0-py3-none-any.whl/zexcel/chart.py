import matplotlib.pyplot as plt


class Canvas:
    def __init__(self):
        self.canvas = plt.figure()
        plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

    def cell(self,w, h, p):
        self.canvas.add_subplot(w,h,p)

    def plot(self, xs, ys, type, props = {}):
        if xs == None:
            xs = range(len(ys))
        if type == None:
            plt.plot(xs, ys, **props)
        elif type =='scatter':
            plt.scatter(xs, ys, **props)

    def draw(self, xs, ys, props = {}):
        self.plot(xs, ys, None, props)

    def scatter(self, xs, ys, props = {}):
        self.plot(xs, ys, 'scatter', props)

    def hist(self, xs, props = {}):
        plt.hist(xs, **props)

    def pie(self, xs, props = {}):
        plt.pie(xs, **props)

    @staticmethod
    def title(title):
        plt.title(title)

    @staticmethod
    def xlabel(label):
        plt.xlabel(label)

    @staticmethod
    def ylabel(label):
        plt.ylabel(label)

    @staticmethod
    def legend():
        plt.legend()

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(filename, props = {}):
        plt.savefig(filename, **props)






