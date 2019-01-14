class PlotPoint(object):
    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val

    def str(self):
        return "({}, {})".format(self.x_val, self.y_val)
