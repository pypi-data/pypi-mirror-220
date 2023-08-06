__all__ = [
    "add_colorbar",
    "format_datetime_axis",
]

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as mdates


def add_colorbar(axis, where="right", pad=0.05, size="2%"):
    r"""Adds colorbar next to an axis"""
    divider = make_axes_locatable(axis)
    return divider.append_axes(where, size=size, pad=pad)


def format_datetime_axis(axis):
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    axis.xaxis.set_major_formatter(formatter)
