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
"""

from pathlib import Path
import time

import statsmodels.stats.diagnostic as smd
import statsmodels.stats.power as smp
import scipy.stats as stats
import matplotlib.cm as cm
import datasense as ds
import pandas as pd
import numpy as np

def main():
    output_url = "one_sample_t_test.html"
    header_title = "One-sample t test"
    header_id = "one-smaple-t-test"
    hypothesized_difference = 400
    significance_level = 0.05
    start_time = time.time()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    data = {
        "x": [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25
        ],
        "y": [
            211, 572, 558, 250, 478, 307, 184, 435, 460, 308, 188, 111, 676,
            326, 142, 255, 205, 77, 190, 320, 407, 333, 488, 374, 409
        ]
    }
    df = pd.DataFrame(data=data)
    x = df['x'][df['x'].notna()]
    y = df['y'][df['y'].notna()]
    n = df['y'].count()
    parametric_statistics = ds.parametric_summary(
        series=y,
        decimals=3
    )
    print("Paametric statistics")
    print(parametric_statistics)
    nonparametric_statistics = ds.nonparametric_summary(
        series=y,
        alphap=1/3,
        betap=1/3,
        decimals=3
    )
    print()
    print("Non-paametric statistics")
    print(nonparametric_statistics)
    print()
    stop_time = time.time()
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
