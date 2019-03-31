import matplotlib.pyplot as pl


def plot(xs, ys, title):
    figure, axis = pl.subplots()
    axis.set_title(title)
    axis.plot(xs, ys[:, 0], label='X')
    axis.plot(xs, ys[:, 1], label='Y')
    axis.plot(xs, ys[:, 2], label='Z')
    pl.xlabel('time (s)')
    pl.ylabel('magnitude')
    axis.legend(loc=5, bbox_to_anchor=(1.15, 0.92))
    figure.show()
