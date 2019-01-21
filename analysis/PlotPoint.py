class PlotPoint(object):
    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val

    def str(self):
        return "({}, {})".format(self.x_val, self.y_val)

def plot_point_list_to_axes(point_list):
    x_axis = np.zeros(len(point_list))
    y_axis = np.zeros(len(point_list))

    for idx, data_point in enumerate(point_list):
        x_axis[idx] = data_point.x_val
        y_axis[idx] = data_point.y_val

    return (x_axis, y_axis)
