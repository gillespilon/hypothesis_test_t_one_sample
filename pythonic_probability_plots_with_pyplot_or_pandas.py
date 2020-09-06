#! /usr/bin/env python3

'''
Comparison of matplotlib.pyplot vs pandas for normal probability plot.

- matplotlib.pyplot requires one line
- pandas requires three line

time -f '%e' ./pythonic_probability_plots_with_pyplot_or_pandas.py
./pythonic_probability_plots_with_pyplot_or_pandas.py
'''


import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import numpy as np


figure_width_height = (8, 6)
x_axis_label = 'Theoretical quantiles (osm)'
y_axis_label = 'Ordered values (osr)'
axes_title = 'Normal Probability Plot'


def main():
    # Generate the data
    y = np.random.normal(0, 1, 100)
    x = list(range(100))
    # matplotlib.pyplot
    fig = plt.figure(figsize=figure_width_height)
    ax = fig.add_subplot(111)
    (osm, osr), (slope, intercept, r) = stats.probplot(y, plot=ax, fit=True)
    ax.set_title(axes_title)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    # pandas.plot.scatter
    df = pd.DataFrame.from_dict({x_axis_label: osm,
                                 y_axis_label: osr})
    fig = plt.figure(figsize=figure_width_height)
    ax = fig.add_subplot(111)
    ax = df.plot.scatter(
        x=x_axis_label,
        y=y_axis_label,
        title=axes_title,
        ax=ax
    )
    (osm, osr), (slope, intercept, r) = stats.probplot(y, plot=ax, fit=True)
    ax.plot([-3, 3], [-3, 3], 'r-')


if __name__ == '__main__':
    main()
