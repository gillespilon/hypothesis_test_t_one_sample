#! /usr/bin/env python3
"""
A one-sample t test answers these questions:

Is the average of a sample different from a specified value?
Is the average of a sample less than a specified value?
Is the average of a sample greater than a specified value?
What is the range of values that is likely to include the population average?

- The data are continuous (interval or ratio scales).
- The data in a sample follow a normal distribution with mean  𝜇
  and variance  𝜎2 .
- The sample variance  𝑠2  follows a  𝜒2  distribution with  𝜌  degrees of
  freedom under the null hypothesis, where  𝜌  is a positive constant.
- (𝑌 - 𝜇)  and the sample standard deviation  𝑠  are independent.

The first column of the dataset must be the "x" and can be labelled in any
manner you wish. It is a series of integers that are sample IDs.
The second column of the dataset must be the "y" and can be labelled in any
manner you wish. It is a series of integers or floats.

Requires:
- datasense https://github.com/gillespilon/datasense
"""

from pathlib import Path
import time

import statsmodels.stats.power as smp
import scipy.stats as stats
import datasense as ds
import pandas as pd
import numpy as np


def main():
    filetypes = [("csv and feather files", ".csv .CSV .feather .FEATHER")]
    path_in_title = "Select csv or feather file to read"
    initialdir = Path(__file__).parent.resolve()
    output_url = "one_sample_t_test.html"
    header_title = "One-sample t test"
    header_id = "one-smaple-t-test"
    significance_level = 0.05
    hypothesized_value = 400
    colour = "#0077bb"
    decimals = 3
    path_in = ds.ask_open_file_name_path(
        title=path_in_title,
        initialdir=initialdir,
        filetypes=filetypes
    )
    start_time = time.perf_counter()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    ds.script_summary(
        script_path=Path(__file__),
        action="started at"
    )
    ds.style_graph()
    print("Data file", path_in)
    print()
    df = ds.read_file(file_name=path_in)
    columns = df.columns
    columny = columns[0]
    y = df[columny][df[columny].notna()]
    n = df[columny].count()
    print("Scenario 1")
    print()
    result = ds.one_sample_t(
        series=y,
        hypothesized_value=hypothesized_value,
        alternative_hypothesis="two-sided"
    )
    print("Scenario 2")
    print()
    result = ds.one_sample_t(
        series=y,
        hypothesized_value=hypothesized_value,
        alternative_hypothesis="less"
    )
    print("Scenario 3")
    print()
    result = ds.one_sample_t(
        series=y,
        hypothesized_value=hypothesized_value,
        alternative_hypothesis="greater"
    )
    fig, ax = ds.plot_histogram(series=y)
    ax.set_xlabel("Y (units)")
    ax.set_ylabel("Count")
    ax.set_title(label="Histogram")
    fig.savefig(fname="histogram.svg", format="svg")
    ds.html_figure(
        file_name="histogram.svg",
        caption="histogram.svg"
    )
    stop_time = time.perf_counter()
    ds.script_summary(
        script_path=Path(__file__),
        action="finished at"
    )
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == "__main__":
    main()
