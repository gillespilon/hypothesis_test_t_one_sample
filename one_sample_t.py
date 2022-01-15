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
"""

from typing import IO, List, NoReturn, Tuple, Union
from pathlib import Path
import time

import statsmodels.stats.diagnostic as smd
import statsmodels.stats.power as smp
import scipy.stats as stats
import datasense as ds
import pandas as pd
import numpy as np


def create_dataframe(
    title: str, filetypes: List[Tuple[str, str]]
) -> Tuple[pd.DataFrame, Path]:
    """
    Helper function to request Path of data file and create DataFrame.

    Parameters
    ----------
    title : str
        The title for the GUI window.
    filetypes : List[Tuple[str, str]]
        The list of acceptable data file types.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame of data.
    path_in : Path
        The Path of the input data file.

    Example
    -------
    >>> df, path_in = create_dataframe(
    >>>     title=path_in_title, filetypes=filetypes
    >>> )
    """
    initialdir = Path(__file__).parent.resolve()
    path_in = ds.ask_open_file_name_path(
        title=title, initialdir=initialdir, filetypes=filetypes
    )
    df = ds.read_file(file_name=path_in)
    return (df, path_in)


def main():
    filetypes = [("csv and feather files", ".csv .CSV .feather .FEATHER")]
    path_in_title = "Select csv or feather file to read"
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
    # data = {
    #     "x": [
    #         1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    #         20, 21, 22, 23, 24, 25
    #     ],
    #     "y": [
    #         211, 572, 558, 250, 478, 307, 184, 435, 460, 308, 188, 111, 676,
    #         326, 142, 255, 205, 77, 190, 320, 407, 333, 488, 374, 409
    #     ]
    # }
    # df = pd.DataFrame(data=data)
    df, path_in = create_dataframe(title=path_in_title, filetypes=filetypes)
    columns = df.columns
    columnx = columns[0]
    columny = columns[1]
    print()
    x = df[columnx][df[columnx].notna()]
    y = df[columny][df[columny].notna()]
    n = df[columny].count()
    standard_deviation = y.std()
    average = y.mean()
    parametric_statistics = ds.parametric_summary(
        series=y,
        decimals=3
    ).to_string()
    print("Paametric statistics")
    print(parametric_statistics)
    nonparametric_statistics = ds.nonparametric_summary(
        series=y,
        alphap=1/3,
        betap=1/3,
        decimals=3
    ).to_string()
    print()
    print("Non-paametric statistics")
    print(nonparametric_statistics)
    print()
    print("Scenario 1")
    print()
    print(
        "Ho:  𝜇  = specified value."
        "The population average equals the specified value."
    )
    print(
        "Ha:  𝜇  ≠ specified value."
        "The population average does not equal the specified value."
    )
    print()
    qdresult = stats.ttest_1samp(y, hypothesized_difference)
    power = smp.ttest_power(
        np.abs(
            (hypothesized_difference - average) / standard_deviation
        ),
        nobs=n,
        alpha=significance_level,
        alternative='two-sided'
    )
    if qdresult.pvalue < significance_level:
        print('statistically significant')
        significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": qdresult.pvalue,
                "power": power
            }
        ).round(decimals=3).to_string()
        print(significant)
    else:
        print('not statistically significant')
        not_significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": qdresult.pvalue,
                "power": power
            }
        ).round(decimals=3).to_string()
        print(not_significant)
    print()
    stop_time = time.time()
    print("Scenario 2")
    print()
    print(
        "Ho:  𝜇  = specified value."
        "The population average equals the specified value."
    )
    print(
        "Ha:  𝜇  < specified value."
        "The population average is less than the specified value."
    )
    print()
    power = smp.ttest_power(
        np.abs(
            (hypothesized_difference - average) / standard_deviation
        ),
        nobs=n,
        alpha=significance_level,
        alternative='smaller'
    )
    if hypothesized_difference < average:
        pvalue2 = (1 - qdresult.pvalue / 2)
    else:
        pvalue2 = qdresult.pvalue / 2
    if pvalue2 < significance_level:
        print('statistically significant')
        significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue2,
                "power": power
            }
        ).round(decimals=3).to_string()
        print(significant)
    else:
        print('not statistically significant')
        not_significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue2,
                "power": power
            }
        ).round(decimals=3).to_string()
        print(not_significant)
    print()
    print("Scenario 3")
    print()
    print(
        "Ho:  𝜇  = specified value."
        "The population average equals the specified value."
    )
    print(
        "Ha:  𝜇  > specified value."
        "The population average is greater than the specified value."
    )
    print()
    power = smp.ttest_power(
        np.abs(
            (hypothesized_difference - average) / standard_deviation
        ),
        nobs=n,
        alpha=significance_level,
        alternative='larger'
    )
    if hypothesized_difference < average:
        pvalue3 = qdresult.pvalue / 2
    else:
        pvalue3 = (1 - qdresult.pvalue / 2)
    if pvalue3 < significance_level:
        print('statistically significant')
        significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue3,
                "power": power
            }
        ).round(decimals=3).to_string()
        print(significant)
    else:
        print('not statistically significant')
        not_significant = pd.Series(
            data={
                "test statistic": qdresult.statistic,
                "p value": pvalue3,
                "power": power
            }
        ).round(decimals=3).to_string()
        print(not_significant)
    print()
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
