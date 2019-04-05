import pylab as pl


def plot_triple(xs, ys, title):
    figure, axis = pl.subplots()
    axis.set_title(title)
    axis.plot(xs, ys[:, 0], label='X')
    axis.plot(xs, ys[:, 1], label='Y')
    axis.plot(xs, ys[:, 2], label='Z')
    pl.xlabel('time (s)')
    pl.ylabel('magnitude')
    axis.legend(loc=5, bbox_to_anchor=(1.15, 0.92))
    figure.show()


def plot_single(xs, ys, title):
    figure, axis = pl.subplots()
    axis.set_title(title)
    axis.plot(xs, ys, label='X')
    pl.xlabel('time (s)')
    pl.ylabel('magnitude')
    axis.legend(loc=5, bbox_to_anchor=(1.15, 0.92))
    figure.show()


def show():
    pl.show()
