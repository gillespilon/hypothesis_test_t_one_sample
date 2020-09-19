#! /usr/bin/env python3
'''
Compare of matplotlib.pyplot vs pandas for normal probability plot.

- matplotlib.pyplot requires one line
- pandas requires three line

time -f '%e' ./pythonic_probability_plots_with_pyplot_or_pandas.py
./pythonic_probability_plots_with_pyplot_or_pandas.py
'''

import matplotlib.pyplot as plt
from scipy.stats import norm, probplot
import pandas as pd
import numpy as np

figure_width_height = (8, 6)
x_axis_label = 'Theoretical quantiles (osm)'
y_axis_label = 'Ordered values (osr)'
axes_title = 'Normal Probability Plot'
file_name_graph_matplotlib = 'npp_matplotlib.svg'
file_name_graph_pandas = 'npp_pandas.svg'


def main():
    # Generate the data
    y = np.random.normal(loc=0, scale=1, size=100)
    # matplotlib.pyplot
    fig = plt.figure(figsize=figure_width_height)
    ax = fig.add_subplot(111)
    (osm, osr), (slope, intercept, r) = probplot(
        x=y,
        dist=norm,
        plot=ax,
        fit=True
    )
    ax.set_title(axes_title)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.figure.savefig(file_name_graph_matplotlib)
    # pandas.plot.scatter
    df = pd.DataFrame.from_dict({x_axis_label: osm,
                                 y_axis_label: osr})
    fig = plt.figure(figsize=figure_width_height)
    ax = fig.add_subplot(111)
    ax = df.plot.scatter(
        x=x_axis_label,
        y=y_axis_label,
        ax=ax
    )
    (osm, osr), (slope, intercept, r) = probplot(y, plot=ax, fit=True)
    ax.set_title(axes_title)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.figure.savefig(file_name_graph_pandas)


if __name__ == '__main__':
    main()
